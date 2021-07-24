"""
_map.py - The map class manages the characters travelling across the map.

Written by Amandeep Singh
"""

import os, time, random

class MapInfo:

	def __init__(self, icon=None, y=0, x=0):
		self.icon = icon
		self.y = y
		self.x = x
		self.last_step = None

class Map:

    def __init__(self, env):
        self.env = env
        self.height = 15
        self.width = 15
        if self.env.difficulty == 'm': self.width *= 2
        elif self.env.difficulty == 'h': self.width *= 3
        elif self.env.difficulty == 'l': self.width *= 4
        elif self.env.difficulty == 'i': self.width *= 5
        self.PATH = '  ' if self.env.EMOJI_GRAPHICS_MODE else ' '
        self.WALL = '██' if self.env.EMOJI_GRAPHICS_MODE else '#'
        self.TREE = '🌲' if self.env.EMOJI_GRAPHICS_MODE else '*'
        self.ROCK = '🗿' if self.env.EMOJI_GRAPHICS_MODE else 'O'
        self.FIRE = '🔥' if self.env.EMOJI_GRAPHICS_MODE else 'F'
        self.GOLD = '💰' if self.env.EMOJI_GRAPHICS_MODE else 'G'
        self.map = None
        self.generate_random_map()

    def generate_random_map(self):
        self.map = [[self.WALL] * self.width]
 
        for y in range(1, self.height - 1):
            row = [self.WALL]
            for x in range(1, self.width - 1):
                r = random.randint(0, 10)
                if random.randint(0, 50) == 25: row.append(self.GOLD)
                elif r == 3: row.append(self.TREE)
                elif r == 8: row.append(self.ROCK)
                elif r == 10: row.append(self.FIRE)
                else: row.append(self.PATH)
            row.append(self.WALL)
            self.map.append(row)
        self.map.append([self.WALL] * self.width)

        self.random_spawn(self.env.shop)
        
        for t in self.env.enemies.teams:
            self.random_spawn(t)
        
        self.random_spawn(self.env.player)

    def printMap(self):
        os.system("cls")
        for i in self.map:
            print(''.join(i))
        print('')

    def player_move(self):
        if (self.env.status != "Map"): return

        inp = 'l'
        while inp == 'l':
            inp = self.env.input(['w','a','s','d','l'])
            if inp == 'l':
                self.print_legends()
                self.printMap()

        next_step = None
        new_y = self.env.player.map.y
        new_x = self.env.player.map.x

        if (inp == 'w'):
            new_y -= 1
            next_step = self.map[new_y][self.env.player.map.x]
        elif (inp == 'd'):
            new_x += 1
            next_step = self.map[self.env.player.map.y][new_x]
        elif (inp == 's'):
            new_y += 1
            next_step = self.map[new_y][self.env.player.map.x]
        else:
            new_x -= 1
            next_step = self.map[self.env.player.map.y][new_x]

        if (next_step not in [self.WALL, self.TREE, self.ROCK, self.FIRE] + [t.map.icon for t in self.env.enemies.teams]):
            if next_step == self.GOLD:
                self.env.player.gold += 50
                print("You landed on gold and obtained 50 gold.")
                print("Total gold:", self.env.player.gold)
                print('')
                time.sleep(1)
            elif next_step == self.env.shop.map.icon:
                self.env.status = "Shop"
                print("You are entering the Shop")
                print('')
                time.sleep(1)
                return
            self.env.player.map.last_step = inp
            self.map[self.env.player.map.y][self.env.player.map.x] = self.PATH
            self.env.player.map.y = new_y
            self.env.player.map.x = new_x
            self.map[self.env.player.map.y][self.env.player.map.x] = self.env.player.map.icon
        else:
            if next_step == self.WALL: print("You bumped into a Wall")
            elif next_step == self.TREE: print("You bumped into a Tree")
            elif next_step == self.ROCK: print("You bumped into a Giant Rock")
            elif next_step == self.FIRE:
                print("You touched Fire. {} lost 5 health.".format("All the players" if (len(self.env.player.members) > 1) else "Your player"))
                print('')
                time.sleep(1)
                for i, m in enumerate(self.env.player.members):
                    m.health -= 5
                    if m.health <= 0: self.env.player.members.pop(i)
                if len(self.env.player.members) == 0:
                    self.env.status = "GameLost"
                    print("The players died from touching Fire.")
            print('')
            time.sleep(1)

    def enemies_move(self):
        if (self.env.status != "Map"): return
        for t in self.env.enemies.teams:
            counter = 0
            direction = 'y' if (self.env.player.map.last_step in ['w','s']) else 'x'
            new_y = t.map.y
            new_x = t.map.x
            while (counter < 2):
                if (direction == 'y'):
                    if t.map.y > self.env.player.map.y: new_y -= 1
                    elif t.map.y < self.env.player.map.y: new_y += 1
                else:
                    if t.map.x > self.env.player.map.x: new_x -= 1
                    elif t.map.x < self.env.player.map.x: new_x += 1

                if (self.map[new_y][new_x] == self.PATH):
                    self.map[t.map.y][t.map.x] = self.PATH
                    t.map.y = new_y
                    t.map.x = new_x
                    self.map[t.map.y][t.map.x] = t.map.icon
                    break
                else:
                    counter += 1
                    direction = 'y' if (direction == 'x') else 'x'

    def battle_check(self):
        if (self.env.status != "Map"): return False
        for t in self.env.enemies.teams:
            if (t.map.icon in [
                self.map[self.env.player.map.y - 1][self.env.player.map.x],
                self.map[self.env.player.map.y][self.env.player.map.x + 1],
                self.map[self.env.player.map.y + 1][self.env.player.map.x],
                self.map[self.env.player.map.y][self.env.player.map.x - 1]
            ]):
                self.env.status = "Battle"
                self.env.battle_enemy_team = t
                return True
        return False

    def random_spawn(self, of):
        if of.map.y not in [0, None] and of.map.x not in [0, None]: self.map[of.map.y][of.map.x] = self.PATH
        y = x = 0
        while self.map[y][x] != self.PATH:
            y = random.randint(2, self.height - 2)
            x = random.randint(2, self.width - 2)
        of.map.y = y
        of.map.x = x
        self.map[of.map.y][of.map.x] = of.map.icon

    def remove(self, of):
        self.map[of.map.y][of.map.x] = self.PATH
    
    def print_legends(self):
        os.system("cls")
        print("\n----- MAP LEGENDS -----")
        print("Player  - {}".format(self.env.player.map.icon))
        print("Enemies - {}".format(" | ".join([x.map.icon for x in self.env.enemies.teams])))
        print("Shop    - {}".format(self.env.shop.map.icon))
        print("Gold    - {}".format(self.GOLD))
        print("Fire    - {} (All team members will suffer 5 damage)".format(self.FIRE))
        print("Tree    - {}".format(self.TREE))
        print("Rock    - {}".format(self.ROCK))
        print("Wall    - {}".format(self.WALL))
        print('')
        print("Use Keys w, a, s, d to move Player")
        print("Press l to show Map Legends")
        print('')
        inp = input(" Press enter to continue... ")