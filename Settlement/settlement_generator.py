"""
settlement_generator.py

Generates a procedural settlement (village, town, or city) with basic attributes.
This is a base scaffolding for our procedural settlement generator.
"""

import random

class SettlementGenerator:
    def __init__(self):
        self.types = ["Village", "Town", "City"]
        self.names = {
            "Village": ["Greenfield", "Oakvale", "Riverside"],
            "Town": ["Briarwood", "Stonebridge", "Mapleton"],
            "City": ["Highgate", "Ironhold", "Silverport"]
        }
        self.populations = {
            "Village": (100, 500),
            "Town": (500, 5000),
            "City": (5000, 50000)
        }

    def generate_settlement(self) -> dict:
        """
        Generate a random settlement with type, name, population, and a brief description.
        """
        settlement_type = random.choice(self.types)
        name = random.choice(self.names[settlement_type])
        pop_range = self.populations[settlement_type]
        population = random.randint(*pop_range)
        description = f"A {settlement_type.lower()} known for its vibrant community and local traditions."
        # More detailed features can be added later.
        settlement = {
            "type": settlement_type,
            "name": name,
            "population": population,
            "description": description
        }
        return settlement

if __name__ == '__main__':
    generator = SettlementGenerator()
    settlement = generator.generate_settlement()
    print("Generated Settlement:")
    for key, value in settlement.items():
        print(f"{key}: {value}")
