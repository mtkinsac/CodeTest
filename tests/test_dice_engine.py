"""
tests/test_dice_engine.py

Unit tests for the dice_engine module.
"""

import pytest
from dice_engine import parse_dice_notation, roll_dice

def test_parse_dice_notation_basic():
    result = parse_dice_notation("2d6+3")
    assert "rolls" in result
    assert isinstance(result["rolls"], list)
    assert result["modifier"] == 3
    assert result["total"] == sum(result["rolls"]) + 3

def test_parse_dice_notation_default_number():
    result = parse_dice_notation("d20")
    assert len(result["rolls"]) == 1

def test_invalid_notation():
    with pytest.raises(ValueError):
        parse_dice_notation("invalid")

def test_roll_dice_exploding():
    calls = []
    def fake_randint(a, b):
        calls.append(1)
        if len(calls) == 1:
            return b
        return a
    original_randint = __import__("random").randint
    __import__("random").randint = fake_randint
    try:
        result = roll_dice(6, number=1, modifier=0, exploding=True)
        assert result["total"] == 7
    finally:
        __import__("random").randint = original_randint
