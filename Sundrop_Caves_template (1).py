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
today_prices = {'copper': 0, 'silver': 0, 'gold': 0}

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    lines = map_file.readlines()
    for line in lines:
        line = line.rstrip('\n')     
        if line != "":
            map_struct.append(list(line))
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

#function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    px = player['x']
    py = player['y']
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            x = px + dx
            y = py + dy
            if x >= 0 and x < MAP_WIDTH and y >= 0 and y < MAP_HEIGHT:
                fog[y][x] = False
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
    fog[:] = []
    for _ in range(MAP_HEIGHT):
        fog.append([True] * MAP_WIDTH)
    
    # TODO: initialize player
    start_x = 0
    start_y = 0
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if game_map[y][x] == 'T':
                start_x = x
                start_y = y
    
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    print("\n----- Mine Map -----")
    for y in range(MAP_HEIGHT):
        row = ""
        for x in range(MAP_WIDTH):
            if fog[y][x]:
                row += '?'
            else:
                if x == player['x'] and y == player['y']:
                    row += 'P'
                else:
                    row += game_map[y][x]
        print(row)

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    print("\n--- View (3x3) ---")
    px = player['x']
    py = player['y']
    for y in range(py - 1, py + 2):
        row = ""
        for x in range(px - 1, px + 2):
            if x >= 0 and x < MAP_WIDTH and y >= 0 and y < MAP_HEIGHT:
                if fog[y][x]:
                    row += '?'
                else:
                    if x == px and y == py:
                        row += 'P'
                    else:
                        row += game_map[y][x]
            else:
                row += ' '
        print(row)


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
    def save_game(game_map, fog, player):
        f = open("save.txt", "w")
        f.write(str(player['x']) + " " + str(player['y']) + "\n")
        f.write(str(player['day']) + " " + str(player['turns']) + " " + str(player['GP']) + "\n")
        f.write(str(player['copper']) + " " + str(player['silver']) + " " + str(player['gold']) + "\n")
        f.write(player['name'] + "\n")
        f.write("FOG\n")
        for y in range(MAP_HEIGHT):
            row = ""
            for x in range(MAP_WIDTH):
                if fog[y][x]:
                    row += "1"
                else:
                    row += "0"
            f.write(row + "\n")
        f.close()
        print("Game saved to save.txt")
        
# This function loads the game
def load_game(game_map, fog, player):
    load_map("level1.txt", game_map)

    f = open("save.txt", "r")
    parts = f.readline().rstrip("\n").split()
    player['x'] = int(parts[0])
    player['y'] = int(parts[1])

    parts = f.readline().rstrip("\n").split()
    player['day'] = int(parts[0])
    player['turns'] = int(parts[1])
    player['GP'] = int(parts[2])

    parts = f.readline().rstrip("\n").split()
    player['copper'] = int(parts[0])
    player['silver'] = int(parts[1])
    player['gold'] = int(parts[2])

    player['name'] = f.readline().rstrip("\n")

    f.readline()  

    fog[:] = []
    for _ in range(MAP_HEIGHT):
        line = f.readline().rstrip("\n")
        row = []
        for ch in line:
            if ch == "1":
                row.append(True)
            else:
                row.append(False)
        fog.append(row)
    f.close()

    clear_fog(fog, player) 
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

def roll_day_prices():
    today_prices['copper'] = randint(prices['copper'][0], prices['copper'][1])
    today_prices['silver'] = randint(prices['silver'][0], prices['silver'][1])
    today_prices['gold']   = randint(prices['gold'][0], prices['gold'][1])

def check_win():
    if player['GP'] >= WIN_GP:
        print("\n*** Congratulations! You reached " + str(player['GP']) + " GP. You win! ***")
        print("Thanks for playing!")
        return True
    else:
        return False
def sell_all():
    total = (player['copper'] * today_prices['copper'] +
             player['silver'] * today_prices['silver'] +
             player['gold']   * today_prices['gold'])

    if total == 0:
        print("\nYou have no minerals to sell.")
        return

    print("\nSelling all minerals...")
    print(" Copper x" + str(player['copper']) + " at " + str(today_prices['copper']) + " GP")
    print(" Silver x" + str(player['silver']) + " at " + str(today_prices['silver']) + " GP")
    print("   Gold x" + str(player['gold'])   + " at " + str(today_prices['gold'])   + " GP")
    print(" -> You earn " + str(total) + " GP.")

    player['GP'] = player['GP'] + total
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0

    check_win()  

