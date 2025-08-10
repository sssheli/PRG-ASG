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


def clear_fog(fog, player):
    px = player['x']
    py = player['y']
    for dy in (0, 1):
        for dx in (0, 1):
            x = px + dx
            y = py + dy
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
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
    
    player['x'] = start_x
    player['y'] = start_y
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['pickaxe'] = 1      # lvl 1: can mine Copper only
    player['capacity'] = 10
    player['backpack_upgrade_cost'] = 20

    clear_fog(fog, player)
    
def inventory_count():
    return player['copper'] + player['silver'] + player['gold']

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
    px = player['x']
    py = player['y']

    lines = []
    for y in range(py - 1, py + 2):
        row = ""
        for x in range(px - 1, px + 2):
            if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT:
                row += "#"
            else:
                if fog[y][x]:
                    row += "#"
                else:
                    if x == px and y == py:
                        row += "M"
                    else:
                        row += game_map[y][x]
        lines.append(row)

    print("+---+")
    for row in lines:
        if len(row) < 3:
            row = row + " " * (3 - len(row))
        else:
            row = row[:3]
        print("|" + row + "|")
    print("+---+")

def show_information(player):
    print("\n--- Player Information ---")
    print("Name   : " + player['name'])
    print("Day    : " + str(player['day']))
    print("Turns  : " + str(player['turns']) + "/" + str(TURNS_PER_DAY))
    print("GP     : " + str(player['GP']))
    print("Copper : " + str(player['copper']))
    print("Silver : " + str(player['silver']))
    print("Gold   : " + str(player['gold']))
    return

def save_game(game_map, fog, player):
    f = open("save.txt", "w")  # use one filename consistently

    # 1: position
    f.write(str(player['x']) + " " + str(player['y']) + "\n")
    # 2: day, turns, GP
    f.write(str(player['day']) + " " + str(player['turns']) + " " + str(player['GP']) + "\n")
    # 3: ore
    f.write(str(player['copper']) + " " + str(player['silver']) + " " + str(player['gold']) + "\n")
    # 4: name
    f.write(player['name'] + "\n")
    # 5: upgrades & steps
    f.write(
    str(player['pickaxe']) + " " +
    str(player['capacity']) + " " +
    str(player['backpack_upgrade_cost']) + " " +
    str(player['steps']) + " " +
    str(player.get('portal_x', -1)) + " " +  # -1 means “no portal yet”
    str(player.get('portal_y', -1)) + "\n"
)
    # 6: fog header
    f.write("FOG\n")
    
    for y in range(MAP_HEIGHT):
        row = ""
        for x in range(MAP_WIDTH):
            row += "1" if fog[y][x] else "0"
        f.write(row + "\n")

    f.close()
    print("Game saved to save.txt")
        
def load_game(game_map, fog, player):
    load_map("level1.txt", game_map)

    f = open("save.txt", "r")

    # 1: position
    parts = f.readline().rstrip("\n").split()
    player['x'] = int(parts[0]); player['y'] = int(parts[1])

    # 2: day, turns, GP
    parts = f.readline().rstrip("\n").split()
    player['day'] = int(parts[0]); player['turns'] = int(parts[1]); player['GP'] = int(parts[2])

    # 3: ore
    parts = f.readline().rstrip("\n").split()
    player['copper'] = int(parts[0]); player['silver'] = int(parts[1]); player['gold'] = int(parts[2])

    # 4: name
    player['name'] = f.readline().rstrip("\n")

    # 5: upgrades & steps
    parts = f.readline().rstrip("\n").split()
    player['pickaxe'] = int(parts[0])
    player['capacity'] = int(parts[1])
    player['backpack_upgrade_cost'] = int(parts[2])
    player['steps'] = int(parts[3])
    # optional portal coords (older saves won’t have them)
    if len(parts) >= 6:
        player['portal_x'] = int(parts[4])
        player['portal_y'] = int(parts[5])
    # 6: "FOG"
    f.readline()

    fog[:] = []
    for _ in range(MAP_HEIGHT):
        line = f.readline().rstrip("\n")
        row = []
        for ch in line:
            row.append(True if ch == "1" else False)
        fog.append(row)

    f.close()

    # reveal around player per your rule (2x2)
    clear_fog(fog, player)
    print("Game loaded successfully!")
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
    print("(S)ell minerals")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

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
    player['steps'] = 0    
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
    player['steps'] = player['steps'] + 1
    tile = game_map[ny][nx]
    if tile in ('C', 'S', 'G'):
        if inventory_count() >= player['capacity']:
            print("Your backpack is full!")
        else:
            if tile == 'C':
                player['copper'] += 1
                game_map[ny][nx] = ' '
                print("You mined some copper!")
            elif tile == 'S':
                if player['pickaxe'] >= 2:
                    player['silver'] += 1
                    game_map[ny][nx] = ' '
                    print("You mined some silver!")
                else:
                    print("Your pickaxe is too weak to mine silver.")
            elif tile == 'G':
                if player['pickaxe'] >= 3:
                    player['gold'] += 1
                    game_map[ny][nx] = ' '
                    print("You mined some gold!")
                else:
                    print("Your pickaxe is too weak to mine gold.")
    clear_fog(fog, player)
    return True

