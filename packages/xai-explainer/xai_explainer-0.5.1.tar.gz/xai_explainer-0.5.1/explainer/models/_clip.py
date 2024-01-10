import torch
from transformers import CLIPModel, CLIPProcessor

from explainer.datasets import CustomCLIP

from ._api import ModelType, get_model_dir, register_model
from .base import ClassificationModel

__all__ = [
    "CLIP",
]


class CLIP(ClassificationModel):
    def __init__(self, model, preprocess, promts, classes, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.processor = preprocess
        self.prompts = promts
        self.classes = classes

    def predict(self, image):
        inputs = self.processor(
            text=self.prompts, images=image, return_tensors="pt", padding=True
        )
        inputs = inputs.to(self.device)
        outputs = self.model(**inputs)
        logits_per_image = (
            outputs.logits_per_image
        )  # this is the image-text similarity score
        probs = logits_per_image.softmax(
            dim=1
        )  # we can take the softmax to get the label probabilities

        # Get the label with the highest probability
        _, predicted_label = torch.max(probs, dim=1)
        predicted_label = predicted_label.item()

        return [predicted_label]


@register_model(
    model_type=ModelType.PARTS_MODEL,
    weights_url=None,
    dataset=CustomCLIP,
    name="clip_parts_model",
    config={
        "num_classes": CustomCLIP.num_classes(),
    },
)
def clip_parts_model(**kwargs):
    model = CLIPModel.from_pretrained(
        "openai/clip-vit-large-patch14", cache_dir=get_model_dir()
    )
    processor = CLIPProcessor.from_pretrained(
        "openai/clip-vit-large-patch14", cache_dir=get_model_dir()
    )

    return CLIP(
        model, processor, CustomCLIP.class_texts(), CustomCLIP.classes(), **kwargs
    )
