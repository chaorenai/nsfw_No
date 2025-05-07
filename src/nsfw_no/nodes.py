from PIL import Image
from transformers import pipeline
import torchvision.transforms as T
import torch
import numpy as np

_classifier_pipeline = None


def tensor2pil(image_tensor):
    image = image_tensor.permute(2, 0, 1) if image_tensor.shape[2] == 3 else image_tensor
    image = image.cpu().detach()
    image = T.ToPILImage()(image)
    return image


def pil2tensor(image_pil):
    image = image_pil.convert("RGB")
    tensor = T.ToTensor()(image)
    return tensor.permute(1, 2, 0)


class nsfw_No:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "score": ("FLOAT", {
                    "default": 0.9,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001,
                    "display": "nsfw_threshold"
                }),
                "backup_image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "nsfw_No"

    def run(self, image, score, backup_image):
        global _classifier_pipeline

        if _classifier_pipeline is None:
            _classifier_pipeline = pipeline("image-classification", model="Falconsai/nsfw_image_detection")

        out_images = []

        for i, img_tensor in enumerate(image):
            pil_image = tensor2pil(img_tensor)
            result = _classifier_pipeline(pil_image)
            is_nsfw = any(r["label"] == "nsfw" and r["score"] > score for r in result)

            if is_nsfw:
                # 直接返回 backup_image 原图和尺寸
                out_tensor = backup_image[0]
            else:
                out_tensor = img_tensor

            out_images.append(out_tensor)

        return (torch.stack(out_images),)


NODE_CLASS_MAPPINGS = {
    "nsfw_No": nsfw_No
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "nsfw_No": "nsfw_No"
}
