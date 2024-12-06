# from numpy import *
def read_and_process_board():
    board = []

    with open('input', 'r') as file:
        for line in file:
            line = line.strip()

            row = []
            for index in range(len(line)):
                if line[index] in ['#', '^', '>', '<', 'v']:
                    row.append(line[index])
                else:
                    row.append(" ")
            board.append(row)

    return board

def get_starting_pos(board):
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            if board[row_idx][col_idx] in ['^', '>', '<', 'v']:
                return (row_idx ,col_idx), board[row_idx][col_idx]

def predict_path(board, starting_pos, start_direction):
    # [up, right, down, left]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_map = {'^': 0, '>': 1, 'v': 2, '<': 3}
    direction_index = direction_map[start_direction]

    row, column = starting_pos
    # board[starting_pos[0]][starting_pos[1]] = "X"

    # Set to track visited positions along with directions
    visited_positions = set()
    #visited_positions.add((starting_pos, directions[direction_index]))
    visited_positions.add(starting_pos)
    
    new_pos = add_tuples(starting_pos, directions[direction_index])

    while True:        
        # check if the new position is out of bounds
        if new_pos[0] < 0 or new_pos[0] >= len(board) or new_pos[1] < 0 or new_pos[1] >= len(board[0]):
            break
        
        # if we encounter a '#', turn 90 degrees to the right
        if board[new_pos[0]][new_pos[1]] == '#':
            this_pos = subtract_tuples(new_pos, directions[direction_index])

            direction_index = (direction_index + 1) % 4            
            new_pos = add_tuples(this_pos, directions[direction_index])
            continue
        
        # mark spot with an X
        #board[new_pos[0]][new_pos[1]] = 'X'
        #visited_positions.add((new_pos, directions[direction_index]))
        visited_positions.add(new_pos)

        # continue moving
        new_pos = add_tuples(new_pos, directions[direction_index])
    
    return visited_positions

def uniq_pos_count(board):
    count = 0
    for row in board:
        count += row.count('X')
    return count

def subtract_tuples(tuple_1, tuple_2):
    return tuple(map(lambda i, j: i - j, tuple_1, tuple_2))

def add_tuples(tuple_1, tuple_2):
    return tuple(map(lambda i, j: i + j, tuple_1, tuple_2))

def place_new_obstacles(board, starting_pos, starting_icon):
    # [up, right, down, left]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_map = {'^': 0, '>': 1, 'v': 2, '<': 3}
    direction_index = direction_map[starting_icon]

    row, column = starting_pos
    
    previous_obstacle_pos = ()
    tally = 0
    while True:
        current_obstacle_pos = find_next_obstacle(board, (row, column), directions[direction_index])
        if current_obstacle_pos == (-1, -1):
            break

        # Found an obstacle, so set guard position and then turn right
        #row = current_obstacle_pos[0] - directions[direction_index][0]
        #column = current_obstacle_pos[1] - directions[direction_index][1]
        row, column = subtract_tuples(current_obstacle_pos, directions[direction_index])
        direction_index = (direction_index + 1) % 4
        
        # Initialize the first obstacle
        if previous_obstacle_pos == ():
            previous_obstacle_pos = current_obstacle_pos
            continue
        
        # If we have already found a first obstacle, (and a second), then we should look for the third so we can place the fourth
        next_obstacle_pos = find_next_obstacle(board, (row, column), directions[direction_index])
        if next_obstacle_pos == (-1, -1):
            break
        
        print("previous obstacle: (%d, %d)" % (previous_obstacle_pos[0], previous_obstacle_pos[1]))
        print("this obstacle: (%d, %d)" % (current_obstacle_pos[0], current_obstacle_pos[1]))
        print("next obstacle: (%d, %d)" % (next_obstacle_pos[0], next_obstacle_pos[1]))
        # We found a third obstacle, so now we can potentially place down a loop obstacle
        # This will be found by turning right again, and going forward until one of our positions matches
        # a position from previous obstacle. then the object will go 1 further
        loop_guard_pos = subtract_tuples(next_obstacle_pos, directions[direction_index])
        loop_direction = directions[(direction_index + 1) % 4]
        loop_object_pos = ()
        while True:
            if loop_guard_pos[0] == previous_obstacle_pos[0] or loop_guard_pos[1] == previous_obstacle_pos[1]:
                potential_object_pos = add_tuples(loop_guard_pos, loop_direction)
                break
            loop_guard_pos = add_tuples(loop_guard_pos, loop_direction)

        # Try placing object position
        if board[potential_object_pos[0]][potential_object_pos[1]] == " ":
            board[potential_object_pos[0]][potential_object_pos[1]] = "O"

            # See if walking the guard from "next_obstacle_pos" runs into our placed object
            new_pos = subtract_tuples(next_obstacle_pos, directions[direction_index])
            new_direction = directions[(direction_index + 1) % 4]
            hit_object_pos = find_next_obstacle(board, new_pos, new_direction)

            if hit_object_pos[0] == potential_object_pos[0] and hit_object_pos[1] == potential_object_pos[1]:            
                #print("placed obstacle: " + str(add_tuples(loop_guard_pos, loop_direction)))
                
                # might need to walk from placed object to previous object
                # turn to the right, and do it again
                new_pos = subtract_tuples(hit_object_pos, directions[(direction_index + 1) % 4])
                new_direction = directions[(direction_index + 2) % 4]
                hit_object_pos = find_next_obstacle(board, new_pos, new_direction)

                if hit_object_pos[0] == previous_obstacle_pos[0] and hit_object_pos[1] == previous_obstacle_pos[1]:            
                    print("placed obstacle: " + str(add_tuples(loop_guard_pos, loop_direction)))

                    tally = tally + 1
            
            # remove placed object
            board[potential_object_pos[0]][potential_object_pos[1]] = " "

        # (6,3) is correct, (7,6) is correct, (7,7) is correct, (8,1) is correct, (9,7) is correct
        # missing (8,3), fuck
        print()

        # Done with this cycle
        previous_obstacle_pos = current_obstacle_pos

    print(tally)


