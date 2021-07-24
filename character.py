"""
character.py - Class definition for RPG Characters

Modified by Amandeep Singh
Originally written by Bruce Fuda for Intermediate Programming
Modified with permission by Edwin Griffin
"""

import time, random

"""
Define the attributes and methods available to all characters in the Character
Superclass. All characters will be able to access these abilities.
Note: All classes should inherit the 'object' class.
"""

def possible_names(mode, race):
	if mode == 2:
		if race == 1: return ["Azog","Druid","Gorkil"]
		elif race == 2: return ["Gholug","Grishnakh","Shagrat","Sharku"]
		elif race == 3: return ["Bolg","Lurtz"]
		elif race == 4: return ["Bavmorda","Gorbag"]
		else: return ["Alatar","Gandalf","Saruman"]
	else:
		if race == 1: return ["Frodo","Meriadoc","Peregrin","Rumble","Sam"]
		elif race == 2: return ["Durin","Gimli"]
		elif race == 3: return ["Blitz","Legolas"]
		elif race == 4: return ["Aragorn","Boromir","Eowyn","Faramir"]
		else: return ["Alatar","Gandalf","Saruman"]

def make_character(mode, race, name):
    if mode == 2:
        if race == 1: return Goblin(name)
        elif race == 2: return Orc(name)
        elif race == 3: return Uruk(name)
        elif race == 4: return Witch(name)
        else: return Wizard(name)
    else:
        if race == 1: return Hobbit(name)
        elif race == 2: return Dwarf(name)
        elif race == 3: return Elf(name)
        elif race == 4: return Human(name)
        else: return Wizard(name)

