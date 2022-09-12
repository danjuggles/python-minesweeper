import random
from termcolor import colored, cprint

# just to force the same sequence for testing/setup
#random.seed(0)

number_of_rows = int(input("Choose number of rows (1-49): "))
number_of_cols = int(input("Choose number of columns (1-26): "))
difficulty_level = int(input("Choose difficulty (1-7): "))

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#symbols
sym_bomb = "💣"
sym_blank = "⬜"
sym_visited = "⬛"

game_ended = False

check_window = [[-1,-1], [-1,0], [-1,1],
                [0, -1], [0, 0], [0, 1],
                [1, -1], [1, 0], [1, 1]]

def create_play_area(rows, cols, difficulty=1):
    # create empty grids
    play_area = [[sym_blank for col in range(cols)] for row in range(rows)]
    data_grid = [[i for i in row] for row in play_area]

    # bomb stuff
    bomb_locations = []
    number_of_bombs = int(rows * cols * (difficulty / 25))
    for b in range(number_of_bombs):
        bomb_row = random.randint(0, number_of_rows-1)
        bomb_col = random.randint(0, number_of_cols-1)
        data_grid[bomb_row][bomb_col] = sym_bomb
        bomb_locations.append([bomb_row, alphabet[bomb_col]])
    print("There are {} bombs. Good luck!".format(number_of_bombs))
    #print("They are here: {}".format(sorted(bomb_locations)))

    # add numbers around bombs
    update_grid_with_numbers(data_grid)

    return play_area, data_grid, number_of_bombs

def update_grid_with_numbers(input_grid, char=sym_bomb):
    char_locations = []
    # passes over a grid looking for char
    for row in range(len(input_grid)):
        for col in range(len(input_grid[row])):
            bomb_counter = 0
            # make sure we don't overwrite a bomb
            if input_grid[row][col] == sym_bomb:
                continue
            # check adjacent squares
            for r, c in check_window:
                # no need to check ourselves, hopefully we won't wreck ourselves
                if r == 0 and c == 0:
                    continue
                # set the indecies to check
                row_check = row + r
                col_check = col + c
                # check to see if these are out of the input_grid
                if row_check < 0 or row_check > number_of_rows-1 or col_check < 0 or col_check > number_of_cols-1:
                    continue
                elif input_grid[row_check][col_check] == sym_bomb:
                    bomb_counter += 1
            # update the square
            if bomb_counter == 0:
                input_grid[row][col] = sym_blank
            else:
                input_grid[row][col] = " " + str(bomb_counter)
    return input_grid

def update_grid_after_good_guess(grid, row, col, adjacent_blanks=[]):
    play_grid[row][col] = sym_visited
    data_grid[row][col] = sym_visited
    # check adjacent squares
    for r, c in check_window:
        # no need to check ourselves, hopefully we won't wreck ourselves
        if r == 0 and c == 0:
            continue
        # set the indecies to check
        row_check = row + r
        col_check = col + c
        # check to see if these are out of the grid
        if row_check < 0 or row_check > number_of_rows-1 or col_check < 0 or col_check > number_of_cols-1:
            continue
        else:
            loc = [row_check, col_check]
            data = data_grid[row_check][col_check]
            if data == sym_blank: # is a blank
                loc = [row_check, col_check]
                if loc not in adjacent_blanks: # check to see if we already know about this one
                    adjacent_blanks.append(loc)
            else: # must be number
                play_grid[row_check][col_check] = data_grid[row_check][col_check]

    if len(adjacent_blanks) > 0:
        next_r, next_c = adjacent_blanks.pop(0)
        update_grid_after_good_guess(play_grid, next_r, next_c, adjacent_blanks)

    return play_grid

number_colors = {1:"blue", 2:"green", 3:"red", 4:"magenta", 5:"red", 6:"cyan", 7:"yellow", 8:"grey"}
def pretty_print_grid(grid):
    number_of_blanks = 0
    print_title, print_string = "", ""
    print(print_string)
    # create the title row and print it
    for l in range(number_of_cols):
        cprint(" {l}".format(l=alphabet[l]), "red", end="", attrs=["underline"])
    print("")
    # process and print grid
    row_number = 0
    for r in range(number_of_rows):
        for c in range(number_of_cols):
            x = grid[r][c]
            if x == sym_blank: # count the blanks
                number_of_blanks += 1
            # color print numbers
            if x != sym_blank and x != sym_bomb and x != sym_visited:
                num = x[1:]
                cprint(" {num}".format(num=num), number_colors[int(num)], end="")
            else: # print out the non-numbers
                cprint(grid[r][c], end="")
        cprint("|{r}".format(r=row_number), "red") # print the row ends
        row_number += 1
        print_string = ""
    if number_of_blanks == number_of_bombs:
        return 1 # win mechanism
    else:
        print("Remaining blanks: {blanks}".format(blanks=number_of_blanks-number_of_bombs))

def convert_user_input(row, col):
    r = int(row)
    c = alphabet.find(col.upper())
    return r, c

def check_guess(user_r, user_c):
    x = data_grid[user_r][user_c]
    if play_grid[user_r][user_c] != sym_blank:
        pretty_print_grid(play_grid)
        print("Not a blank, please try again")
    elif x == sym_bomb: # Bomb!
        pretty_print_grid(data_grid)
        return 0
    elif x == sym_blank: # blank space
      update_grid_after_good_guess(play_grid, user_r, user_c)
      return pretty_print_grid(play_grid)
    else: # must be a number
        play_grid[user_r][user_c] = x
        return pretty_print_grid(play_grid)

def clear_screen():
    print("\033[H\033[3J")
    for i in range(number_of_rows + 50):
        for j in range(number_of_cols + 50):
            print("")
    print("\033[H\033[3J")

# create a play area
play_grid, data_grid, number_of_bombs = create_play_area(number_of_rows, number_of_cols, difficulty_level)
pretty_print_grid(play_grid)

# play time
while True:
    user_ip_r = input("Enter row: ")    # grab some user input
    user_ip_c = input("Enter column: ") # grab some user input
    #coord = input("Enter coord as number,letter: ")
    #user_ip_r, user_ip_c = coord.split(",")
    user_r, user_c = convert_user_input(user_ip_r, user_ip_c) # convert it
    clear_screen()
    game = check_guess(user_r, user_c) # check the guess
    if game == 0: # lose message
        cprint(" __     __            _____            _     ", "red")
        cprint(" \ \   / /           / ____|          | |    ", "red")
        cprint("  \ \_/ /__  _   _  | (___  _   _  ___| | __ ", "red")
        cprint("   \   / _ \| | | |  \___ \| | | |/ __| |/ / ", "red")
        cprint("    | | (_) | |_| |  ____) | |_| | (__|   <  ", "red")
        cprint("    |_|\___/ \__,_| |_____/ \__,_|\___|_|\_\ ", "red")
        break
    elif game == 1: # win message
        cprint(" __     __           _____            _     ", "green")
        cprint(" \ \   / /          |  __ \          | |    ", "green")
        cprint("  \ \_/ /__  _   _  | |__) |___   ___| | __ ", "green")
        cprint("   \   / _ \| | | | |  _  // _ \ / __| |/ / ", "green")
        cprint("    | | (_) | |_| | | | \ \ (_) | (__|   <  ", "green")
        cprint("    |_|\___/ \__,_| |_|  \_\___/ \___|_|\_\ ", "green")
        break