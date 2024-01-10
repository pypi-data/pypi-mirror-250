import importlib.resources

from PIL import Image
from torch import Tensor

from explainer.datasets.base import ClassificationDataset

from ._api import register_dataset

__all__ = ["ImageNet"]


def _init_classes():
    files = importlib.resources.files("explainer.resources.datasets")
    content = files.joinpath("imagenet_classes.txt").read_text(encoding="utf-8")

    classes = content.splitlines()
    classes = [x.strip() for x in classes]
    classes = [x.replace(" ", "_") for x in classes]

    return classes


_CLASSES = _init_classes()


@register_dataset
class ImageNet(ClassificationDataset):
    def transform(img: Image.Image) -> Tensor:
        raise NotImplementedError

    def classes():
        return _CLASSES
