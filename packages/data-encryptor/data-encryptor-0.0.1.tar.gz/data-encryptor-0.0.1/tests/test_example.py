"""Unit test example."""
from encryptor import my_module


def test_greet():
    """Test the greet function."""
    assert len(my_module.greet(name="John")) > 0
