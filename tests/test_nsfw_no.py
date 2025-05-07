#!/usr/bin/env python

"""Tests for `nsfw_no` package."""

import pytest
from src.nsfw_no.nodes import nsfw_No

@pytest.fixture
def example_node():
    """Fixture to create an nsfw_No node instance."""
    return nsfw_No()

def test_example_node_initialization(example_node):
    """Test that the node can be instantiated."""
    assert isinstance(example_node, nsfw_No)

def test_return_types():
    """Test the node's metadata."""
    assert nsfw_No.RETURN_TYPES == ("IMAGE",)
    assert nsfw_No.FUNCTION == "run"
    assert nsfw_No.CATEGORY == "nsfw_No"