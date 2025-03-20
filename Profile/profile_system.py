"""
profile_system.py

A basic system for managing player profiles within a campaign.
Profiles include player name, character details, and preferences.
"""

import json
import os

class ProfileSystem:
    def __init__(self, profiles_file="profile/profiles.json"):
        self.profiles_file = profiles_file
        self.profiles = self.load_profiles()

    def load_profiles(self):
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading profiles: {e}")
        return {}

    def save_profiles(self):
        try:
            with open(self.profiles_file, "w", encoding="utf-8") as f:
                json.dump(self.profiles, f, indent=4)
        except Exception as e:
            print(f"Error saving profiles: {e}")

    def add_profile(self, player_id: str, profile_data: dict):
        self.profiles[player_id] = profile_data
        self.save_profiles()

    def get_profile(self, player_id: str) -> dict:
        return self.profiles.get(player_id, {})

if __name__ == '__main__':
    ps = ProfileSystem()
    # Example usage:
    ps.add_profile("player1", {"name": "Aria", "class": "Ranger", "level": 5})
    print(ps.get_profile("player1"))
