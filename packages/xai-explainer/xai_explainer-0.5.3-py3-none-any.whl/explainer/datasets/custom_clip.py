from PIL import Image
from torch import Tensor

from explainer.datasets.base import ClassificationDataset

from ._api import register_dataset

__all__ = ["CustomCLIP"]


@register_dataset
class CustomCLIP(ClassificationDataset):
    def transform(img: Image.Image) -> Tensor:
        raise NotImplementedError

    def classes():
        return [
            "car",
            "car_trunk",
            "car_windshield",
            "car_wheel",
            "truck",
            "bus",
            "motorcycle",
            "bicycle",
            "crosswalk",
            "road",
            "building",
            "tree",
            "traffic_light",
            "traffic_sign",
            "crash_barrier",
            "google_logo",
        ]

    def class_texts():
        return list(
            map(lambda x: f"an image of a {x.replace('_', ' ')}", CustomCLIP.classes())
        )
