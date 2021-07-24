"""
game.py - This file executes the game and manages its state.

Written by Amandeep Singh
"""

import os, sys, time, random
import battle, character, _map, shop

os.system("cls")

print("""
 _    _      _                             _         
| |  | |    | |                           | |        
| |  | | ___| | ___  ___  _ __ ___   ___  | |_  ___  
| |/\| |/ _ \ |/ __|/ _ \| '_ ` _ \ / _ \ | __|/ _ \ 
\  /\  /  __/ | (__| (_) | | | | | |  __/ | |_| (_) |
 \/  \/ \___|_|\___|\___/|_| |_| |_|\___|  \__|\___/

____________ _____  ______       _   _   _      _ 
| ___ \ ___ \  __ \ | ___ \     | | | | | |    | |
| |_/ / |_/ / |  \/ | |_/ / __ _| |_| |_| | ___| |
|    /|  __/| | __  | ___ \/ _` | __| __| |/ _ \ |
| |\ \| |   | |_\ \ | |_/ / (_| | |_| |_| |  __/_|
\_| \_\_|    \____/ \____/ \__,_|\__|\__|_|\___(_)

""")
time.sleep(5)

##########
### Settings for the Environment
##########

class Environment:
    def __init__(self, status, difficulty=None, mode=None):
        # Choosing Emoji Graphics
        print("Use Emoji Graphics? (y/n)")
        print('')
        self.EMOJI_GRAPHICS_MODE = self.input(['y','n']) == 'y'
        print("- Chose to{}use Emoji Graphics".format(' ' if self.EMOJI_GRAPHICS_MODE else " not "))
        print('')
        time.sleep(1)

        # Game Data
        self.status = status
        self.difficulty = self.set_difficulty() if not difficulty else difficulty
        self.mode = self.set_mode() if not mode else mode
        # self.mode = mode
        # if not self.mode: self.set_mode()
        self.battle_enemy_team = None
        self.game_won = False

        # Game Items
        self.player = Player(self)
        self.enemies = Enemies(self)
        self.shop = shop.Shop(self)
        self.map = _map.Map(self)

    # Get input according to allowed values and data type
    def input(self, allow=None, t=None):
        while True:
            try:
                inp = input(" Input: ")
                print('')
                if inp == '': raise ValueError
                elif inp in ['q',"quit"]: self.quit_game()

                if t == "int": inp = int(inp)
                elif (t == "bool") and (allow != None): return ((inp in allow) if (type(allow) is list) else (inp == allow))

                if (allow != None) and ((inp not in allow) if (type(allow) is list) else (inp != allow)): raise ValueError
                return inp
            except ValueError:
                print(" You must enter a valid input.")
            print('')

    def set_difficulty(self):
        os.system("cls")
        o = {
            'e': "Easy",
            'm': "Medium",
            'h': "Hard",
            'l': "Legendary",
            'i': "I'm the Knight Mode"
        }
        print("Please select a difficulty level:")
        for k in o:
            print(" {} - {}".format(k, o[k]))
        print('')
        self.difficulty = self.input(list(o.keys()))
        print(" - You have chosen the {} difficulty.".format(o[self.difficulty]))
        print('')
        time.sleep(1)
        return self.difficulty

    def set_mode(self):
        os.system("cls")
        print("Please select a side:")
        print(" 1. Good")
        print(" 2. Evil")
        print('')
        self.mode = self.input(list(range(1, 3)), "int")
        print("You have chosen the {} side.".format("Good" if (self.mode == 1) else "Evil"))
        print('')
        time.sleep(1)
        return self.mode

    def quit_game(self):
        print("Are you sure you want to quit the game? (y/n)")
        print('')
        inp = self.input(['y','n'])
        if inp == 'y': self.leave_game()

    def leave_game(self):
        print('')
        print("Thank you for playing RPG Battle.")
        print('')
        time.sleep(3)
        sys.exit()

class Team:
	def __init__(self, members=[], icon=None):
		self.members = members
		self.map = _map.MapInfo(icon)

##########
### Settings for the Player
##########

