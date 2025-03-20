"""
dice_engine.py

Implements dice rolling functions, including inline notation parsing.
Supports "2d6+3" and exploding dice rolls.
"""

import random
import re

def parse_dice_notation(notation: str) -> dict:
    pattern = r'(?P<num>\d*)d(?P<sides>\d+)(?P<mod>[+-]\d+)?'
    match = re.fullmatch(pattern, notation.strip())
    if not match:
        raise ValueError(f"Invalid dice notation: {notation}")
    
    num = int(match.group("num")) if match.group("num") != "" else 1
    sides = int(match.group("sides"))
    mod_str = match.group("mod")
    modifier = int(mod_str) if mod_str else 0
    
    rolls = [random.randint(1, sides) for _ in range(num)]
    total = sum(rolls) + modifier
    return {
        "notation": notation,
        "rolls": rolls,
        "modifier": modifier,
        "total": total
    }

def roll_dice(sides: int, number: int = 1, modifier: int = 0, exploding: bool = False) -> dict:
    rolls = []
    for _ in range(number):
        roll = random.randint(1, sides)
        sub_rolls = [roll]
        if exploding:
            while roll == sides:
                roll = random.randint(1, sides)
                sub_rolls.append(roll)
        rolls.append(sum(sub_rolls))
    total = sum(rolls) + modifier
    return {
        "rolls": rolls,
        "modifier": modifier,
        "total": total
    }
