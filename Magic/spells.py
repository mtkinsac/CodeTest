"""
spell.py

Defines the Spell class, representing a single spell in Blackstone Codex.
This model includes attributes such as name, cost, tags, keywords, effects, school, and rarity.
"""

class Spell:
    def __init__(self, name: str, cost: int, tags: list, keywords: list,
                 effects: str, school: str, rarity: str):
        self.name = name
        self.cost = cost
        self.tags = tags
        self.keywords = keywords
        self.effects = effects
        self.school = school
        self.rarity = rarity

    def __str__(self):
        return f"{self.name} (Cost: {self.cost}, School: {self.school}, Rarity: {self.rarity})"

    def get_details(self) -> str:
        """
        Return a detailed description of the spell.
        """
        details = (
            f"Name: {self.name}\n"
            f"Cost: {self.cost}\n"
            f"School: {self.school}\n"
            f"Rarity: {self.rarity}\n"
            f"Tags: {', '.join(self.tags)}\n"
            f"Keywords: {', '.join(self.keywords)}\n"
            f"Effects: {self.effects}"
        )
        return details