class Character:

    def __init__(self, name):
        self.name = name
        self.attack_mod = 1.0
        self.defense_mod = 1.0
        self.freeze = 0

        self.weapon = None
        self.armour = None

    def frozen(self):
        if self.freeze > 0:
            self.freeze -= 1
            print(self.name, "is still frozen and cannot make a move.")
            print('')
            time.sleep(1)
            return True
        return False

    def set_stance(self, c):
        if c == 'a':
            self.attack_mod = 1.3
            self.defense_mod = 0.6
            print(self.name, "chose Aggressive stance.")
        elif c == 'd':
            self.attack_mod = 0.6    
            self.defense_mod = 1.3
            print(self.name, "chose Defensive stance.")
        else:
            self.attack_mod = 1.0
            self.defense_mod = 1.0
            print(self.name, "chose Balanced stance.")
        print('')
        time.sleep(1)

    ##########
    ### Attack and Defense
    ##########

    def move(self, target):
        if self.health < (self.max_health/2):
            self.set_stance('d')
            # self.use_potion()
            return True
        return False

    def attack_target(self, target):
        if self.frozen(): return (False, 0)

        roll = random.randint(0, 20)
        hit = int(roll * self.attack_mod * self.attack)

        if self.weapon != None:
            hit += self.weapon.damage
            self.weapon.health -= 5
            if self.weapon.health <= 0: self.weapon = None

        print("{} attacks {}.".format(self.name, target.name))
        print('')
        time.sleep(1)

        roll = random.randint(1, 10)
        if roll == 10:
            hit *= 2
            print("- {} scores a critical hit! Double damage inflicted!!".format(self.name))
            print('')
            time.sleep(1)

        kill, new_gold = target.defend_attack(hit)
        
        time.sleep(1)
        
        if kill:
            print("- {} has killed {}.".format(self.name, target.name))
            print('')
            time.sleep(1)

        return (kill, new_gold)

    def defend_attack(self, att_damage):

        roll = random.randint(1, 20)
        block = int(roll * self.defense_mod * self.defense)

        if self.armour != None: block += 10
            
        block_roll = random.randint(1, 10)
        if block_roll == 10:
            print("- {} successfully blocks the attack!".format(self.name))
            block = att_damage
            time.sleep(1)
    
        damage = att_damage - block
        if damage < 0: damage = 0

        if self.shield > 0 and damage != 0:
            if damage <= self.shield:
                print("- {}'s Shield absorbs {} damage.".format(self.name, damage))
                time.sleep(1)
                self.shield -= damage
                damage = 0
            else:
                print("- {}'s Shield absorbs {} damage.".format(self.name, self.shield))
                time.sleep(1)
                print("- The Shield is now completely broken.")
                time.sleep(1)
                damage -= self.shield
                self.shield = 0

        if self.armour != None and damage != 0:
            if damage <= self.armour.health:
                print("- {}'s Armour absorbs {} damage.".format(self.name, damage))
                time.sleep(1)
                self.armour.health -= damage
                damage = 0
            else:
                print("- {}'s Armour absorbs {} damage.".format(self.name, self.armour))
                time.sleep(1)
                print("- The Armour is now completely broken.")
                time.sleep(1)
                damage -= self.armour.health
                self.armour = None

        print("- {} suffers {} damage!".format(self.name, damage))
        self.health -= damage
        time.sleep(1)

        new_gold = int(damage/2)
        death = False

        if self.health <= 0:
            self.health = 0
            new_gold *= 2
            print("- {} is dead!".format(self.name))
            time.sleep(2)
            death = True
        else:
            print("- {} has {} health left.".format(self.name, self.health))
            time.sleep(1)

        print('')
        return (death, new_gold)


    ##########
    ### Using Magic
    ##########

    def cast_spell(self, c, target=None):
        if c == "fb" and target != None: return self.cast_fireball(target)
        elif c == 's': self.cast_shield()
        elif c == 'm' and target != None: self.cast_mana_drain(target)
        elif c == 'f' and target != None: self.cast_freeze(target)

    def cast_fireball(self, target):        
        if self.frozen() or (self.mana < 10) or (target == None): return (False, 0)

        self.mana -= 10
        print("{} casts Fireball on {}!".format(self.name, target.name))
        print('')
        time.sleep(1)
        
        roll = random.randint(1, 10)
        defense_roll = random.randint(1, 10)
        damage = int(roll * self.magic) - int(defense_roll * target.resistance)
        if damage < 0: damage = 0

        kill, new_gold = target.defend_attack(damage)

        return (kill, new_gold)

    def cast_shield(self):
        if self.frozen() or (self.mana < 20): return

        self.mana -= 20
        print(self.name, "casts Shield!")
        print('')
        time.sleep(1)
        if self.shield <= self.max_shield: self.shield = self.max_shield
        print("- {} is shielded from the next {} damage.".format(self.name, self.shield))
        print('')
        time.sleep(1)

    def cast_mana_drain(self, target):
        if self.frozen() or (target == None): return
        elif target.mana == 0:
            print("The target has no mana to drain.")
            print('')
            time.sleep(1)
            return

        print("{} casts Mana Drain on {}!".format(self.name, target.name))
        print('')
        time.sleep(1)

        if target.mana >= 20: drain = 20
        else: drain = target.mana
        print("- {} drains {} mana from {}.".format(self.name, drain, target.name))
        time.sleep(1)
        
        target.mana -= drain
        self.mana += drain
        
        if target.mana <= 0:
            target.mana = 0
            print("- {}'s mana has been exhausted!".format(target.name))
        else:
            print("- {} has {} mana left.".format(target.name, target.mana))
        print('')
        time.sleep(1)

    def cast_freeze(self, target):
        if self.frozen() or (target == None): return

        if (self.mana < 20): return
        self.mana -= 20
        print("{} casts Freeze on {}!".format(self.name, target.name))
        print('')
        time.sleep(1)
        self.freeze += 2
        print("- {} is now frozen.".format(target.name))
        print('')
        time.sleep(1)

    ##########
    ### Inventory
    ##########

    def useInventory(self, env, inventory):        
        if self.frozen(): return

        print("Inventory:")
        op = []
        s = a = ar = hp = mp = 0
        for i in inventory:
            if i.__class__.__name__ == "Sword": s += 1
            elif i.__class__.__name__ == "Axe": a += 1
            elif i.__class__.__name__ == "Armour": ar += 1
            elif i.__class__.__name__ == "HealthPotion": hp += 1
            elif i.__class__.__name__ == "ManaPotion": mp += 1
        
        if s > 0 or (self.weapon != None and self.weapon.__class__.__name__ == "Sword"):
            op.append("Sword")
            print("{}. {}".format(len(op), ("Unequip the Sword" if (self.weapon != None) else ("Equip a Sword ({} in the inventory)".format(s)))))
        if a > 0 or (self.weapon != None and self.weapon.__class__.__name__ == "Axe"):
            op.append("Axe")
            print("{}. {}".format(len(op), ("Unequip the Axe" if (self.weapon != None) else ("Equip an Axe ({} in the inventory)".format(a)))))
        if ar > 0 or (self.weapon != None and self.armour.__class__.__name__ == "Armour"):
            op.append("Armour")
            print("{}. {}".format(len(op), ("Unequip the Armour" if (self.weapon != None) else ("Equip an Armour ({} in the inventory)".format(ar)))))
        if hp > 0:
            op.append("HealthPotion")
            print("{}. Use a Health Potion ({} in the inventory)".format(len(op), hp))
        if mp > 0:
            op.append("ManaPotion")
            print("{}. Use a Mana Potion ({} in the inventory)".format(len(op), mp))
        print("0. Return")
        print('')

        inp = env.input(list(range(0, len(op) + 1)), "int")

        if inp == 0: None
        elif op[inp - 1] == "Sword":
            if self.weapon != None and self.weapon.__class__.__name__ == "Sword":
                inventory.append(self.weapon)
                self.weapon = None
                print("The Sword has been unequipped.")
            else:
                for i, it in enumerate(inventory):
                    if it.__class__.__name__ == "Sword":
                        self.weapon = inventory.pop(i)
                        break
                print("The Sword has been equipped.")
            print('')
        elif op[inp - 1] == "Axe":
            if self.weapon != None and self.weapon.__class__.__name__ == "Axe":
                inventory.append(self.weapon)
                self.weapon = None
                print("The Axe has been unequipped.")
            else:
                for i, it in enumerate(inventory):
                    if it.__class__.__name__ == "Axe":
                        self.weapon = inventory.pop(i)
                        break
                print("The Axe has been equipped.")
            print('')
        elif op[inp - 1] == "Armour":
            if self.weapon != None and self.weapon.__class__.__name__ == "Armour":
                inventory.append(self.weapon)
                self.weapon = None
                print("The Armour has been unequipped.")
            else:
                for i, it in enumerate(inventory):
                    if it.__class__.__name__ == "Armour":
                        self.weapon = inventory.pop(i)
                        break
                print("The Armour has been equipped.")
            print('')
        elif op[inp - 1] == "HealthPotion":
            print("How many Health Potions you want to use?")
            print('')
            num = env.input(list(range(0, hp)), "int")
            if num > 0:
                rh = self.max_health - self.health
                if rh > 0:
                    for i, it in enumerate(inventory):
                        if it.__class__.__name__ == "HealthPotion":
                            if it.health <= rh:
                                self.health += it.health
                                inventory.pop(i)
                                num -= 1
                            else:
                                h = it.health - rh
                                self.health += h
                                it.health -= h
                            if self.health == self.max_health: break
                            elif num == 0: break
                    print("This player has used {} numbers of Health Potions.".format(num))
                else: print("The player's Health is already at max.")
            else: print("No Health Potions were used.")
            print('')
        elif op[inp - 1] == "ManaPotion":
            print("How many Mana Potions you want to use?")
            print('')
            num = env.input(list(range(1, mp)), "int")
            if num > 0:
                rm = self.max_mana - self.mana
                if rm > 0:
                    for i, it in enumerate(inventory):
                        if it.__class__.__name__ == "ManaPotion":
                            if it.mana <= rm:
                                self.mana += it.mana
                                inventory.pop(i)
                                num -= 1
                            else:
                                h = it.mana - rm
                                self.mana += h
                                it.mana -= h
                            if self.mana == self.max_mana: break
                            elif num == 0: break
                    print("This player has used {} numbers of Mana Potions.".format(num))
                else: print("The player's Mana is already at max.")
            else: print("No Mana Potions were used.")
            print('')
  
    def print_status(self, gold):
        print(self.name + "'s Status:")
        time.sleep(0.5)

        if self.attack_mod == 1.3 and self.defense_mod == 0.6: print(" Is on Aggressive stance")
        elif self.attack_mod == 0.6 and self.defense_mod == 1.3: print(" Is on Defensive stance")
        else: print(" Is on Balanced stance")
        time.sleep(0.5)

        print(" Gold:", gold)
        time.sleep(0.5)

        p = int((self.health * 100) / self.max_health)
        print(" Health: |{}{}| {} ({}%)".format(('#' * int(p * 0.1)), (' ' * (10 - int(p * 0.1))), self.health, p))
        time.sleep(0.5)

        if self.max_mana > 0:
            p = int((self.mana * 100) / self.max_mana)
            print(" Mana:   |{}{}| {} ({}%)".format(('#' * int(p * 0.1)), (' ' * (10 - int(p * 0.1))), self.mana, p))
            time.sleep(0.5)

        if self.shield > 0:
            p = int((self.shield * 100) / self.max_shield)
            print(" Shield: |{}{}| {} ({}%)".format(('#' * int(p * 0.1)), (' ' * (10 - int(p * 0.1))), self.shield, p))
            time.sleep(0.5)

        if self.armour != None and self.armour.health > 0:
            p = int((self.armour.health * 100) / self.armour.max_health)
            print(" Armour: |{}{}| {} ({}%)".format(('#' * int(p * 0.1)), (' ' * (10 - int(p * 0.1))), self.armour.health, p))
            time.sleep(0.5)

        if self.weapon != None and self.weapon.health > 0:
            p = int((self.weapon.health * 100) / self.weapon.max_health)
            print('')
            print(" {}: |{}{}| {} ({}%)".format(self.weapon.__class__.__name__, ('#' * int(p * 0.1)), (' ' * (10 - int(p * 0.1))), self.weapon.health, p))
            time.sleep(0.5)

        print('')
        time.sleep(0.5)

    def reset(self):
        self.health = self.max_health
        self.mana = self.max_mana
        self.weapon = None
        self.armour = None
    
