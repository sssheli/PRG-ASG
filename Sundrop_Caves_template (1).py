from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    print("\n--- Mine Map (placeholder) ---")
    print("[###]")
    print("[#P#]   (P = player)")
    print("[###]")
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    return

# This function shows the information for the player
def show_information(player):
    print("\n--- Player Information ---")
    print(f"Name   : {player.get('name', 'Unknown')}")
    print(f"Day    : {player.get('day', 1)}")
    print(f"Turns  : {player.get('turns', TURNS_PER_DAY)}/{TURNS_PER_DAY}")
    print(f"GP     : {player.get('GP', 0)}")
    print(f"Copper : {player.get('copper', 0)}")
    print(f"Silver : {player.get('silver', 0)}")
    print(f"Gold   : {player.get('gold', 0)}")
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

    def buy_stuff():
        print("\n--- Sundrop Shop (placeholder) ---")
        print("Nothing to buy yet. (Implement later)")
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

def town_menu():
    while True:
        print(f"DAY {player.get('day', 1)}")
        show_town_menu()
        choice = input("Your choice? ").strip().lower()

        if choice == "b":
            print("Buying is not implemented yet.")
        elif choice == "i":
            show_information(player)
            input("\n(Press Enter to return to town...)")
        elif choice == "m":
            draw_map(game_map, fog, player)
            input("\n(Press Enter to return to town...)")
        elif choice == "e":
            print("Entering the mine... (not implemented yet)")
            # return here later when you implement the mine
        elif choice == "v":
            save_game(game_map, fog, player)
            print("Game saved!")
        elif choice == "q":
            print("Returning to main menu...")
            return   
        else:
            print("Invalid choice in town. Try again.\n")

while True:
    show_main_menu()
    choice1 = input("Your choice? ").strip().lower()

    if choice1 == "n":
        miner = input("Greetings, miner! What is your name? ")
        player['day'] = 1
        print(f"Pleased to meet you, {miner}. Welcome to Sundrop Town!")
        town_menu()                 

    elif choice1 == "l":
        load_game(game_map, fog, player)
        print("Game loaded successfully!")
        town_menu()                

    elif choice1 == "q":
        print("Thanks for playing. See you next time!")
        break
    else:
        print("Invalid choice. Please restart and choose N, L, or Q.")


# TODO: The game!
    
    
