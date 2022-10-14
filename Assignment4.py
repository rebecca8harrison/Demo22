# Import packages
import random
from IPython.display import clear_output

# Set key variables
KEY_LABEL = {"a":"left","s":"down","w":"up","d":"right","x":"exit"}
KEY_MOVE = {"a":(0, -1),"s":(1 ,0 ),"w":(-1, 0),"d":(0, 1)}

# Set the world map
# -1 is equal to a wall
# 0 is equal to a door
# 1 to 6 are the room numbers
WORLD_MAP = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1, 1, 1, 1, 1, 1, 1,-1, 2, 2,-1, 6, 6, 6, 6,-1,-1],
    [-1, 1, 1, 1, 1, 1, 1, 0, 2, 2,-1, 6, 6, 6, 6,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1, 2, 2,-1, 6, 6, 6, 6,-1,-1],
    [-1, 3, 3, 3, 3, 3, 3,-1, 2, 2,-1, 6, 6, 6, 6,-1,-1],
    [-1, 3, 3, 3, 3, 3, 3, 0, 2, 2,-1, 6, 6, 6, 6, 0,-1],
    [-1, 3, 3, 3, 3, 3, 3,-1, 2, 2,-1, 6, 6, 6, 6,-1,-1],
    [-1,-1,-1, 0,-1,-1,-1,-1,-1,-1,-1, 6, 6, 6, 6,-1,-1],
    [-1, 4, 4, 4, 4,-1, 5, 5, 5, 5,-1, 6, 6, 6, 6,-1,-1],
    [-1, 4, 4, 4, 4,-1, 5, 5, 5, 5,-1, 6, 6, 6, 6,-1,-1],
    [-1, 4, 4, 4, 4, 0, 5, 5, 5, 5,-1, 6, 6, 6, 6,-1,-1],
    [-1, 4, 4, 4, 4,-1, 5, 5, 5, 5, 0, 6, 6, 6, 6,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
]

# Set start location and end location
START_LOCATION = (1, 1) 
END_LOCATION = (5, 15)

# Define functions

# Function to move the player
def direct_yourself():
    while True:
        key_stroke = input("Which direction would you like to move? chose from: a to go left, s to go back, w to go forward, or d to go right")
            
        # Checks the guess is in the range specified
        if key_stroke not in KEY_LABEL.keys():
            print("Please enter either a to go left, s to go back, w to go forward, or d to go right")
        else:
            return key_stroke

# Function to check the move is valid, return the calculated location (new or old)
def move_if_valid(location,direction,key_room):
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
            print("You've hit a wall, you can't go", KEY_LABEL[direction])
            #print("your location is",location,"and the move was",move)
            return location
        elif cell == 0: # Signals to player that a door exists
            print("You have found a door 🚪, continue",KEY_LABEL[direction],"to go through it")
        else:
            old_cell = WORLD_MAP[location[0]][location[1]]
            if old_cell == 0:
                print("You have entered room", cell) 
                if key_room==cell:
                    print("The key is in this room")
            else:   
                print("You moved",KEY_LABEL[direction],"and are still in room", cell)
                #print("your location is",new_location,"and the move was",move)
                
        return new_location

# Function to randomly assign the key location to the map
def valid_location():
    while True:
        location = (
            random.randint(1,len(WORLD_MAP)-1),
            random.randint(1,len(WORLD_MAP[0])-1)
        )
        cell = WORLD_MAP[location[0]][location[1]]
        if cell>0:
            return location

# Prints the map
def print_map_discovered(fox, key,key_found,discovery_map):
    for i, row in enumerate(WORLD_MAP):
        for j, cell in enumerate(row):
            if not discovery_map[i][j]:
                print("⬛", end='')
            elif cell == -1:
                print("🚧", end='') # The empty end='' argument stops the printing of a new line
            elif (i,j) == fox:
                print("🦊", end='')
            elif cell == 0:
                print("🚪", end='')
            elif (i,j) == key and not key_found:
                print("🗝️", end='')
            else:
                print("⬜", end='')
        print() #Causes the row to end

# Function to reveal which parts of the map have already been visited
def reveal_map(discovery_map,location):
    for i in range(location[0]-1,location[0]+2):
        if i<0 or i>=len(discovery_map):
            continue
        for j in range(location[1]-1,location[1]+2):
            if j<0 or j>=len(discovery_map[0]):
                continue
            discovery_map[i][j]=True
    return discovery_map
    


def game_loop():
    # START GAME
    print("Welcome to the Adventure game.")
    print("The aim is to find your way through several rooms, locate the key, then make your way to the exit")
    print("You can direct your movements using the following keys:")
    print("w = up/forward")
    print("a = left")
    print("s = back/down")
    print("d = right")
    print("x to exit the game")
    
    location = START_LOCATION
    print("You are starting from room", WORLD_MAP[location[0]][location[1]])

    discovery_map = [[False] * len(WORLD_MAP[0]) for _ in WORLD_MAP]

    key_found = False
    key_location=valid_location()
    key_room = WORLD_MAP[key_location[0]][key_location[1]]
    #print("The key is at", key_location,"in room",key_room)


    discovery_map = reveal_map(discovery_map,location)
    print_map_discovered(location,key_location,key_found,discovery_map)

    # Game loop
    while True:
        # Move
        direction = direct_yourself()
        clear_output()
        if direction == "x":
            print("You have quit the game")
            return
        if key_room==1:
            print("The key is in this room")
        # Check location is valid, and if location is a door, or tells the room location
        location = move_if_valid(location,direction,key_room)
        discovery_map = reveal_map(discovery_map,location)
        print_map_discovered(location,key_location,key_found,discovery_map)
        if location==key_location:
            key_found=True
            print("You have found the key 🗝️ to the exit")

        if location==END_LOCATION:
            if key_found:
                print("You found the exit, you win! 🍕")
                break
            else:
                print("You have found the exit but you don't have the key, the key is in",key_location)

game_loop() 