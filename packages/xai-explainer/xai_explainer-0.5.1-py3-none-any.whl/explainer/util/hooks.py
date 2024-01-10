import abc
from contextlib import ContextDecorator
from copy import deepcopy
import enum
from functools import partial
import os
from pathlib import Path
import re
from typing import Any, Callable, List, Optional


class WriteLevel(enum.Enum):
    DEBUG = 0
    INFO = 1
    BASIC = 2
    NONE = 3


class _LazyCopy:
    """
    Wrapper class that allows for lazy deep copying of data. This is useful for callbacks that only want to copy the data if it is actually used.

    Args:
        data: The data to wrap. If data is already a _LazyDeepCopy, it is unwrapped.
    """

    def __init__(self, data: Any):
        self._data = (
            data if not isinstance(data, _LazyCopy) else data.data
        )  # unwrap if data is already a _LazyDeepCopy

    @property
    def data(self) -> Any:
        return deepcopy(self._data)


class Hook:
    """
    Base class for callbacks.

    Args:
        level (Optional[CallbackLevel]): The level of the callback. Defaults to CallbackLevel.NONE.

    Raises:
        TypeError: If level is not of type CallbackLevel.
        ValueError: If level is not a valid CallbackLevel.
    """

    def __init__(self, level: Optional[WriteLevel] = None):
        self.level = level
        self._prefixes = []

    @property
    def level(self) -> WriteLevel:
        return self._level

    @level.setter
    def level(self, level: Optional[WriteLevel]):
        level = WriteLevel(level) if level is not None else WriteLevel.NONE
        if not isinstance(level, WriteLevel):
            raise TypeError(f"level must be of type {WriteLevel}, not {type(level)}")
        self._level = level

    @property
    def prefix(self) -> str:
        prefix_builder = ""
        for idx, _prefix in enumerate(self._prefixes):
            prefix_builder += _prefix
            prefix_builder += "/" if idx != len(self._prefixes) - 1 else ""

        return prefix_builder

    @staticmethod
    def _check_url(url: str):
        if not isinstance(url, str):
            raise TypeError(f"prefix must be of type str, not {type(url)}")
        if len(url) == 0:
            raise ValueError("prefix must not be empty")

        ALLOWED_CHARS = r"[a-zA-Z0-9_+-,&%\[\]=\(\)\.]"
        target_regex = r"^{}+(/{}+)*/?$".format(ALLOWED_CHARS, ALLOWED_CHARS)
        target_regex = re.compile(target_regex)

        if not target_regex.match(url):
            allowed_chars = "_+-,[]=()."
            expected_format = "identifier/identifier/.../identifier"
            raise ValueError(
                f'Invalid URL: "{url}". Only URLs in the format "{expected_format}" are allowed, '
                f"where 'identifier' is an alphanumeric string with the additional characters: \"{allowed_chars}\". "
                f"Examples: 'some_id', 'id/', 'id1/id2'."
            )

    @staticmethod
    def _prepare_url(url: str) -> str:
        Hook._check_url(url)
        return url.strip("/")

    @abc.abstractmethod
    def _handle_data_write(self, url: str, data: _LazyCopy):
        """
        Handles the writing of the data. This method should be implemented by subclasses.

        Args:
            url (str): The url to write the data to.
            data (_LazyDeepCopy): The data to write. Note: This is a _LazyDeepCopy, so it must be unwrapped before use (see _LazyDeepCopy.data)
        """
        pass

    def _is_enabled_for(self, level: WriteLevel) -> bool:
        return self.level.value <= level.value

    def _handle_data_write_internal(self, url: str, data: Any):
        suffix = self._prepare_url(url)
        full_url = suffix if self.prefix == "" else f"{self.prefix}/{suffix}"
        self._handle_data_write(full_url, _LazyCopy(data))

    def extend_prefix(self, prefix: str):
        prefix = self._prepare_url(prefix)
        self._prefixes.append(prefix)

    def reduce_prefix(self):
        self._prefixes.pop()

    def reset(self):
        self._prefixes = []

    def on_finish(self):
        pass

    def debug(self, url: str, data: Any):
        if self._is_enabled_for(WriteLevel.DEBUG):
            self._handle_data_write_internal(url, data)

    def info(self, url: str, data: Any):
        if self._is_enabled_for(WriteLevel.INFO):
            self._handle_data_write_internal(url, data)

    def basic(self, url: str, data: Any):
        if self._is_enabled_for(WriteLevel.BASIC):
            self._handle_data_write_internal(url, data)


_HOOKS = []


def add_hook(_hook: Hook, /):
    if not isinstance(_hook, Hook):
        raise TypeError(f"callback must be of type {Hook}, not {type(_hook)}")
    _HOOKS.append(_hook)


def remove_hook(_hook: Hook, /):
    _HOOKS.remove(_hook)


