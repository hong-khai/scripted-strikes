import json
from typing import Optional
from game import Game

class SaveLoad:
    def __init__(self) -> None:
        self.game: Optional[Game] = None

    def generate_key(self) -> str:
        data = {
            "balance": self.game.balance,
            "tanks": self.game.tanks,
            "naval_cruisers": self.game.naval_cruisers,
            "fighter_jets": self.game.fighter_jets,
            "army_bases": self.game.army_bases,
            "naval_bases": self.game.naval_bases,
            "air_force_bases": self.game.air_force_bases,
            "bases": self.game.bases,
            "redeemable": self.game.redeemable,
            "empire_info": self.game.empire_info,
            "shares": self.game.shares,
            "loans": self.game.loans,
            "external_empires": self.game.external_empires
        }
        return json.dumps(data)

    def load_variables(self, key: str) -> bool:
        try:
            data = json.loads(key)
            self.game.balance = data["balance"]
            self.game.tanks = data["tanks"]
            self.game.naval_cruisers = data["naval_cruisers"]
            self.game.fighter_jets = data["fighter_jets"]
            self.game.army_bases = data["army_bases"]
            self.game.naval_bases = data["naval_bases"]
            self.game.air_force_bases = data["air_force_bases"]
            self.game.bases = data["bases"]
            self.game.redeemable = data["redeemable"]
            self.game.empire_info = data["empire_info"]
            self.game.shares = data["shares"]
            self.game.loans = data["loans"]
            self.game.external_empires = data["external_empires"]
            return True
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading variables: {e}")
            return False
