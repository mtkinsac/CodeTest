"""
tests/test_gandor_panel.py

Basic tests for the GandorPanel component.
"""

import pytest
from PyQt6.QtWidgets import QApplication
from gandor_panel import GandorPanel

@pytest.fixture(scope="session")
def app():
    return QApplication([])

def test_generate_response(app):
    panel = GandorPanel(personality="Witty")
    response = panel.generate_response("test message")
    assert "test message" in response
    witty_flavors = ["Well, that's quite a query!", "A clever move indeed!"]
    assert any(flavor in response for flavor in witty_flavors)
