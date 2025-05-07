import os
from PIL import Image, ImageOps
import numpy as np
import torch

# JXL 相关代码已移除
# try:
#     import jxlpy
#     _jxl_available = True
#     print("nsfw_no Node: JXL library found, JXL support enabled.")
# except ImportError:
#     _jxl_available = False
#     print("nsfw_no Node: JXL library not found, JXL support disabled.")

class Folders:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
            },
            "optional": {
                "image_load_cap": ("INT", {"default": 0, "min": 0, "step": 1}),
                "start_index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "load_always": ("BOOLEAN", {"default": False, "label_on": "enabled", "label_off": "disabled"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("IMAGE", "MASK", "FILE PATH")
    OUTPUT_IS_LIST = (True, True, True)

    FUNCTION = "load_images"

    CATEGORY = "nsfw_No"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        if 'load_always' in kwargs and kwargs['load_always']:
            return float("NaN")
        else:
            return hash(frozenset(kwargs))

    def load_images(self, directory: str, image_load_cap: int = 0, start_index: int = 0, load_always=False):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' cannot be found.")
        dir_files = os.listdir(directory)
        if len(dir_files) == 0:
            raise FileNotFoundError(f"No files in directory '{directory}'.")

        # Filter files by extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        # if _jxl_available:  # <-- 使用我们定义的标志  <- REMOVE THIS LINE
        #     valid_extensions.extend('.jxl')           <- REMOVE THIS LINE
        dir_files = [f for f in dir_files if any(f.lower().endswith(ext) for ext in valid_extensions)]

        dir_files = sorted(dir_files)
        dir_files = [os.path.join(directory, x) for x in dir_files]

        # start at start_index
        dir_files = dir_files[start_index:]

        images = []
        masks = []
        file_paths = []

        limit_images = False
        if image_load_cap > 0:
            limit_images = True
        image_count = 0

        for image_path in dir_files:
            # 修正：检查是否是文件，如果不是文件（即是目录），则跳过
            if not os.path.isfile(image_path):
                print(f"Skipping directory or non-file: {image_path}") # 可选的调试信息
                continue
            
            if limit_images and image_count >= image_load_cap:
                break
            
            try:
                i = Image.open(image_path)
                i = ImageOps.exif_transpose(i)
                image = i.convert("RGB")
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]

                if 'A' in i.getbands():
                    mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                    mask = 1. - torch.from_numpy(mask)
                else:
                    mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

                images.append(image)
                masks.append(mask)
                file_paths.append(str(image_path))
                image_count += 1
            except Exception as e:
                print(f"Could not load image {image_path}: {e}") # 错误处理

        return (images, masks, file_paths)

NODE_CLASS_MAPPINGS = {
    "Folders": Folders
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Folders": "Folders"
}