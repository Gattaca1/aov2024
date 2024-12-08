import itertools

def get_input():
    gameboard = []
    with open('input', 'r') as file:
        for line in file:
            line = line.strip()
            temp_line = []
            for char in line:
                temp_line.append(char)
            gameboard.append(temp_line)

    char_dict = {}
    for row_idx, row in enumerate(gameboard):
        for col_idx, char in enumerate(row):            
            if char != '.':
                if char not in char_dict:
                    char_dict[char] = {
                        'gameboard': [r[:] for r in gameboard],
                        'character_position_array': []
                    }
                char_dict[char]['character_position_array'].append((row_idx, col_idx))
    
    return char_dict, gameboard

def subtract_tuples(tuple_1, tuple_2):
    return tuple(map(lambda i, j: i - j, tuple_1, tuple_2))

def add_tuples(tuple_1, tuple_2):
    return tuple(map(lambda i, j: i + j, tuple_1, tuple_2))

def multiply_tuple_by_scalar(tuple_actual, scalar_actual):
    return (tuple_actual[0] * scalar_actual, tuple_actual[1] * scalar_actual)

def place_antinodes(data_dict, game_board):
    max_height = 0
    max_width = 0
    
    row = 0
    col = 1

    #initialize some things
    for key in data_dict:
        max_height = len(data_dict[key]['gameboard'])
        max_width = len(data_dict[key]['gameboard'][0])        
        break
    
    for character_key in data_dict:
        combinations = list(itertools.product(data_dict[character_key]['character_position_array'], repeat=2))

        for pair in combinations:
            if pair[0] == pair[1]:
                continue
            slope = (abs(pair[0][row]) - abs(pair[1][row]), abs(pair[0][col]) - abs(pair[1][col]))
            
            for i in range(max(max_height, max_width)): # this is a copout just to do it the worst case amount of times
            # Gonna make the assumption that there can only be 1 antinode of a same type in the same location
                node_1 = ()
                node_2 = ()
                if add_tuples(pair[0], slope) == pair[1]:
                    node_1 = subtract_tuples(pair[0], multiply_tuple_by_scalar(slope, i))
                    node_2 = add_tuples(pair[1], multiply_tuple_by_scalar(slope, i))
                else:
                    node_1 = add_tuples(pair[0], multiply_tuple_by_scalar(slope, i))
                    node_2 = subtract_tuples(pair[1], multiply_tuple_by_scalar(slope, i))
                

                if node_1 and node_1[row] >= 0 and node_1[row] < max_height and node_1[col] >= 0 and node_1[col] < max_width:
                    data_dict[character_key]['gameboard'][node_1[0]][node_1[1]] = "#"
                if node_2 and node_2[row] >= 0 and node_2[row] < max_height and node_2[col] >= 0 and node_2[col] < max_width:
                    data_dict[character_key]['gameboard'][node_2[0]][node_2[1]] = "#"

    
    for character_key in data_dict:
        for line_idx, line in enumerate(data_dict[character_key]['gameboard']):
            temp_line = game_board[line_idx].copy()
            for char_idx, char in enumerate(line):
                if char == "#":
                    temp_line[char_idx] = "#"
            game_board[line_idx] = temp_line
    
    for line in game_board:
        print(line)
    tally = 0
    for line in game_board:
        for char in line:
            if char == "#":
                tally = tally + 1
    print(tally)


def main():
    data_dict, gameboard = get_input()
    place_antinodes(data_dict, gameboard)

if __name__ == "__main__":
    main()