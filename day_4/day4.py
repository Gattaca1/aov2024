from typing import List

def get_board() -> List[List[str]]:
    board: List[List[str]] = []
    with open('input', 'r') as file:
        for line in file:
            board.append(line.strip())

    return board


def find_words(board: List[List[str]]) -> int:
    rows: int = len(board)
    columns: int = len(board[0])

    count: int = 0

    for i in range(rows):
        for j in range(columns):
            # Initiate search only on X or S (looking for XMAS or SAMX)
            if board[i][j] != 'X' and board[i][j] != 'S':
                continue
            
            if j < columns - 3:
                if look_right(board, i, j):
                    count = count + 1
            if i > 2:
                if look_up(board, i, j):
                    count = count + 1
            if i > 2 and j < columns - 3:
                if look_up_right(board, i, j):
                    count = count + 1
            if i > 2 and j > 2:
                if look_up_left(board, i, j):
                    count = count + 1
    return count


def look_up(board: List[List[str]], i: int, j: int) -> bool:
    if board[i][j] == 'X' and board[i-1][j] == 'M' and board[i-2][j] == 'A' and board[i-3][j] == 'S':
        return True
    if board[i][j] == 'S' and board[i-1][j] == 'A' and board[i-2][j] == 'M' and board[i-3][j] == 'X':
        return True
    return False


def look_up_right(board: List[List[str]], i: int, j: int) -> bool:
    if board[i][j] == 'X' and board[i-1][j+1] == 'M' and board[i-2][j+2] == 'A' and board[i-3][j+3] == 'S':
        return True
    if board[i][j] == 'S' and board[i-1][j+1] == 'A' and board[i-2][j+2] == 'M' and board[i-3][j+3] == 'X':
        return True
    return False


def look_up_left(board: List[List[str]], i: int, j: int) -> bool:
    if board[i][j] == 'X' and board[i-1][j-1] == 'M' and board[i-2][j-2] == 'A' and board[i-3][j-3] == 'S':
        return True
    if board[i][j] == 'S' and board[i-1][j-1] == 'A' and board[i-2][j-2] == 'M' and board[i-3][j-3] == 'X':
        return True
    return False


def look_right(board: List[List[str]], i: int, j: int) -> bool:
    if board[i][j] == 'X' and board[i][j+1] == 'M' and board[i][j+2] == 'A' and board[i][j+3] == 'S':
        return True
    if board[i][j] == 'S' and board[i][j+1] == 'A' and board[i][j+2] == 'M' and board[i][j+3] == 'X':
        return True
    return False


def find_mas_cross(board: List[List[str]]) -> int:
    rows: int = len(board)
    columns: int = len(board[0])

    count: int = 0

    for i in range(rows):
        for j in range(columns):
            # Initiate search only on A
            if board[i][j] != 'A':
                continue
            
            # Don't look for an 'A' on the outer borders since the cross can't appear there
            if i > 0 and i < rows - 1 and j > 0 and j < columns - 1:
                if positive_slope_mas(board, i, j) and negative_slope_mas(board, i, j):
                    count = count + 1
    return count


def positive_slope_mas(board: List[List[str]], i: int, j: int) -> bool:
    if board[i-1][j+1] == 'M' and board[i+1][j-1] == 'S':
        return True
    if board[i-1][j+1] == 'S' and board[i+1][j-1] == 'M':
        return True
    return False


def negative_slope_mas(board: List[List[str]], i: int, j: int) -> bool:
    if board[i-1][j-1] == 'M' and board[i+1][j+1] == 'S':
        return True
    if board[i-1][j-1] == 'S' and board[i+1][j+1] == 'M':
        return True
    return False


def main():
    board = get_board()
    #num_words = find_words(board) # Part 1
    num_words = find_mas_cross(board) # Part 2
    print(num_words)


if __name__ == "__main__":
    main()