"""
shop.py - The shop class allows the player to modify its inventory.

Written by Amandeep Singh
"""

import os, time

from _map import MapInfo

class Shop:

    def __init__(self, env):
        self.env = env
        self.map = MapInfo('🛒' if self.env.EMOJI_GRAPHICS_MODE else 'S')

    def store(self):
        while self.env.status == "Shop":
            sword = Sword()
            axe = Axe()
            armour = Armour()
            healthPotion = HealthPotion()
            manaPotion = ManaPotion()

            os.system("cls")
            self.env.player.show_inventory()
            print("Please select the item")
            print('')
            print("1. Sword ({} Gold)".format(sword.price))
            print("2. Axe ({} Gold)".format(axe.price))
            print("3. Armour ({} Gold)".format(armour.price))
            print("4. Health Potion ({} Gold)".format(healthPotion.price))
            print("5. Mana Potion ({} Gold)".format(manaPotion.price))
            print("0. Leave Shop")
            print('')
            choice = self.env.input(list(range(0, 6)), "int")

            if choice == 1:
                if self.env.player.gold >= sword.price:
                    self.env.player.gold -= sword.price
                    print("You brought a Sword")
                    self.env.player.inventory.append(sword)
                else: print("Not enough Gold")
                print('')
                time.sleep(2)
            elif choice == 2:
                if self.env.player.gold >= axe.price:
                    self.env.player.gold -= axe.price
                    print("You brought an Axe")
                    self.env.player.inventory.append(axe)
                else: print("Not enough Gold")
                print('')
                time.sleep(2)
            elif choice == 3:
                if self.env.player.gold >= armour.price:
                    self.env.player.gold -= armour.price
                    print("You brought an Armour")
                    self.env.player.inventory.append(armour)
                else: print("Not enough Gold")
                print('')
                time.sleep(2)
            elif choice == 4:
                if self.env.player.gold >= healthPotion.price:
                    self.env.player.gold -= healthPotion.price
                    print("You brought a Health Potion")
                    self.env.player.inventory.append(healthPotion)
                else: print("Not enough Gold")
                print('')
                time.sleep(2)
            elif choice == 5:
                if self.env.player.gold >= manaPotion.price:
                    self.env.player.gold -= manaPotion.price
                    print("You brought a Mana Potion")
                    self.env.player.inventory.append(manaPotion)
                else: print("Not enough Gold")
                print('')
                time.sleep(2)
            else:
                self.env.status = "Map"
        print("You are leaving the Shop")
        print('')
        time.sleep(1)

class Sword:
	def __init__(self):
		self.price = 100
		self.damage = 10
		self.max_health = 50
		self.health = self.max_health

class Axe:
	def __init__(self):
		self.price = 150
		self.damage = 20
		self.max_health = 75
		self.health = self.max_health

class Armour:
	def __init__(self):
		self.price = 100
		self.max_health = 200
		self.health = self.max_health

class HealthPotion:
	def __init__(self):
		self.price = 75
		self.max_health = 50
		self.health = self.max_health

class ManaPotion:
	def __init__(self):
		self.price = 75
		self.max_mana = 75
		self.mana = self.max_mana