class Player(Team):

    def __init__(self, env, members_len=0):
        self.env = env
        self.members_len = self.set_members_len() if not members_len else members_len
        self.gold = 100
        self.inventory = []
        # Team
        Team.__init__(self, icon=('🤖' if self.env.EMOJI_GRAPHICS_MODE else '☆'))
        for i in range(self.members_len):
            os.system("cls")
            print("Choose Player", (i + 1))
            print('')
            p = character.make_character(self.env.mode, self.set_race(), self.set_name())
            self.members.append(p)
            print("You now have \"{}\" the {} on your team.".format(p.name, p.__class__.__name__))
            print('')
            time.sleep(1)
        # Records
        self.battles = 0
        self.wins = 0
        self.kills = 0

    def set_members_len(self):
        os.system("cls")
        print("How many Members will your team have? (1-5)")
        print('')
        self.members_len = self.env.input(list(range(1, 6)), "int")
        print("You have {} on your team.".format("{} players".format(self.members_len) if (self.members_len > 1) else "a player"))
        print('')
        time.sleep(1)
        return self.members_len

    def set_race(self):
        if self.env.mode == 2:             
            print("Playing as the Forces of Sauron.")
            print('')
            print("Please select your race:")
            print(" 1. Goblin")
            print(" 2. Orc")
            print(" 3. Uruk")
            print(" 4. Witch")
            print(" 5. Wizard")
        else:
            print("Playing as the Free Peoples of Middle Earth.")
            print('')
            print("Please select your race:")     
            print(" 1. Hobbit")
            print(" 2. Dwarf")
            print(" 3. Elf")
            print(" 4. Human")
            print(" 5. Wizard")
        print('')
        return self.env.input(list(range(1, 6)), "int")

    def set_name(self):
        print("Please enter your Character Name:")
        print('')
        return self.env.input()

    def show_inventory(self):
        print("You currently have {} Gold left".format(self.gold))
        print('')
        if len(self.inventory) == 0: print("You curently have nothing in your inventory.")
        else:
            s = a = ar = hp = mp = 0
            for i in self.inventory:
                if i.__class__.__name__ == "Sword": s += 1
                elif i.__class__.__name__ == "Axe": a += 1
                elif i.__class__.__name__ == "Armour": ar += 1
                elif i.__class__.__name__ == "HealthPotion": hp += 1
                elif i.__class__.__name__ == "ManaPotion": mp += 1

            if s > 0: print("- You have {} in your Inventory.".format("{} Swords".format(s) if (s > 1) else "a Sword"))
            if a > 0: print("- You have {} in your Inventory.".format("{} Axes".format(a) if (a > 1) else "an Axe"))
            if ar > 0: print("- You have {} in your Inventory.".format("{} Armours".format(ar) if (ar > 1) else "an Armour"))
            if hp > 0: print("- You have {} in your Inventory.".format("{} Health Potions".format(hp) if (hp > 1) else "a Health Potion"))
            if mp > 0: print("- You have {} in your Inventory.".format("{} Mana Potions".format(mp) if (mp > 1) else "a Mana Potion"))
        print('')

    def print_results(self):
        print("Game Over!", "You have {} the Game.".format("won" if (self.env.status == "GameWon") else "lost"))
        print("No. Battles: {0}".format(str(self.battles)))
        print("No. Wins: {0}".format(self.wins))
        print("No. Kills: {0}".format(self.kills))
        print("Success Rate (%): {0:.2f}%".format(float((self.wins * 100) / self.battles)))
        print("Avg. kills per battle: {0:.2f}".format(float(self.kills) / self.battles))
        print('')

##########
### Settings for the Enemies
##########

class Enemies:

	def __init__(self, env):
		self.env = env
		self.teams = self.create_enemies()

	def create_enemies(self):
		i = ['😈','🎃','👹','👾','👿'] if self.env.EMOJI_GRAPHICS_MODE else ['X','Y','Z','V','W']
		m = 1 if (self.env.mode == 2) else 2
		l = 2
		if self.env.difficulty == 'm': l = 3
		elif self.env.difficulty == 'h': l = 4
		elif self.env.difficulty == 'l': l = 4
		elif self.env.difficulty == 'i': l = 5
		ts = []

        # Team
		for y in range(0, l):
			t = u = []
			for x in range(0, int(l/2)):
				c = None
				while True:
					r = random.randint(1, l)
					n = character.possible_names(m, r)
					n = n[random.randint(0, len(n) - 1)]
					c = character.make_character(m, r, n)
					b = True
					for m in t:
						if m.__class__.__name__ == c.__class__.__name__ and m.name == c.name:
							b = False
							break
					if b: break
				t.append(c)
			ts.append(Team(t, i[y]))
		return ts

##########
### Running the game
##########

env = Environment(status="Map")
os.system("cls")
env.map.print_legends()

while True:
    os.system("cls")

    if env.status == "Map":
        env.map.printMap()
        env.map.player_move()
        if not env.map.battle_check():
            env.map.enemies_move()
            if env.map.battle_check():
                env.map.printMap()
                print("About to enter a Battle")
                time.sleep(2)
        else:
            env.map.printMap()
            print("About to enter a Battle")
            time.sleep(2)


    elif env.status == "Shop":
        env.shop.store()


    elif env.status == "Battle" and env.battle_enemy_team != None:
        encounter = battle.Battle(env)
        won, wins, kills, gold = encounter.play()
        env.player.battles += 1
        env.player.wins += wins
        env.player.kills += kills
        env.player.gold += gold

        for i, t in enumerate(env.enemies.teams):
            if (len(t.members) == 0):
                env.map.remove(t)
                env.enemies.teams.pop(i)

        if env.status == "Map":
            env.map.random_spawn(env.player)
            env.battle_enemy_team = None
        else:
            os.system("cls")
            if won: print("You have Won the Battle.")
            else: print("You have Lost the Battle and the Game.")
            print('')
            time.sleep(2)

            if len(env.enemies.teams) == 0: env.status = "GameWon"
            elif len(env.player.members) == 0: env.status = "GameLost"
            elif env.status == "Battle":
                env.status = "Map"
                env.battle_enemy_team = None


    elif env.status in ["GameWon","GameLost"]:
        env.player.print_results()
        print("Would you like to play the game again? (y/n)")
        print('')
        q = env.input(['y','n'])
        if q == 'n': env.leave_game()
        else: env = Environment(status="Map")