#!/usr/local/bin/python3
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Modified with permission by Edwin Griffin
"""

import time         #Importing time   
import gui          #Importing the GUI file
import character    #Importing the Character file
import battle       #Importing the Battle file  

app = gui.simpleapp_tk(None)    
app.title('RPG Battle')

app.write('''
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

''')
app.write("You can exit the game at any time by typing in 'quit'")
app.write("")

def set_mode():
  """ Select the game mode """
  # This is an error checking version of reading user input
  # This uses exception handling as discussed in topic 3
  # Understanding try/except cases is important for
  # verifying user input
  try:
    app.write("Please select a side:")          # Asking for the side
    app.write("1. Good")
    app.write("2. Evil")
    app.write("")
    app.wait_variable(app.inputVariable)
    mode = app.inputVariable.get()
    
    if mode == 'quit':        # Quit game mode input
      app.quit()        
    
    mode = int(mode)             
    if mode not in range(1,3):  #Checking whether if the input is between 1 to 3 or not
      raise ValueError
  
  except ValueError:            # Raising an error message   
    app.write("You must enter a valid choice")
    app.write("")
    mode = set_mode()         # Storing set_mode() inside the mode variable
  
  return mode               # Returning a value to this variable 

def set_race(mode):
  """ Set the player's race """
  # If loop for the Evil mode
  if mode == 2:             
    app.write("Playing as the Forces of Sauron.")
    app.write("")
  
    try:
      app.write("Please select your race:")     # Asking for the race for the player by the given options
      app.write("1. Goblin")  
      app.write("2. Orc")
      app.write("3. Uruk")
      app.write("4. Wizard")
      app.write("")
      app.wait_variable(app.inputVariable)
      race = app.inputVariable.get()          # Storing the player's chosen option into the 'race' variable
      
      if race == 'quit':              # Quit game mode input
        app.quit()
      
      race = int(race)                
      if race not in range(1,5):      # Checking whether if the input is between 1 to 5 or not
        raise ValueError
    
    except ValueError:                # Raising the 
      app.write("You must enter a valid choice")
      app.write("")
      race = set_race(mode)

  else: 
    app.write("Playing as the Free Peoples of Middle Earth.")
    app.write("")

    try:
      app.write("Please select your race:")
      app.write("1. Elf")
      app.write("2. Dwarf")
      app.write("3. Human")
      app.write("4. Hobbit")
      app.write("5. Wizard")
      app.write("")
      app.wait_variable(app.inputVariable)
      race = app.inputVariable.get()
      
      if race == 'quit':
        app.quit()
      race = int(race)
      
      if race not in range(1,6):
        raise ValueError
    
    except ValueError:
      app.write("You must enter a valid choice")
      app.write("")
      race = set_race(mode)
  
  return race

def set_name():
  """ Set the player's name """
  try:
    app.write("Please enter your Character Name:")
    app.write("")
    app.wait_variable(app.inputVariable)
    char_name = app.inputVariable.get()

    if char_name == 'quit':
      app.quit()

    if char_name == '':
      raise ValueError

  except ValueError:
    app.write("")
    app.write("Your name cannot be blank")
    char_name = set_name()

  return char_name

def create_player(mode, race, char_name):
  """ Create the player's character """
  if mode == 2:
    if race == 1:
      player = character.Goblin(char_name, app)
    elif race == 2:
      player = character.Orc(char_name, app)
    elif race == 3:
      player = character.Uruk(char_name, app)
    else:
      player = character.Wizard(char_name, app)
  else:
    if race == 1:
      player = character.Elf(char_name, app)
    elif race == 2:
      player = character.Dwarf(char_name, app)
    elif race == 3:
      player = character.Human(char_name, app)
    elif race == 4:
      player = character.Hobbit(char_name, app)
    else:
      player = character.Wizard(char_name, app)
  return player

def set_difficulty():
  """ Set the difficulty of the game """
  try:
    app.write("Please select a difficulty level:")
    app.write("e - Easy")
    app.write("m - Medium")
    app.write("h - Hard")
    app.write("l - Legendary")
    app.write("")
    app.wait_variable(app.inputVariable)
    difficulty = app.inputVariable.get()

    if difficulty == 'quit':
      app.quit()

    if difficulty not in ['e','m','h','l'] or difficulty == '':
      raise ValueError

  except ValueError:
    app.write("You must enter a valid choice")
    app.write("")
    difficulty = set_difficulty()

  return difficulty

def create_enemies(mode, difficulty):
  """ Create the enemies """
  if mode == 2:
    if difficulty == 'm':
      enemies = [character.Hobbit("Peregrin", app), character.Hobbit("Meriadoc", app), character.Human("Eowyn", app)]
    elif difficulty == 'h':
      enemies = [character.Dwarf("Gimli", app), character.Elf("Legolas", app), character.Human("Boromir", app)]
    elif difficulty == 'l':
      enemies = [character.Human("Faramir", app), character.Human("Aragorn", app), character.Wizard("Gandalf", app)]
    else:
      enemies = [character.Hobbit("Frodo", app), character.Hobbit("Sam", app)]

  else:
    if difficulty == 'm':
      enemies = [character.Goblin("Azog", app), character.Goblin("Gorkil", app), character.Orc("Sharku", app)]
    elif difficulty == 'h':
      enemies = [character.Orc("Shagrat", app), character.Orc("Gorbag", app), character.Uruk("Lurtz", app)]
    elif difficulty == 'l':
      enemies = [character.Orc("Grishnakh", app), character.Uruk("Lurtz", app), character.Wizard("Saruman", app)]
    else:
      enemies = [character.Goblin("Azog", app), character.Goblin("Gorkil", app)]

  return enemies

def quit_game():
  """ Quits the game """
  try:
    app.write("Play Again? (y/n)")
    app.write("")
    app.wait_variable(app.inputVariable)
    quit_choice = app.inputVariable.get()

    if quit_choice == 'quit':
      app.quit()

    if quit_choice not in 'yn' or quit_choice == '':
      raise ValueError

  except ValueError:
    app.write("You must enter a valid choice")
    app.write("")
    quit_choice = quit_game()

  return quit_choice

def print_results():
  app.write("Game Over!")
  app.write("No. Battles: {0}".format(str(battles)))
  app.write("No. Wins: {0}".format(wins))
  app.write("No. Kills: {0}".format(kills))
  app.write("Success Rate (%): {0:.2f}%".format(float(wins*100/battles)))
  app.write("Avg. kills per battle: {0:.2f}".format(float(kills)/battles))
  app.write("")

battles = 0
wins = 0
kills = 0

mode = set_mode()
race = set_race(mode)
char_name = set_name()
player = create_player(mode, race, char_name)
app.write(player)
app.write("")
difficulty = set_difficulty()
enemies = create_enemies(mode, difficulty)

while True:

  encounter = battle.Battle(player, enemies, app)
  battle_wins, battle_kills = encounter.play()

  battles += 1
  wins += battle_wins
  kills += battle_kills

  print_results()
    
  quit = quit_game()

  if quit == "n":
    app.write("Thank you for playing RPG Battle.")
    time.sleep(2)
    app.quit()

  else:
    # Playing again - reset all enemies and players
    player.reset()
    for enemy in enemies:
      enemy.reset()
