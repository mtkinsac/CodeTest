"""
magic_loader.py

Loads spell definitions from JSON files located in a designated spells directory.
Creates Spell objects defined in spell.py.
"""

import os
import json
from spell import Spell  # Ensure this import works with your project structure.

class SpellLoader:
    def __init__(self, spells_dir="magic/spells"):
        self.spells_dir = spells_dir
        self.spells = []

    def load_spells(self):
        """
        Scan the spells directory for JSON files and load each as a Spell object.
        """
        if not os.path.exists(self.spells_dir):
            print(f"Spells directory '{self.spells_dir}' does not exist.")
            return

        for filename in os.listdir(self.spells_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.spells_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        spell = Spell(
                            name=data.get("name", "Unnamed Spell"),
                            cost=data.get("cost", 0),
                            tags=data.get("tags", []),
                            keywords=data.get("keywords", []),
                            effects=data.get("effects", ""),
                            school=data.get("school", "General"),
                            rarity=data.get("rarity", "Common")
                        )
                        self.spells.append(spell)
                except Exception as e:
                    print(f"Error loading spell from {filename}: {e}")
        print(f"Loaded {len(self.spells)} spells.")

    def get_spells(self):
        return self.spells

if __name__ == '__main__':
    loader = SpellLoader()
    loader.load_spells()
    for spell in loader.get_spells():
        print(spell.get_details())
