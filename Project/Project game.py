# Import packages
import random
from IPython.display import clear_output 
#from pygame import mixer
import os
from os import system
import time
from time import sleep
import sys
import pandas as pd
from os.path import exists

# Rules of the game:
# you are a rabbit, locked in a field with a fox
# you want to try and find the carrot, and the key to the field, and leave, before the fox finds you
# there is also poison in the field that you can use to kill the fox 
# the fox will walk around randomly until it spots the rabbit, after that it will follow the rabbit, unless the rabbit kills the fox with the poison
# the game will collect information on each game played
# the game will present analysis on statistics of winning and loosing

# information to collect on the game: 
# Win: True/False
# Carrot found: True/False
# Poison found: True/False
# Poison used: True/False
# Fox killed: True/False
# Player's attempt number: positive integer
# Player's name: string
# Key found: true/false
# Fox killed rabbit: True/False
# distance between rabbit and fox at start:
# distance between rabbit and carrot at start:
# distance between rabbit and key at start:
# distance between rabbit and exit at start:

if exists('Project/df.csv'):
    df = pd.read_csv('Project/df.csv')
else:
    d = {'id':[1],
    'name':["test"],
    'win':[False],
    'distance_rabbit_fox_x':[0],
    'distance_rabbit_carrot_x':[0],
    'distance_rabbit_key_x':[0],
    'distance_rabbit_door_x':[0],
    'distance_rabbit_fox_y':[0],
    'distance_rabbit_carrot_y':[0],
    'distance_rabbit_key_y':[0],
    'distance_rabbit_door_y':[0],
    'carrot_found':[True],
    'key_found':[True],
    'poison_found':["Yes"],
    'fox_alive':[False],
    'attempt_no':[1]}
    
    df = pd.DataFrame(data=d)   

    df.to_csv('/Users/rebeccaharrison/Documents/Python/Bootcamp/Project/df.csv',index=False)

previous="x"
previous_range = ["y","n"]
while previous not in previous_range:
    
    previous = input("Have you played this game before? y/n?")
name="none"   
if previous=="n":
    name = input("What is your name?")
    attempt_no=1
else:
    names = set(df['name'])
    print(names)
    while name not in names:
        name = input("Please enter the name from the list above that you have used when you last played this game")
    attempt_no=len(df['name'].loc[df['name']==name])+1
print("This is your",attempt_no,"at playing the game")
# Set key variables
KEY_LABEL = {"a":"move left","s":"move down","w":"move up","d":"move right","x":"exit"}
KEY_MOVE = {"a":(0, -1),"s":(1 ,0 ),"w":(-1, 0),"d":(0, 1)}