"""
Define the attributes specific to each of the Character Subclasses.
This identifies the differences between each race.
"""

class Dwarf(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 300
        self.max_mana = 30
        self.max_shield = 50
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = 0
        self.attack = 9
        self.defense = 6
        self.magic = 4
        self.resistance = 5

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            self.set_stance('a')
            return self.attack_target(target)
        return (False, 0)
    
class Elf(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 300
        self.max_mana = 60
        self.max_shield = 100
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = self.max_shield
        self.attack = 6
        self.defense = 8
        self.magic = 8
        self.resistance = 8

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            self.set_stance('d')
            if self.shield == 0 and self.mana >= 20: self.cast_spell('s')
            else: return self.attack_target(target)
        return (False, 0)

class Goblin(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 100
        self.max_mana = 0
        self.max_shield = 100
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = 0
        self.attack = 3
        self.defense = 3
        self.magic = 0
        self.resistance = 0

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            self.set_stance('d')
            return self.attack_target(target)
        return (False, 0)

class Hobbit(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 250
        self.max_mana = 40
        self.max_shield = 50
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = 0
        self.attack = 3
        self.defense = 9
        self.magic = 6
        self.resistance = 10

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            self.set_stance('d')
            if self.shield == 0 and self.mana >= 20: self.cast_spell('s')
            else: return self.attack_target(target)
        return (False, 0)

class Human(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 250
        self.max_mana = 40
        self.max_shield = 50
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = 0
        self.attack = 7
        self.defense = 8
        self.magic = 5
        self.resistance = 4

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            if self.health*100 / self.max_health > 75: self.set_stance('a')
            elif self.health*100 / self.max_health > 30: self.set_stance('b')
            else: self.set_stance('d')
            
            if self.shield == 0 and self.mana >= 20: self.cast_spell('s')
            else: return self.attack_target(target)
        return (False, 0)

class Orc(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 250
        self.max_mana = 0
        self.max_shield = 100
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = self.max_shield
        self.attack = 7
        self.defense = 5
        self.magic = 2
        self.resistance = 4

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            self.set_stance('b')
            return self.attack_target(target)
        return (False, 0)

class Uruk(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 400
        self.max_mana = 20
        self.max_shield = 100
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = 0
        self.attack = 9
        self.defense = 7
        self.magic = 4
        self.resistance = 6

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            self.set_stance('a')
            return self.attack_target(target)
        return (False, 0)
  
class Witch(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 250
        self.max_mana = 80
        self.max_shield = 250
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = self.max_shield
        self.attack = 7
        self.defense = 4
        self.magic = 15
        self.resistance = 10

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            self.set_stance('a')
            if self.mana < 10 and target.mana > 0: self.cast_spell('f', target)
            elif self.shield == 0 and self.mana >= 20: self.cast_spell('s')
            elif self.mana >= 10: return self.cast_spell("fb", target)
            else: return self.attack_target(target)
        return (False, 0)

class Wizard(Character):

    def __init__(self, name):
        Character.__init__(self, name)
        self.max_health = 150
        self.max_mana = 100
        self.max_shield = 150
        self.health = self.max_health
        self.mana = self.max_mana
        self.shield = self.max_shield
        self.attack = 5
        self.defense = 6
        self.magic = 10
        self.resistance = 10

    def move(self, target):
        move_complete = Character.move(self, target)
        if not move_complete:
            self.set_stance('d')
            if self.mana < 10 and target.mana > 0: self.cast_spell('m', target)
            elif self.shield == 0 and self.mana >= 20: self.cast_spell('s')
            elif self.mana >= 10: return self.cast_spell('fb', target)
            else: return self.attack_target(target)
        return (False, 0)