"""Top-level package for nsfw_no."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """xiaodu"""
__email__ = "yinghanzi@gmail.com"
__version__ = "1.0.0"

from .src.nsfw_no.nodes import NODE_CLASS_MAPPINGS
from .src.nsfw_no.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