# Set the world map
# -1 is equal to a wall
# 0 is equal to an item
# 1 means field
WORLD_MAP = [
    [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
    [-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],
    [-2,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-2],   
    [-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2],
    [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2]
]

# Create or load database

##### DEFINE FUNCTIONS

# Function to move the player
def direct_yourself(poison_found):
    while True:
        if poison_found=="Yes":
            KEY_LABEL["e"]="dropped poison"
            key_stroke = input("Which direction would you like to move? chose from: a to go left, s to go back, w to go forward, or d to go right, e to drop poison")
                
            # Checks the guess is in the range specified
            if key_stroke not in KEY_LABEL.keys():
                print("Please enter either a to go left, s to go back, w to go forward, d to go right or e to drop poison")
            else:
                return key_stroke
        else:
            key_stroke = input("Which direction would you like to move? chose from: a to go left, s to go back, w to go forward, or d to go right")
                
            # Checks the guess is in the range specified
            if key_stroke not in KEY_LABEL.keys():
                print("Please enter either a to go left, s to go back, w to go forward, or d to go right")
            else:
                return key_stroke

# Function to move the fox

# Function to move the fox
def move_fox(fox_alive,fox_location, poison_location, poison_found,location):
    if fox_alive==True:  
        while True:
            move=random.choice(list(KEY_MOVE.values()))
            new_fox_location = (
                fox_location[0] + move[0],
                fox_location[1] + move[1],
                )
            # Check that the location is within the map
            assert 0 <= new_fox_location[0] < len(WORLD_MAP)
            assert 0 <= new_fox_location[1] < len(WORLD_MAP[0])
            
            cell = WORLD_MAP[new_fox_location[0]][new_fox_location[1]]
            if cell < 0: # checks if hitting a wall, and if so returns original location
                continue
            if new_fox_location==poison_location and poison_found=="dropped":
                print("You've killed the fox")
                return False,new_fox_location
            else:   
                return True,new_fox_location  
    else:
        False,fox_location         

# Function to check the move is valid, return the calculated location (new or old)
def move_if_valid(location,direction):
    move = KEY_MOVE[direction]
    new_location = (
        location[0] + move[0],
        location[1] + move[1],
    )
    # Check that the location is within the map
    assert 0 <= new_location[0] < len(WORLD_MAP)
    assert 0 <= new_location[1] < len(WORLD_MAP[0])

    if direction=="x":
        return direction
    else:    
        cell = WORLD_MAP[new_location[0]][new_location[1]]
        # Setting the move
        if cell < 0: # checks if hitting a wall, and if so returns original location
            print("You've hit a wall, you can't", KEY_LABEL[direction])
            return location
        else:   
            print("You ",KEY_LABEL[direction])
                
                
        return new_location

# Function to randomly assign an entity to a location to the map
def valid_location(door=False):
    while True:
        if door==False:
            location = (
                random.randint(1,len(WORLD_MAP)-1),
                random.randint(1,len(WORLD_MAP[0])-1)
            )
            cell = WORLD_MAP[location[0]][location[1]]
            if cell==1:
                WORLD_MAP[location[0]][location[1]] = 2
                return location
        else:
            location = (
                random.randint(1,len(WORLD_MAP)-1),
                random.randint(1,len(WORLD_MAP[0])-1)
            )
            cell = WORLD_MAP[location[0]][location[1]]
            if cell==-1:
                WORLD_MAP[location[0]][location[1]] = 0
                return location

# Prints the map
def print_map(rabbit, fox, carrot, poison, key,key_found, poison_found,carrot_found,fox_alive):
    for i, row in enumerate(WORLD_MAP):
        for j, cell in enumerate(row):
            if cell <= -1:
                print("⬛", end='') # The empty end='' argument stops the printing of a new line
            elif (i,j) == fox and fox_alive:
                print("🦊", end='')
            elif (i,j) == fox and not fox_alive:
                print("🪦", end='')    
            elif (i,j) == rabbit:
                print("🐰", end='')
            elif (i,j) == poison and (poison_found=="No" or poison_found=="dropped"):
                print("💀", end='')
            elif (i,j) == carrot and not carrot_found:
                print("🥕", end='')
            elif cell == 0:
                print("🚪", end='')
            elif (i,j) == key and not key_found:
                print("🗝️", end='')
            else:
                print("🟩", end='')
        print() #Causes the row to end


def game_loop():
   # os.system('clear')
   # mixer.init()
   # mixer.music.load("black-knight-121105.mp3") # Music file can only be MP3
   # mixer.music.play()
    # Then start a infinite loop

    # START GAME
    print("Welcome to the Adventure game.\n")
    print("The aim is to find yourself a carrot to eat, then make your way out of the field, before the fox eats you \n")
    print("You will need to find the key to the door before you leave \n")
    print("There is also poison that you can use to kill the fox \n")
    print("You can direct your movements using the following keys:\n")
    print("w = up/forward")
    print("a = left")
    print("s = back/down")
    print("d = right")
    print("x to exit the game")
    
    location = valid_location()

    key_found = False
    carrot_found = False
    poison_found = "No"
    key_location=valid_location()
    fox_alive=True
    fox_location=valid_location()
    poison_location=valid_location()
    carrot_location=valid_location()
    door_location=valid_location(door=True)
    distance_rabbit_fox_x=fox_location[0]-location[0]
    distance_rabbit_fox_y=fox_location[1]-location[1]
    distance_rabbit_carrot_x=carrot_location[0]-location[0]
    distance_rabbit_carrot_y=carrot_location[1]-location[1]
    distance_rabbit_key_x=key_location[0]-location[0]
    distance_rabbit_key_y=key_location[1]-location[1]
    distance_rabbit_door_x=door_location[0]-location[0]
    distance_rabbit_door_y=door_location[1]-location[1]


    print_map(location, fox_location, carrot_location, poison_location, key_location,key_found, poison_found,carrot_found,fox_alive)

    # Game loop
    while True:
        # Move
        
        direction = direct_yourself(poison_found)
        clear_output()
        os.system('clear')
        if direction == "e":
            poison_location=location
            poison_found="dropped"
            print_map(location, fox_location, carrot_location, poison_location, key_location,key_found, poison_found,carrot_found,fox_alive)
            continue
        if direction == "x":
            print("You have quit the game")
            break
        # Check location is valid, and if location is a door, or tells the room location
        location = move_if_valid(location,direction)
        if fox_alive:
            fox_alive,fox_location = move_fox(fox_alive,fox_location, poison_location, poison_found,location)
        print_map(location, fox_location, carrot_location, poison_location, key_location,key_found, poison_found,carrot_found,fox_alive)
        if location==key_location:
            key_found=True
            print("You have found the key 🗝️ to the exit")
        if location==carrot_location:
            carrot_found=True
            print("You have found a carrot")
        if location==poison_location and poison_found=="No":
            poison_found="Yes"
            print("You have found the poison, you can press e to open and drop it and try to kill the fox")    
        if location==fox_location and fox_alive:
            print("You have been eaten by the fox, you loose")
            win=False
            break
        if location==door_location:
            if key_found and carrot_found:
                print("You found the exit, you are free and you win the game")
                win=True
                break
            if not key_found:
                print("You have found the exit but you don't have the key")
                
            if  key_found and not carrot_found:
                print("You have found the exit but you haven't eaten the carrot so don't have the energy to turn the key in the door")
    d = {'id':[1],
    'name':[""],
    'win':[win],
    'distance_rabbit_fox_x':[distance_rabbit_fox_x],
    'distance_rabbit_carrot_x':[distance_rabbit_carrot_x],
    'distance_rabbit_key_x':[distance_rabbit_key_x],
    'distance_rabbit_door_x':[distance_rabbit_door_x],
    'distance_rabbit_fox_y':[distance_rabbit_fox_y],
    'distance_rabbit_carrot_y':[distance_rabbit_carrot_y],
    'distance_rabbit_key_y':[distance_rabbit_key_y],
    'distance_rabbit_door_y':[distance_rabbit_door_y],
    'carrot_found':[carrot_found],
    'key_found':[key_found],
    'poison_found':[poison_found],
    'fox_alive':[fox_alive],
    'attempt_no':[1]}
    
    df = pd.DataFrame(data=d) 
    return df

df_game = game_loop() 
df_game.loc[0,'id']=max(df['id'])+1
print(attempt_no)
df_game.loc[0,'attempt_no']=attempt_no
df_game.loc[0,'name']=name
print(df_game)
df = pd.concat([df,df_game])
print(df)
df.to_csv('/Users/rebeccaharrison/Documents/Python/Bootcamp/Project/df.csv',index=False)

