"""Top-level package for nsfw_no."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """xiaodu"""
__email__ = "yinghanzi@gmail.com"
__version__ = "1.0.0"

# 从 nodes.py 导入并使用别名
from .src.nsfw_no.nodes import NODE_CLASS_MAPPINGS as NSFW_NO_CLASS_MAPPINGS
from .src.nsfw_no.nodes import NODE_DISPLAY_NAME_MAPPINGS as NSFW_NO_DISPLAY_NAME_MAPPINGS

# 从 Folders.py 导入并使用别名
from .src.nsfw_no.Folders import NODE_CLASS_MAPPINGS as FOLDERS_CLASS_MAPPINGS
from .src.nsfw_no.Folders import NODE_DISPLAY_NAME_MAPPINGS as FOLDERS_DISPLAY_NAME_MAPPINGS

# 合并 MAPPINGS
NODE_CLASS_MAPPINGS = {
    **NSFW_NO_CLASS_MAPPINGS,
    **FOLDERS_CLASS_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **NSFW_NO_DISPLAY_NAME_MAPPINGS,
    **FOLDERS_DISPLAY_NAME_MAPPINGS,
}

WEB_DIRECTORY = "./web"
