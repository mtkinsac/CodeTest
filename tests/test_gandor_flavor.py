"""
tests/test_gandor_flavor.py

Basic unit tests for the gandor_flavor module.
"""

import pytest
from gandor_flavor import get_flavor

def test_get_flavor_wise():
    flavor = get_flavor("Wise")
    assert isinstance(flavor, str)
    assert flavor in ["Contemplate deeply.", "The ancient scrolls whisper truths."]

def test_get_flavor_invalid():
    flavor = get_flavor("NonExistent")
    assert flavor == "Hmm..."
