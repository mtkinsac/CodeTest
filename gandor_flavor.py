"""
gandor_flavor.py

Provides a centralized flavor generator for Gandor's responses.
Based on the selected personality (e.g., "Wise", "Grumpy", etc.), it returns a random flavor phrase.
"""

import random

def get_flavor(personality: str) -> str:
    """
    Return a random flavor phrase based on the given personality.
    
    Args:
        personality (str): The personality type (e.g., "Wise", "Grumpy", "Mysterious", "Witty").
        
    Returns:
        str: A flavor phrase.
    """
    styles = {
        "Wise": ["Contemplate deeply.", "The ancient scrolls whisper truths."],
        "Grumpy": ["Not again...", "I've had enough of these inquiries."],
        "Mysterious": ["The mists conceal many secrets.", "There is more than meets the eye."],
        "Witty": ["Well, that's quite a query!", "A clever move indeed!"]
    }
    return random.choice(styles.get(personality, ["Hmm..."]))
