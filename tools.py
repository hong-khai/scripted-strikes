import random
from typing import List

class Tools:
    def __init__(self) -> None:
        self.used_empire_names: List[str] = []
        self.first_names: List[str] = [
            "Emma", "Olivia", "Ava", "Isabella", "Sophia",
            "Liam", "Noah", "William", "James", "Logan"
        ]
        self.last_names: List[str] = [
            "Smith", "Johnson", "Williams", "Brown", "Jones",
            "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"
        ]
        self.place_adjectives: List[str] = [
            'Mystic', 'Forgotten', 'Enchanted', 'Lost', 'Ancient',
            'Whispering', 'Ethereal', 'Silent', 'Celestial', 'Hidden',
            'Glowing', 'Secret', 'Twilight', 'Emerald', 'Frozen',
            'Divine', 'Moonlit', 'Golden', 'Sapphire', 'Starlit'
        ]
        self.place_nouns: List[str] = [
            'Valley', 'Forest', 'Island', 'Mountains', 'Canyon',
            'Labyrinth', 'Cave', 'Grove', 'Lake', 'Ruins',
            'Waterfall', 'Citadel', 'Garden', 'Desert', 'Oasis',
            'Temple', 'Castle', 'Peak', 'Spires', 'Meadow'
        ]
        self.empire_prefixes: List[str] = [
            "Galactic", "Celestial", "Stellar", "Cosmic",
            "Universal", "Interstellar"
        ]
        self.empire_suffixes: List[str] = [
            "Empire", "Dominion", "Federation", "Union",
            "Consortium", "Alliance"
        ]

    def generate_name(self) -> str:
        return f"{random.choice(self.first_names)} {random.choice(self.last_names)}"

    def generate_place(self) -> str:
        return f"{random.choice(self.place_adjectives)} {random.choice(self.place_nouns)}"

    def generate_new_empire(self) -> str:
        while True:
            new_empire = f"{random.choice(self.empire_prefixes)} {random.choice(self.empire_suffixes)}"
            if new_empire not in self.used_empire_names:
                self.used_empire_names.append(new_empire)
                return new_empire
