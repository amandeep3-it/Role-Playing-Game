"""
battle.py - The battle class manages the events of the battle

Modified by Amandeep Singh
Originally written by Bruce Fuda for Intermediate Programming
Modified with permission by Edwin Griffin
"""

import os, sys, time, random

class Battle:

    def __init__(self, env):
        self.env = env

        self.turn = 0
        self.wins = 0
        self.kills = 0
        self.gold = 0

        self.player_won = False
        self.player_lost = False
 
    def play(self):
        while not self.player_won and not self.player_lost and self.env.status == "Battle":
            os.system("cls")
            self.turn += 1
            print("Turn:", self.turn)
            print('')
            time.sleep(2)

            self.do_player_actions()
            self.do_enemy_actions()

        return (self.player_won, self.wins, self.kills, self.gold)

    def do_player_actions(self):
        player = self.env.player
        if len(player.members) == 0: return
        print("The Player's Turn")
        print('')
        pi = self.select_player()
        p = player.members[pi]
        print("{} the {} has been chosen.".format(p.name, p.__class__.__name__))
        print('')
        turn_over = False
        i = 0
        while not self.player_won and not self.player_lost and not turn_over and self.env.status == "Battle":
            if i != 0: os.system("cls")
            print('')
            i += 1
            p.print_status(player.gold)

            action = self.get_action(p)

            # Player has choosen to use inventory items
            if action == 4:
                os.system("cls")
                if len(player.inventory) > 0 or p.weapon != None or p.armour != None:
                    p.useInventory(self.env, player.inventory)
                else:
                    print("You curently have nothing in your inventory.")
                    time.sleep(1)
                    print('')

            # Player has choosen to use spell
            elif action == 3:
                os.system("cls")
                c = self.select_spell(p)
                if c != 0:
                    turn_over = True

                    if c == "fb":
                        ti = self.select_target()
                        t = self.env.battle_enemy_team.members[ti]
                        print("{} has been chosen as the target.".format(t.name))
                        print('')
                        k, g = p.cast_spell(c, t)
                        if k:
                            print("Enemy has been killed.")
                            print('')
                            self.env.battle_enemy_team.members.pop(ti)
                            self.kills += 1
                        self.gold += g
                    elif c == 's': p.cast_spell(c)
                    else:
                        ti = self.select_target()
                        t = self.env.battle_enemy_team.members[ti]
                        print("{} has been chosen as the target.".format(t.name))
                        print('')
                        p.cast_spell(c, t)

            # Player has choosen to change stance
            elif action == 2:
                os.system("cls")
                c = self.select_stance()
                p.set_stance(c)
            
            # Player has choosen to attack
            elif action == 1:
                os.system("cls")
                ti = self.select_target()
                t = self.env.battle_enemy_team.members[ti]
                print("{} has been chosen as the target.".format(t.name))
                print('')
                turn_over = True
                k, g = p.attack_target(t)
                if k:
                    print("Enemy has been killed.")
                    print('')
                    self.env.battle_enemy_team.members.pop(ti)
                    self.kills += 1
                self.gold += g
            else:
                self.env.status = "Map"
                print("Fleeing from the Battle.")
                print('')
            time.sleep(1)

            if len(self.env.battle_enemy_team.members) == 0: self.player_won = True
            elif len(player.members) == 0: self.player_lost = True

            if self.player_won: self.wins += 1

    def select_player(self):
        team = self.env.player.members
        if (len(team) == 1): return 0
        print("Choose Player from the team:")
        for i, tm in enumerate(team):
            print(" {}. \"{}\" the {}".format((i + 1), tm.name, tm.__class__.__name__))
        print('')
        ind = self.env.input(list(range(1, (len(team) + 1))), "int") - 1
        return ind

    def select_target(self):
        team = self.env.battle_enemy_team.members
        if (len(team) == 1): return 0
        print("Choose your target:")
        for i, tm in enumerate(team):
            print(" {}. \"{}\" the {}".format((i + 1), tm.name, tm.__class__.__name__))
        print('')
        ind = self.env.input(len(range(1, (len(team) + 1))), "int") - 1
        return ind

    def get_action(self, p):
        print("Choose your move:")
        print(" 1. Attack Enemies")
        print(" 2. Change Stance")
        print(" 3. Cast Magic")
        print(" 4. Use Inventory")
        print(" 0. Flee from Battle")
        print('')
        return self.env.input(list(range(0, 5)), "int")
    
    def select_stance(self):
        print("Choose your stance:")
        print(" a - Aggressive")
        print(" d - Defensive")
        print(" b - Balanced")
        print('')
        inp = self.env.input(['a','d','b'])
        return inp

    def select_spell(self, p):
        r = p.__class__.__name__
        print("Mana:", p.mana)
        op = []
        print("Select your spell:")
        if p.mana >= 10 and r == "Wizard":
            op.append("fb")
            print(" {}. Fireball (10 mp)".format(len(op)))
        if p.mana >= 20:
            op.append('s')
            print(" {}. Shield (20 mp)".format(len(op)))
        if r == "Wizard":
            op.append('m')
            print(" {}. Mana Drain (no mp cost)".format(len(op)))
        if p.mana >= 10 and r == "Witch":
            op.append('f')
            print(" {}. Freeze (10 mp)".format(len(op)))
        print(" 0. Cancel Spell")
        print('')
        inp = self.env.input(list(range(0, len(op) + 1)), "int")
        return (0 if (inp == 0) else op[inp - 1])

    def do_enemy_actions(self):
        team = self.env.battle_enemy_team
        if len(team.members) == 0 or self.player_won or self.player_lost or self.env.status != "Battle": return
        os.system("cls")
        print("The Enemy's Turn")
        print('')
        time.sleep(1)
        
        e = None
        while True:
            e = team.members[random.randint(0, len(team.members) - 1)]
            if e.health > 0: break
        print("{} the {} will be making a move.".format(e.name, e.__class__.__name__))
        print('')

        if not self.player_won and not self.player_lost and self.env.status == "Battle":
            e.frozen()

            ti = random.randint(0, len(self.env.player.members) - 1)
            kill, g = e.move(self.env.player.members[ti])

            if kill:
                print(self.env.player.members[ti].name, "have been killed by the enemy.")
                print('')
                self.env.player.members.pop(ti)
                if len(self.env.player.members) == 0: self.player_lost = True
                time.sleep(1)