def list_hooks() -> List[Hook]:
    return _HOOKS.copy()


def _apply_to_all(func_name, *args, **kwargs):
    for callback in _HOOKS:
        method = getattr(callback, func_name)
        method(*args, **kwargs)


debug = partial(_apply_to_all, "debug")
info = partial(_apply_to_all, "info")
basic = partial(_apply_to_all, "basic")
reset = partial(_apply_to_all, "reset")
on_finish = partial(_apply_to_all, "on_finish")
extend_prefix = partial(_apply_to_all, "extend_prefix")
reduce_prefix = partial(_apply_to_all, "reduce_prefix")


class prefix_extender(ContextDecorator):
    """
    Context manager that extends the prefix of the hook.

    Args:
        prefix: The prefix to extend the hooks prefix with.

    Example:
        >>> import explainer.util.hooks as hooks
        >>> with hooks.prefix_extender("ext1"):
        ...     hooks.info("test", "test_data") # info (url="ext1/test")

        >>> @hooks.prefix_extender("example/subexample")
        ... def test_func():
        ...     hooks.debug("test", "test_data") # debugging (url="example/subexample/test")
        ...     with hooks.prefix_extender("subsubexample"):
        ...         hooks.debug("test2", "test_data") # debugging (url="example/subexample/subsubexample/test2")
        ...
        >>> test_func()

    """

    def __init__(self, prefix: str):
        self._prefix = prefix

    def __enter__(self):
        extend_prefix(self._prefix)

    def __exit__(self, exc_type, exc_value, traceback):
        reduce_prefix()


class _Counter:
    START_INDEX = 1

    def __init__(self, enabled: bool):
        self._history = []
        self._enabled = enabled

    @staticmethod
    def _split_left(string: str, delimiter: str = "/"):
        split = string.split(delimiter)
        if len(split) == 1:
            return split[0], None
        else:
            return split[0], delimiter.join(split[1:])

    @staticmethod
    def _unique(iterable):
        seen = set()
        return [x for x in iterable if not (x in seen or seen.add(x))]

    @staticmethod
    def _check_is_leaf(x):
        return x[1] is None

    @staticmethod
    def _add_countings_to_url(url, history, debug=False):
        if debug:
            print(f"{url=} - {history=}")

        name, suffix = _Counter._split_left(url)
        assert name != "", f"Invalid url: {url}"

        split_history = [_Counter._split_left(x) for x in history]  # [(name, suffix)]

        # Collect all necessary information
        files, directories, directory_to_content = [], [], {}
        for entry in split_history:
            entry_name, entry_suffix = entry
            if _Counter._check_is_leaf(entry):
                files.append(entry_name)
            else:
                if entry_name not in directory_to_content:
                    directories.append(entry_name)
                    directory_to_content[entry_name] = []
                directory_to_content[entry_name].append(entry_suffix)

        if debug:
            print(f"{files=} - {directories=}")

        if _Counter._check_is_leaf((name, suffix)):
            return f"{len(files) + 1}_{name}"  # End of recursion

        try:
            idx = directories.index(name)
            content = directory_to_content[name]
            if debug:
                print(f"Found directory {name=}")
        except ValueError:  # name not in directories
            idx = len(directories)
            content = []
            if debug:
                print(f"New directory {name=}")

        _tmp = _Counter._add_countings_to_url(suffix, content)
        return f"{idx + 1}_{name}/{_tmp}"

    def __call__(self, url: str) -> str:
        extended_url = (
            self._add_countings_to_url(url, self._history) if self._enabled else url
        )

        self._history.append(url)

        return extended_url

    def reset(self):
        self._history = []