def find_next_obstacle(board, starting_pos, start_direction):    
    row, column = starting_pos

    delta_row, delta_column = start_direction
    next_row = row + delta_row
    next_column = column + delta_column
    
    while True:
        # check if the new position is out of bounds
        if next_row < 0 or next_row >= len(board) or next_column < 0 or next_column >= len(board[0]):
            break
        
        # if we encounter a '#', 'O', return its position
        if board[next_row][next_column] in ['#', 'O']:
            return (next_row, next_column)
        
        # move in the current direction
        next_row = next_row + delta_row
        next_column = next_column + delta_column
    return (-1, -1)

def has_loop(board, starting_pos, start_direction):
    # [up, right, down, left]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_map = {'^': 0, '>': 1, 'v': 2, '<': 3}
    direction_index = direction_map[start_direction]

    row, column = starting_pos

    # Set to track visited positions along with directions
    visited_positions = set()
    visited_positions.add((starting_pos, directions[direction_index]))

    new_pos = add_tuples(starting_pos, directions[direction_index])    

    while True:        
        # check if the new position is out of bounds
        if new_pos[0] < 0 or new_pos[0] >= len(board) or new_pos[1] < 0 or new_pos[1] >= len(board[0]):
            break
        
        # If the current position with the same direction has been visited, we have a loop
        if (new_pos, directions[direction_index]) in visited_positions:
            #print("Loop detected at position " + str(new_pos) + " with direction " + str(directions[direction_index]))
            return True
        
        # if we encounter a '#', turn 90 degrees to the right
        if board[new_pos[0]][new_pos[1]] in ['#', 'O']:
            this_pos = subtract_tuples(new_pos, directions[direction_index])

            direction_index = (direction_index + 1) % 4            
            new_pos = add_tuples(this_pos, directions[direction_index])
            continue
        
        # Track position
        visited_positions.add((new_pos, directions[direction_index]))

        # continue moving
        new_pos = add_tuples(new_pos, directions[direction_index])
    
    # if board[6][3] == 'O':
    #     print("first case")
    #     print(visited_positions)

    return False

def main():
    board = read_and_process_board()
    starting_pos, start_direction = get_starting_pos(board)
    
    board[starting_pos[0]][starting_pos[1]] = " "
    for line in board:
        print(line)
    
    visited_positions_with_directions = predict_path(board, starting_pos, start_direction)
    
    tally = 0
    for position in visited_positions_with_directions:
        #print(position)
        temp_board = [row[:] for row in board]
        temp_board[position[0]][position[1]] = "O"
        
        if has_loop(temp_board, starting_pos, start_direction):
            # for line in temp_board:
            #     print(line)
            # print()
            tally = tally + 1
    print(tally)
    print(len(visited_positions_with_directions))

    #print(uniq_pos_count(board))
    
    #board = read_and_process_board()
    #place_new_obstacles(board, starting_pos, start_direction)


if __name__ == "__main__":
    main()