def enter_mine():
    while True:
        print("---------------------------------------------------")
        print(" DAY " + str(player['day']))
        print("---------------------------------------------------")
        print("DAY " + str(player['day']))

        draw_view(game_map, fog, player)

        print("Turns left: " + str(player['turns']) +
              " Load: " + str(inventory_count()) + " / " + str(player['capacity']) +
              " Steps: " + str(player['steps']))
        print("(WASD) to move")
        print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")

        action = input("Action? ").strip().lower()

        if action == 'q':
            return "quit_to_main"

        if action == 'p':
            print("-----------------------------------------------------")
            print("You place your portal stone here and zap back to town.")

            # remember where you placed the portal
            player['portal_x'] = player['x']
            player['portal_y'] = player['y']

            # jump to town tile 'T'
            found_town = False
            for yy in range(MAP_HEIGHT):
                for xx in range(MAP_WIDTH):
                    if game_map[yy][xx] == 'T':
                        player['x'] = xx
                        player['y'] = yy
                        found_town = True
                        break
                if found_town:
                    break

            clear_fog(fog, player)

            # Sell all minerals automatically
            c = player['copper']; s = player['silver']; g = player['gold']
            total = (c * today_prices['copper'] +
                     s * today_prices['silver'] +
                     g * today_prices['gold'])

            if total > 0:
                if s == 0 and g == 0:
                    print("You sell " + str(c) + " copper ore for " + str(total) + " GP.")
                elif c == 0 and g == 0:
                    print("You sell " + str(s) + " silver ore for " + str(total) + " GP.")
                elif c == 0 and s == 0:
                    print("You sell " + str(g) + " gold ore for " + str(total) + " GP.")
                else:
                    print("You sell your minerals for " + str(total) + " GP.")

                player['GP'] += total
                player['copper'] = 0
                player['silver'] = 0
                player['gold'] = 0
                print("You now have " + str(player['GP']) + " GP!")
            else:
                print("You have no minerals to sell.")

            # New day
            end_of_day()
            return

        acted = False
        if action == 'w':
            acted = try_move(0, -1)
        elif action == 's':
            acted = try_move(0, 1)
        elif action == 'a':
            acted = try_move(-1, 0)
        elif action == 'd':
            acted = try_move(1, 0)
        elif action == 'm':
            draw_map(game_map, fog, player)
            input("\n(Press Enter to continue...)")
        elif action == 'i':
            show_information(player)
            input("\n(Press Enter to continue...)")
        else:
            print("Use WASD to move, or M, I, P, Q.")
            continue

        if acted:
            player['turns'] = player['turns'] - 1
            if player['turns'] <= 0:
                end_of_day()
                return

def buy_stuff():
    while True:
        print("----------------------- Shop Menu -------------------------")
        if player['pickaxe'] == 1:
            print("(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP")
        elif player['pickaxe'] == 2:
            print("(P)ickaxe upgrade to Level 3 to mine gold ore for 150 GP")
        else:
            print("(P)ickaxe upgrade: (Max level reached)")
        print("(B)ackpack upgrade to carry " + str(player['capacity'] + 2) +
      " items for " + str(player['backpack_upgrade_cost']) + " GP")
        print("(L)eave shop")
        print("-----------------------------------------------------------")
        print("GP: " + str(player['GP']))
        print("-----------------------------------------------------------")
        choice = input("Your choice? ").strip().lower()

        if choice == 'p':
            if player['pickaxe'] == 1:
                if player['GP'] >= 50:
                    player['GP'] -= 50
                    player['pickaxe'] = 2
                    print("You upgraded your pickaxe to Level 2. You can mine silver now!")
                else:
                    print("Not enough GP.")
            elif player['pickaxe'] == 2:
                if player['GP'] >= 150:
                    player['GP'] -= 150
                    player['pickaxe'] = 3
                    print("You upgraded your pickaxe to Level 3. You can mine gold now!")
                else:
                    print("Not enough GP.")
            else:
                print("Your pickaxe is already Level 3.")
        elif choice == 'b':
            if player['GP'] >= player['backpack_upgrade_cost']:
                player['GP'] -= player['backpack_upgrade_cost']
                player['capacity'] += 2  # each upgrade adds 2 slots
                print("Congratulations! You can now carry " + str(player['capacity']) + " items!")
                player['backpack_upgrade_cost'] += 4  # next upgrade costs 4 GP more
            else:
                print("Not enough GP.")
        elif choice == 'l': 
            print("Leaving shop...")
            return
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
        print("DAY " + str(player['day']))
        print("Today's prices: Copper " + str(today_prices['copper']) +
      " | Silver " + str(today_prices['silver']) +
      " | Gold " + str(today_prices['gold']))
        show_town_menu()
        choice = input("Your choice? ").strip().lower()

        if choice == "b":
            buy_stuff()
            input("\n(Press Enter to return to town...)")
        elif choice == "s":
            sell_all()
            input("\n(Press Enter to return to town...)")
        elif choice == "i":
            show_information(player)
            input("\n(Press Enter to return to town...)")
        elif choice == "m":
            draw_map(game_map, fog, player)
            input("\n(Press Enter to return to town...)")
        elif choice == "e":
            if 'portal_x' in player and 'portal_y' in player and player['portal_x'] >= 0 and player['portal_y'] >= 0:
                player['x'] = player['portal_x']
                player['y'] = player['portal_y']
            else:
                found_town = False
                for yy in range(MAP_HEIGHT):
                    for xx in range(MAP_WIDTH):
                        if game_map[yy][xx] == 'T':
                            player['x'] = xx
                            player['y'] = yy
                            found_town = True
                            break
                    if found_town:
                        break
                if not found_town:
                    print("Couldn't find the town tile 'T' on the map.")
                    continue  # stay in town menu 
            clear_fog(fog, player)          # reveal the starting spot
            result = enter_mine()            # show mine UI
            if result == "quit_to_main":
                return


while True:
    show_main_menu()
    choice1 = input("Your choice? ").strip().lower()

    if choice1 == "n":
        miner = input("Greetings, miner! What is your name? ")
        player['name'] = miner
        player['day'] = 1
        initialize_game(game_map, fog, player)
        roll_day_prices()
        print("Pleased to meet you, "+ miner + ". Welcome to Sundrop Town!")
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
    
    