class DiskWriter(Hook):
    """
    Callback that writes to disk.

    Args:
        root_dir: The root directory to write the data to.
        use_counter: Whether to use a counter for the callback. Note: This cannot be changed after initialization. The counter is used to avoid overwriting files.
        **kwargs: Additional arguments to pass to the CallBack constructor.
    """

    def __init__(self, root_dir: os.PathLike, use_counter: bool = False, **kwargs):
        super().__init__(**kwargs)

        root_dir = Path(root_dir)
        assert root_dir.is_dir(), f"root_dir must be a directory, not {root_dir}"

        self._debugging_dir = root_dir / "debugging_log"
        self._debugging_dir.mkdir(exist_ok=True)

        self._dir = self._initialize_new_run_directory()

        self._counter = _Counter(use_counter)

    def _handle_data_write(self, url: str, data: _LazyCopy):
        fp = None  # type: Optional[Path]

        def _write_image(data, fp):
            import PIL.Image
            import numpy as np

            if isinstance(data, np.ndarray):
                data = PIL.Image.fromarray(data)
            if isinstance(data, PIL.Image.Image):
                data.save(fp.with_suffix(".png"), format="PNG")
            else:
                raise TypeError(
                    f"data must be of type PIL.Image.Image or np.ndarray, not {type(data)}"
                )

        def _write_segmentation(data, fp):
            import PIL.Image
            import numpy as np

            num_segments = int(data.max()) + 1
            np.random.seed(0)

            try:
                import distinctipy

                __color_map__ = distinctipy.get_colors(num_segments, n_attempts=250)
                __color_map__[0] = [0, 0, 0]  # black background
            except ImportError:
                __color_map__ = np.random.rand(num_segments, 3)

            seg_img = np.zeros(shape=(data.shape[0], data.shape[1], 3))

            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    seg_img[i, j] = __color_map__[data[i, j]]

            seg_img = seg_img * 255
            seg_img = np.array(seg_img, dtype=np.uint8)
            seg_img = PIL.Image.fromarray(seg_img)
            seg_img.save(fp.with_suffix(".png"), format="PNG")

        def _write_heatmap(data, fp):
            import io

            import PIL.Image

            try:
                import matplotlib.pyplot as plt
                import seaborn as sns
            except ImportError:
                print(f"Could not import matplotlib.pyplot or seaborn. Skipping {url=}")
                return

            plt.figure()
            sns.heatmap(data, cmap="plasma")  # viridis

            # Hide axis labels
            plt.xticks([])
            plt.yticks([])
            plt.axis("off")

            # Save the figure to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png", dpi=300)
            plt.close()
            buf.seek(0)

            image = PIL.Image.open(buf)
            image.save(fp.with_suffix(".png"), format="PNG")

        def _write_segmentation_and_relevancies(data, fp):
            import numpy as np

            segmentation = data["segmentation"]
            relevancies = data["relevancies"]

            heatmap = np.zeros(shape=segmentation.shape)

            for seg_id in relevancies:
                heatmap[segmentation == seg_id] = relevancies[seg_id]

            _write_heatmap(heatmap, fp)

        def _write_json(data, fp):
            import json

            with open(fp.with_suffix(".json"), "w") as f:
                json.dump(data, f, indent=4)

        def url_to_writer(url: str) -> Callable:
            if url.find("parts_extraction") != -1:
                if re.match(r"^.*image$", url):
                    print(f"<{self.__class__.__name__}> Writing image {url=}")
                    return _write_image

                if re.match(r"^.*xai_map$", url):
                    print(f"<{self.__class__.__name__}> Writing heatmap {url=}")
                    return _write_heatmap

                elif re.match(r"^.*segmentation_and_relevancies$", url):
                    print(
                        f"<{self.__class__.__name__}> Writing segmentation and relevancies {url=}"
                    )
                    return _write_segmentation_and_relevancies

                elif re.match(r"^.*segmentation$", url):
                    print(f"<{self.__class__.__name__}> Writing segmentation {url=}")
                    return _write_segmentation

                elif re.match(r"^.*relevancies$", url):
                    print(f"<{self.__class__.__name__}> Writing relevancies {url=}")
                    return _write_json
                elif re.match(r"^.*parts_image.*$", url):
                    print(f"<{self.__class__.__name__}> Writing parts image {url=}")
                    return _write_image
                elif re.match(r"^.*filter_parameters$", url):
                    print(
                        f"<{self.__class__.__name__}> Writing filter parameters {url=}"
                    )
                    return _write_json

            # Default if no match is found
            print(f"<{self.__class__.__name__}> Ignoring {url=}")
            return None

        writer_func = url_to_writer(url)
        if writer_func is not None:
            maybe_counted_url = self._counter(url)
            fp = self._dir / maybe_counted_url  # type: Path
            # print(f"<DebuggingCallBack> Target file={fp}")

            fp_dir = fp.parent
            fp_dir.mkdir(exist_ok=True, parents=True)

            data = data.data

            writer_func(data, fp)

    def _initialize_new_run_directory(self):
        next_id = len(list(self._debugging_dir.iterdir()))
        dir = self._debugging_dir / f"run_{next_id}"
        assert not dir.exists()

        return dir

    def reset(self):
        super().reset()
        self._dir = self._initialize_new_run_directory()
        self._counter.reset()


if __name__ == "__main__":
    add_hook(
        DiskWriter(
            root_dir=Path(__file__).parent.parent.parent / "output",
            level=WriteLevel.DEBUG,
            use_counter=True,
        )
    )

    for _ in range(2):
        debug("file", "data")
        debug("dir/file", "data")
        debug("file", "data")

        with prefix_extender("ext1"):
            info("file", "data")
            info("file", "data")
            info("file", "data")

        @prefix_extender("ext2")
        def test_func():
            basic("file", "data")
            basic("dir/file", "data")
            basic("file", "data")
            with prefix_extender("ext3"):
                debug("file", "data")
                debug("file", "data")
                debug("file", "data")

        test_func()

        print("*" * 50)
        reset()