def end_of_day():
    player['day'] = player['day'] + 1
    player['turns'] = TURNS_PER_DAY
    print("\nYou return to town to rest.")
    print("*** A new day dawns! DAY " + str(player['day']) + " ***")
    roll_day_prices()

def try_move(dx, dy):
    nx = player['x'] + dx
    ny = player['y'] + dy

    if nx < 0 or nx >= MAP_WIDTH or ny < 0 or ny >= MAP_HEIGHT:
        print("You cannot go that way.")
        return False

    # Move
    player['x'] = nx
    player['y'] = ny

    # Check tile pickup
    tile = game_map[ny][nx]
    if tile == 'C':
        player['copper'] = player['copper'] + 1
        game_map[ny][nx] = ' '
        print("You mined some copper!")
    elif tile == 'S':
        player['silver'] = player['silver'] + 1
        game_map[ny][nx] = ' '
        print("You mined some silver!")
    elif tile == 'G':
        player['gold'] = player['gold'] + 1
        game_map[ny][nx] = ' '
        print("You mined some gold!")

    # Reveal new area
    clear_fog(fog, player)
    return True

def enter_mine():
    print("\n--- Entering the Mine ---")
    print("Controls: W/A/S/D to move, V=View, M=Full Map, Q=Leave")
    while True:
        print("Turns left today: " + str(player['turns']))
        cmd = input("> ").strip().lower()

        if cmd == 'q':
            print("You use the portal stone to return to town.")
            return

        acted = False
        if cmd == 'w':
            acted = try_move(0, -1)
        elif cmd == 's':
            acted = try_move(0, 1)
        elif cmd == 'a':
            acted = try_move(-1, 0)
        elif cmd == 'd':
            acted = try_move(1, 0)
        elif cmd == 'v':
            draw_view(game_map, fog, player)
        elif cmd == 'm':
            draw_map(game_map, fog, player)
        else:
            print("Use W/A/S/D to move, or V, M, Q.")

        if acted:
            player['turns'] = player['turns'] - 1
            if player['turns'] <= 0:
                end_of_day()
                return      

def buy_stuff():
    print("\n--- Sundrop Shop ---")
    print("1. Copper Pickaxe - 50 GP")
    print("2. Silver Pickaxe - 150 GP")
    print("3. Exit shop")

    choice = input("What would you like to buy? ").strip()

    if choice == "1":
        if player['GP'] >= 50:
            player['GP'] -= 50
            print("You bought a Copper Pickaxe!")
        else:
            print("Not enough GP!")
    elif choice == "2":
        if player['GP'] >= 150:
            player['GP'] -= 150
            print("You bought a Silver Pickaxe!")
        else:
            print("Not enough GP!")
    elif choice == "3":
        print("Leaving shop...")
    else:
        print("Invalid choice.")

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
        print("Today's prices: Copper " + str(today_prices['copper']) +
      " | Silver " + str(today_prices['silver']) +
      " | Gold " + str(today_prices['gold']))
        show_town_menu()
        choice = input("Your choice? ").strip().lower()

        if choice == "b":
            buy_stuff()
        elif choice == "i":
            show_information(player)
            input("\n(Press Enter to return to town...)")
        elif choice == "m":
            draw_map(game_map, fog, player)
            input("\n(Press Enter to return to town...)")
        elif choice == "e":
            print("Entering the mine...")
            enter_mine()
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
        player['name'] = miner
        player['day'] = 1
        initialize_game(game_map, fog, player)
        roll_day_prices()
        print(f"Pleased to meet you, {miner}. Welcome to Sundrop Town!")
        town_menu()                 

    elif choice1 == "l":
        load_game(game_map, fog, player)
        print("Game loaded successfully!")
        roll_day_prices()
        town_menu()                

    elif choice1 == "q":
        print("Thanks for playing. See you next time!")
        break
    else:
        print("Invalid choice. Please restart and choose N, L, or Q.")


# TODO: The game!
    
    
