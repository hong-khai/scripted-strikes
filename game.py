import threading
import random
import time
from typing import Dict, List, Union

class Game:
    def __init__(self) -> None:
        from saveload import SaveLoad
        from tools import Tools

        self.balance: int = 250
        self.tanks: int = 0
        self.naval_cruisers: int = 0
        self.fighter_jets: int = 0
        self.army_bases: int = 0
        self.naval_bases: int = 0
        self.air_force_bases: int = 0
        self.wars: int = 0
        self.wars_won: int = 0
        self.wars_lost: int = 0
        self.add_dividend_interval: int = 0
        self.completed_intro: bool = False
        self._update = None
        self.tools: Tools = Tools()
        self.saveload: SaveLoad = SaveLoad()
        self.saveload.game = self
        self.separator: str = '-' * 30
        self.bases: List[str] = []
        self.redeemable: List[bool] = [True] * 5
        self.loans: List[int] = []

        self.empire_info: Dict[str, str] = {
            "name": self.tools.generate_new_empire(),
            "monarch": self.tools.generate_name()
        }

        self.vehicle_costs: Dict[str, Dict[str, Union[int, str]]] = {
            "a": {
                "cost": 100,
                "base": "army_bases",
                "type": "army"
            },
            "b": {
                "cost": 40,
                "base": "naval_bases",
                "type": "naval"
            },
            "c": {
                "cost": 200,
                "base": "air_force_bases",
                "type": "air force"
            }
        }

        self.base_costs: Dict[str, int] = {
            "a": {
                "cost": 10,
            },
            "b": {
                "cost": 25,
            },
            "c": {
                "cost": 50,
            }
        }

        self.shares: Dict[str, Dict[str, int]] = {
            "a": {
                "name": "Horizon Industries",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "b": {
                "name": "Summit Securities",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "c": {
                "name": "Crestline Holdings",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "d": {
                "name": "Cascade Ventures",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "e": {
                "name": "Panorama Industries",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "f": {
                "name": "Vanguard Corporation",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "g": {
                "name": "Apex Dynamics",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "h": {   
                "name": "Zenith Ventures",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "i": {   
                "name": "Crestview Holdings",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            },
            "j": {   
                "name": "Brick Corporation",
                "price": 0,
                "value": 0,
                "dividend_yield": 0,
                "amount": 0
            }
        }

        self.external_empires: Dict[str, Dict[str, str]] = {
            "a": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "b": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "c": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "d": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "e": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "f": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "g": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "h": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "i": {
                "name": self.tools.generate_new_empire(),
                "rating": "neutral"
            },
            "j": {
                "name":  self.tools.generate_new_empire(),
                "rating": "neutral"
            }
        }

    @property
    def update(self):
        if self._update is None:
            self._update = Update(self)
        return self._update

    def make_payment(self, price: int, number_needed: int, vehicle_type: str) -> None:
        if self.balance >= price:
            self.balance -= price
            setattr(self, vehicle_type + 's', getattr(self, vehicle_type + 's') + number_needed)
        else:
            print("You do not have enough money!")

    def show_empire_info(self) -> None:
        print(f"""Empire Name: {self.empire_info['name']}
Empire Monarch: {self.empire_info['monarch']}
Empire Treasury: ${self.balance}
Wars Fought: {self.wars}
Wars Won: {self.wars_won}
Wars Lost: {self.wars_lost}
Tanks: {self.tanks}
Naval Cruisers: {self.naval_cruisers}
Fighter Jets: {self.fighter_jets}
Army Bases: {self.army_bases}
Naval Bases: {self.naval_bases}
Air Force Bases: {self.air_force_bases}""")

    def edit_empire(self) -> None:
        new_empire_name: str = input("Enter your new empire name (leave blank to skip): ")
        new_empire_monarch: str = input("Enter your new monarch name (leave blank to skip): ")
        if new_empire_name:
            self.empire_info["name"] = new_empire_name
        if new_empire_monarch:
            self.empire_info["monarch"] = new_empire_monarch

    def send_aid_to_empire(self, alphic_empire_choice, alphic_aid_choice) -> None:
        if alphic_empire_choice not in self.external_empires:
            print("Not a valid option.")
            return
        
        empire_aiding: str = self.external_empires[alphic_empire_choice]["name"]
        if alphic_aid_choice == "a":
            try:
                aid_amount = int(input(f"How much money do you want to send to {empire_aiding}?"))
                if aid_amount < 1:
                    print("Negative numbers and zero are not allowed.")
                    return
            except ValueError:
                print("Invalid number.")
                return
            
            if self.balance < aid_amount:
                print("Not enough money.")
                return
            
            self.balance -= aid_amount
            print(f"Sucessfully aided {empire_aiding}.")

            self.improve_rating(alphic_empire_choice)
        elif alphic_aid_choice == "b":
            vehicle_aiding: str = input(f"Which vehicle do you want to send to {empire_aiding}? (tank, naval cruiser or fighter jet)").strip().lower()
            if vehicle_aiding not in ["tank", "naval cruiser", "fighter jet"]:
                print("Invalid vehicle type! Please choose from 'tank', 'naval cruiser', or 'fighter jet'.")
                return
            
            try:
                amount_giving = int(input(f"How many {vehicle_aiding}s do you want to send to {empire_aiding}?"))
                if amount_giving < 1:
                    print("Negative numbers and zero are not allowed.")
                    return
            except ValueError:
                print("Invalid number.")
            
            if vehicle_aiding == "naval cruiser":
                read_var: str = "naval_cruiser"
            if vehicle_aiding == "fighter jet":
                read_var: str = "fighter_jet"

            vehicle_attr = getattr(self, read_var + "s")

            if vehicle_attr < amount_giving:
                print(f"Not enough {vehicle_aiding}s.")
                return
            
            setattr(self, vehicle_attr, vehicle_attr - amount_giving)
            
            self.improve_rating(alphic_empire_choice)
        else:
            print("Not a valid option.")

    def improve_rating(self, alphic_empire_choice) -> None:
        if self.external_empires[alphic_empire_choice]["rating"] == "enemy" and random.randint(0, 1):
            self.external_empires[alphic_empire_choice]["rating"] = "neutral"
        elif self.external_empires[alphic_empire_choice]["rating"] == "neutral":
            self.external_empires[alphic_empire_choice]["rating"] = "ally"

    def print_all_empires_with_prompt(self, prompt) -> None:
        print(prompt)
        for empire in self.external_empires:
            print(f"{empire}) {self.external_empires[empire]['name']}")

    def declare_war_on(self, alphic_empire_choice) -> None:
        if alphic_empire_choice not in self.external_empires:
            print("Not a valid option.")
            return
        
        print(f"Declaring war on {self.external_empires[alphic_empire_choice]['name']}...")
        time.sleep(1)

        self.external_empires[alphic_empire_choice]["rating"] = "enemy"

        print(f"""{self.external_empires[alphic_empire_choice]['name']} has sent vehicles towards your territory.
Do you want to defend or offend?""")
        
        invasion_response = input().strip().lower()
        if invasion_response not in ["defend", "offend"]:
            print("Not a valid option.")
            return
        
        self.vehicles_into_war = []
        self.ask_if_vehicle_needed("tanks")
        self.ask_if_vehicle_needed("naval cruisers")
        self.ask_if_vehicle_needed("fighter jets")
        
        total_vehicles = 0
        for vehicle in self.vehicles_into_war:
            print(f"How many {vehicle} do you want to send?")
            try:
                amount_of_vehicles = int(input().strip())
            except ValueError:
                print("Invalid number.")
                return
            
            if amount_of_vehicles < 1:
                print("Negative numbers and zero are not allowed.")
                return
            
            read_var = f"{vehicle.replace(' ', '_')}"
            vehicle_attr = getattr(self, read_var + "s", 0)
            
            if vehicle_attr < amount_of_vehicles:
                print(f"Not enough {vehicle}")
                return
            
            total_vehicles += amount_of_vehicles

        enemy_fleet = random.randint(10, 500)
        time.sleep(1)

        if total_vehicles > enemy_fleet and random.randint(0, 1):
            print("You won!")
            self.wars_won += 1
        elif random.randint(0, 1):
            print("You won!")
            self.wars_won += 1
        else:
            print("You lost.")
            self.wars_lost += 1
            
    def ask_if_vehicle_needed(self, vehicle_type) -> None:
        print(f"Do you want to send {vehicle_type}? (answer yes or no)")
        vehicle_needed = input().strip().lower()
        if vehicle_needed == "yes":
            self.vehicles_into_war.append(vehicle_type)
    
    def buy_vehicle(self, vehicle_type: str, number_needed: int) -> None:
        if number_needed < 1:
            print("Negative numbers and zero are not allowed.")
            return

        vehicle_type = vehicle_type.strip().lower()

        vehicle_mapping = {
            "tank": "a",
            "naval cruiser": "b",
            "fighter jet": "c"
        }

        key = vehicle_mapping.get(vehicle_type)

        if not key:
            print("Invalid vehicle type! Please choose from 'tank', 'naval cruiser', or 'fighter jet'.")
            return

        cost_info = self.vehicle_costs.get(key)
        if not cost_info:
            print("Error retrieving vehicle cost information.")
            return

        base_name = cost_info["base"]
        if getattr(self, base_name) < 1:
            print(f"No {cost_info['type']} base available.")
            return

        price = cost_info["cost"] * number_needed
        if self.balance < price:
            print("You do not have enough money!")
            return

        filtered_vehicle_type: str = vehicle_type
        if vehicle_type == "fighter jet": filtered_vehicle_type: str = "fighter_jet"
        if vehicle_type == "naval cruiser": filtered_vehicle_type: str = "naval_cruiser"

        current_count = getattr(self, filtered_vehicle_type + 's')
        setattr(self, filtered_vehicle_type + 's', current_count + number_needed)
        self.balance -= price

        print(f"Successfully bought {number_needed} {vehicle_type}(s).")

    def get_loan(self, loan_price) -> None:
        if random.randint(0, 1):
            print("Your loan has been accepted.")
            self.balance += loan_price
            self.loans.append(loan_price)
        else:
            print("Your loan has been declined.")

    def pay_loan(self) -> None:
        for step, loan in enumerate(self.loans, 1):
            print(f"Loan ID: {step} | Amount: {loan}$")
        
        try:
            loan_paying = int(input("Which loan would you like to pay (enter Loan ID): "))
            if loan_paying < 1:
                print("Negative numbers and zero are not allowed.")
                return
        except ValueError:
            print("Invalid number.")
            return
        
        if loan_paying not in self.loans:
            print("Invalid Loan ID.")
            return
        
        if self.balance < self.loans[loan_paying]:
            print("Not enough money.")
            return
        
        self.balance -= self.loans[loan_paying]
        print(f"Loan with ID{loan_paying} paid sucessfully.")

    def purchase_shares(self, alphic_shares_choice: str) -> None:
        share: str = self.shares[alphic_shares_choice]["name"]
        price_per_share: int = self.shares[alphic_shares_choice]["price"]

        print(f"""The price of one share in {share} is ${price_per_share}
Enter the amount of shares you want to buy. To calculate the price, type in "calculator".""")
        
        shares_choice: str = input().strip().lower()
        if shares_choice == "calculator":
            try:
                shares_to_calculate = int(input("Enter the amount of shares you want to calculate the price of: "))
                if shares_to_calculate < 1:
                    print("Negative numbers and zero are not allowed.")
                    return
            except ValueError:
                print("Invalid number.")
                return

            if shares_to_calculate < 1:
                print("Negative numbers and zero are not allowed.")
                return

            cost_of_shares: int = shares_to_calculate * price_per_share
            print(f"The price of {shares_to_calculate} shares in {share} is ${cost_of_shares}.")

        else:
            try:
                cost_of_shares: int = int(shares_choice) * price_per_share
            except ValueError:
                print("Invalid number.")
                return
            
            if self.balance < cost_of_shares:
                print("Not enough money!")
                return
            
            self.balance -= cost_of_shares
            self.shares[alphic_shares_choice]["amount"] += int(shares_choice)

            print(f"Sucessfully bought {shares_choice} shares in {share}.")
    
    def sell_shares(self, alphic_shares_choice: str) -> None:
        try:
            shares_to_sell = int(input("Enter the amount of shares you want to sell: "))
            if shares_to_sell < 1:
                print("Negative numbers and zero are not allowed.")
                return
        except ValueError:
            print("Invalid number.")
            return
        
        if self.shares[alphic_shares_choice]["amount"] < shares_to_sell:
            print("Not enough shares to sell.")
            return
        self.balance += self.shares[alphic_shares_choice]["value"] * shares_to_sell
    
    def view_share_market(self) -> None:
        print(f"""{self.separator}
Share Market
{self.separator}""")
        for share in self.shares:
            share_name: str = self.shares[share]["name"]
            print(f"""Price of one share in {share_name}: ${self.shares[share]['price']}
Value of one share in {share_name}: ${self.shares[share]['value']}
Dividend yield of {share_name}: {self.shares[share]["dividend_yield"] * 100}%
{self.separator}""")
    
    def print_share_choices(self) -> None:
        for share in self.shares:
            print(f"{share}) {self.shares[share]['name']}")
        
    def create_base(self, alphic_base_type: str) -> None:
        if alphic_base_type == "a":
            base_name: str = "Fort " + self.tools.generate_place()
            increment_var: str = "army_bases"
        elif alphic_base_type == "b":
            base_name: str = "Naval Base " + self.tools.generate_place()
            increment_var: str = "naval_bases"
        elif alphic_base_type == "c":
            base_name: str = self.tools.generate_place() + " Air Force Base"
            increment_var: str = "air_force_bases"
        else:
            print("Not a valid option.")
            return
        
        if self.balance < self.base_costs[alphic_base_type]["cost"]:
            print("Not enough money.")
            return
        
        self.balance -= self.base_costs[alphic_base_type]["cost"]
        self.bases.append(self.check_base_exists(base_name))

        current_count = getattr(self, increment_var)
        setattr(self, increment_var, current_count + 1)
        print(f"Sucessfully created a base.")

    def check_base_exists(self, base_name) -> str:
        extra_base_name: int = 1
        while base_name in self.bases:
            base_name = f"{base_name} {extra_base_name}"
            extra_base_name += 1
        return base_name

    def print_all_bases(self) -> None:
        print("Bases:")
        for base in self.bases:
            print(base)

    def rename_base(self) -> None:
        self.print_all_bases()
        old_name: str = input("Enter the name of the base you want to rename: ")
        if old_name in self.bases:
            new_name: str = input("Enter the new name for the base: ")
            if new_name:
                index: int = self.bases.index(old_name)
                self.bases[index] = new_name
                print(f"Base renamed from '{old_name}' to '{new_name}'.")
            else:
                print("New name cannot be empty.")
        else:
            print("Base not found.")

    def load_game_from_file(self) -> None:
        if len(self.game_info) < 2:
            print("Error finding saved game.")
        else:
            if self.saveload.load_variables(self.game_info[1]):
                print("Game loaded successfully.")
                self.start_game_loop()
    
    def get_game_info(self) -> None:
        with open("game_info.txt", "r") as file:
            self.game_info = file.readlines()
    
    def complete_save_procedure(self) -> None:
        try:
            with open("game_info.txt", "r") as file:
                self.game_info = file.readlines()
                if len(self.game_info) < 2:
                    any_saved_game: bool = False
        except FileNotFoundError:
            any_saved_game: bool = False

        print("""How do you want to save your game?
a) Get game key
b) Save game in file""")
        save_choice: str = input().strip().lower()

        if save_choice == "a":
            print(f"Game Key: {self.saveload.generate_key()}. Save it securely.")
        elif save_choice == "b":
            if any_saved_game == True:
                print("""You already have a saved game. Do you want to overwrite it?
a) Yes
b) No""")
        overwrite_saved = input("You already have a saved game. Do you want to overwrite it?").strip().lower()
        if overwrite_saved == "a":
            self.write_game_key()
        elif overwrite_saved == "b":
            print(f"Game Key: {self.saveload.generate_key()}. Save it securely.")
        else:
            print("Not a valid option.")
            
    def start_game(self) -> None:
        if self.completed_intro == False:
            self.completed_intro: bool = True
            new_status = input("Are you new?")
            if new_status == "yes":
                self.game_intro()

        print(f"""{self.separator}
Main Menu:
a) Tutorial
b) Create Game
c) Load Game
d) Exit""")

        while True:
            choice: str = input("Enter your choice: ").strip().lower()

            if choice == "a":
                self.display_tutorial()
            elif choice == "b":
                print("New game created.")
                with open("game_info.txt", 'a+') as file:
                    file.seek(0)
                    self.game_info = file.read()
                    if not self.game_info:
                        file.write("\n")
                self.start_game_loop()
            elif choice == "c":
                print("""How do you want to load your game?
a) Game key
b) Saved key in file""")
                load_choice = input().strip().lower()
                if load_choice == "a":
                    key: str = input("Enter your game key: ").strip()
                    if self.saveload.load_variables(key):
                        print("Game loaded successfully.")
                        self.start_game_loop()
                    else:
                        print("Failed to load game. Please check your key and try again.")
                elif load_choice == "b":
                    try:
                        self.load_game_from_file()
                    except AttributeError:
                        self.get_game_info()
                        self.load_game_from_file()
            elif choice == "d":
                print("Exiting game...")
                break
            else:
                print("Invalid option!")

    def slow_print(self, text, delay=0.05) -> None:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def game_intro(self) -> None:
        messages = [
            ("Welcome to Scripted Strikes\n", 0.5),
            ("In the year 3035, the world is a battleground of power and strategy.", 1),
            ("You are a monarch in this dystopian future, where resources are scarce and every decision could mean the difference between victory and defeat.", 2),
            ("Your mission is to build your empire, forge alliances, and lead your forces to dominate the war-torn lands.", 2),
            ("The future of your empire lies in your hands. It is time you start your journey.", 1)
        ]
        
        for text, delay in messages:
            self.slow_print(text)
            time.sleep(delay)

    def display_tutorial(self) -> None:
        print(f"""{self.separator}
[OVERVIEW]
Buy vehicles to earn money.
Tanks cost $40 each. Naval cruisers cost $100 each. Fighter jets cost $200 each.
To purchase vehicles, create bases.
Army bases cost $10 each. Naval bases cost $25 each. Air Force bases cost $50 each.
The more bases you have, the more money you make!
Get loans if needed.
[COMMANDS]
/empireinfo - View empire info
/editempire - Edit empire name and monarch
/savegame - Save your game
/declarewar - Declare war against an empire
/sendaid - Send aid to an empire
/empirestatus - View all empires' status (enemy, neutral or ally)
/buyvehicle - Purchase vehicles
/getloan - Get a loan
/payloan - Pay a loan
/buyshares - Purchase shares
/sellshares - Sell your shares
/sharemarket - View the share market
/createbase - Create a new base
/bases - View all bases
/renamebase - Rename a base
/achievements - View achievements and rewards
/redeem - Redeem a passkey
/? or /help - Display tutorial
/exit - Exit game or main menu
[WARNINGS]
Do not modify game_info.txt as it may corrupt game data.
{self.separator}""")
        
    def start_game_loop(self) -> None:
        threading.Thread(target=self.update.update_game, daemon=True).start()

        while True:
            command: str = input("Command: ").strip().lower()

            if command == "/empireinfo":
                self.show_empire_info()
            elif command == "/editempire":
                self.edit_empire()
            elif command == "/savegame":
                self.complete_save_procedure()
            elif command == "/declarewar":
                self.print_all_empires_with_prompt("Which empire do you want to declare war on?")
                empire_declaring_war_on = input().strip().lower()
                
                self.declare_war_on(empire_declaring_war_on)
            elif command == "/sendaid":
                print("""What kind of aid do you want to send?
a) Monetary aid
b) Vehicle aid""")
                aid_type: str = input().strip().lower()
                self.print_all_empires_with_prompt("Which empire do you want to send the aid to?")

                empire_receiving_aid: str = input().strip().lower()

                self.send_aid_to_empire(empire_receiving_aid, aid_type)
            elif command == "/empirestatus":
                for empire in self.external_empires:
                    print(f"Empire Name: {self.external_empires[empire]['name']} | Rating: {self.external_empires[empire]['rating']}")
            elif command == "/buyvehicle":
                print("Pick a vehicle to buy. (tank, naval cruiser or fighter jet)")
                vehicle_type: str = input().strip().lower()
                try:
                    number_needed = int(input("How many? "))
                    self.buy_vehicle(vehicle_type, number_needed)
                except ValueError:
                    print("Invalid number.")
            elif command == "/getloan":
                try:
                    loan_needed = int(input("How much do you want to borrow? "))
                    if number_needed < 1:
                        print("Negative numbers and zero are not allowed.")
                        return
                except ValueError:
                    print("Invalid number.")
                self.get_loan(loan_needed)
            elif command == "/payloan":
                self.pay_loan()
            elif command == "/buyshares":
                print("Which share do you want to invest in?")
                self.print_share_choices()
                new_share: str = input().strip().lower()
                self.purchase_shares(new_share)
            elif command == "/sellshares":
                print("Which share do you want to sell?")
                self.print_share_choices()
                share_to_sell: str = input().strip().lower()
                self.sell_shares(share_to_sell)
            elif command == "/sharemarket":
                self.view_share_market()
            elif command == "/createbase":
                print("""What type of base to you want to create?
a) Army
b) Navy
c) Air Force""")
                new_base: str = input().strip().lower()
                self.create_base(new_base)
            elif command == "/bases":
                self.print_all_bases()
            elif command == "/renamebase":
                self.rename_base()
            elif command == "/exit":
                print("""Exit to:
a) Main Menu
b) Exit game""")
                exit_action: str = input().strip().lower()
                if exit_action:
                    print("You are about to exit your game. Please make sure to save your game.")
                    self.complete_save_procedure()
                if exit_action == "a":
                    print("Returning to main menu...")
                    self.__init__()
                    self.start_game()
                elif exit_action == "b":
                    print("Exiting game...")
                    break
                else:
                    print("Invalid option.")
            elif command == "/achievements":
                self.check_achievements()
            elif command == "/redeem":
                self.redeem_passkey()
            elif command in ["/?", "/help"]:
                self.display_tutorial()
            elif not command:
                continue
            else:
                print("Unknown command.")

    def check_achievements(self) -> None:
        if self.balance > int(self.high_score) and self.redeemable[1]:
            with open("game_info.txt", "w") as file:
                file.write(str(self.balance))
            print("Achievement: Beaten high score! Passkey: t5m7pk8")
        elif self.balance % 2500 == 0 and self.redeemable[2]:
            print("Achievement: $2500 earned! Passkey: ut6gp9s")
        elif len(self.loans) == 1 and self.redeemable[3]:
            print("Achievement: First loan! Passkey: po31u5b")
        elif self.tanks + self.naval_cruisers + self.fighter_jets == 20 and self.redeemable[4]:
            print("Achievement: 20 vehicles! Passkey: 5rop05b")
        else:
            print("No achievements found.")

    def redeem_passkey(self) -> None:
        passkey = input("Enter passkey: ").strip()
        rewards = {
            "t5m7pk8": ("2 tanks", lambda: setattr(self, 'tanks', self.tanks + 2)),
            "ut6gp9s": ("$500", lambda: setattr(self, 'balance', self.balance + 500)),
            "po31u5b": ("$250", lambda: setattr(self, 'balance', self.balance + 250)),
            "5rop05b": ("10 naval cruisers", lambda: setattr(self, 'naval_cruisers', self.naval_cruisers + 10))
        }
        reward = rewards.get(passkey)
        if reward:
            if passkey == "t5m7pk8" and self.army_bases == 0:
                print("No army base available.")
                return
            if passkey == "5rop05b" and self.naval_bases == 0:
                print("No naval base available.")
                return
            reward[1]()
            print(f"Redeemed prize of {reward[0]}.")
            self.redeemable[list(rewards.keys()).index(passkey) + 1] = False
        else:
            print("Invalid passkey.")

    def write_game_key(self) -> None:
        try:
            with open("game_info.txt", "r") as file:
                pass
        except FileNotFoundError:
            self.game_info = [''] * 2

        if len(self.game_info) < 2:
            self.game_info.extend([''] * (2 - len(self.game_info)))

        self.game_info[1] = self.saveload.generate_key() + '\n'

        with open("game_info.txt", 'w') as file:
            file.writelines(self.game_info)

class Update:
    def __init__(self, game) -> None:
        self.game = game

    def update_inventory(self) -> None:
        balance_delta: int = 0
        rareness = sum(random.randint(0, 1) for _ in range(3))

        if rareness == 3:
            for empire in self.game.external_empires.values():
                if empire["rating"] == "ally":
                    if random.randint(0, 1):
                        aid_actions = {
                            "money": lambda: random.randint(100, 1000),
                            "tanks": lambda: setattr(self.game, "tanks", self.game.tanks + random.randint(1, 5)),
                            "cruisers": lambda: setattr(self.game, "cruisers", self.game.naval_cruisers + random.randint(1, 5)),
                            "jets": lambda: setattr(self.game, "jets", self.game.fighter_jets + random.randint(1, 5))
                        }
        
                        type_of_aid = random.choice(list(aid_actions.keys()))
                        if type_of_aid == "money":
                            balance_delta += aid_actions[type_of_aid]()
                        else:
                            aid_actions[type_of_aid]()
                            
        self.game.balance -= len(self.game.loans) * 100

        self.game.add_dividend_interval += 1
        if self.game.add_dividend_interval == 100:
            for share in self.game.shares:
                total_investment_value: int = self.game.shares[share]["amount"] * self.game.shares[share]["price"]
                balance_delta += total_investment_value * self.game.shares[share]["dividend_yield"]
        
        self.game.balance = int(self.game.balance)
        self.game.balance += balance_delta

    def update_high_scores(self) -> None:
        try:
            self.game.get_game_info()

            high_scores_str: str = self.game.game_info[0]
            self.game.high_score = high_scores_str if high_scores_str else 0
        except FileNotFoundError:
            self.game.high_score = 0
            with open("game_info.txt", "w") as file:
                file.write("0\n")

        if str(self.game.balance) > self.game.high_score:
            self.game.high_score = self.game.balance
            with open("game_info.txt", "w") as file:
                file.write(str(self.game.high_score) + "\n")
    
    def update_share_values(self) -> None:
        for share in self.game.shares:
            self.game.shares[share]["value"] = random.randint(-500, 500)

    def update_share_prices(self) -> None:
        for share in self.game.shares:
            self.game.shares[share]["price"] = self.game.shares[share]["value"] + random.randint(-250, 250)
            if self.game.shares[share]["price"] < 1:
                self.game.shares[share]["price"] = random.randint(0, abs(self.game.shares[share]["price"]))

    def update_share_dividend_yield(self) -> None:
        for share in self.game.shares:
            self.game.shares[share]["dividend_yield"] = round(random.uniform(0, 0.05), 3)

    def update_game(self) -> None:
        while True:
            self.update_share_values()
            self.update_share_prices()
            self.update_share_dividend_yield()
            self.update_inventory()
            self.update_high_scores()
            
            time.sleep(3)

game = Game()
update = game.update 
            
