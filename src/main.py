# Default board size
SIZE = 3

# Styles
RED_FG = "\033[91m"
BLUE_FG = "\033[94m"
GREEN_FG = "\033[92m"

RESET = "\033[0m"

# Players
# [color, mark]
PLAYERS = [[RED_FG, "X"], [BLUE_FG, "O"]]
TURN: int = 0

WINNER: int = -1

def create_board(size: int) -> list[list[str]]:
    return [[" " for _ in range(size)] for _ in range(size)]

def print_board(board: list[list[str]]) -> None:
    for row in board:
        print(f"| {" | ".join(row)} |")

def set_cell(board: list[list[str]], cell_no: int, turn: int) -> None:
    # row = (cell_no - 1) // SIZE (len(board))
    # col = (cell_no - 1) % SIZE (len(board))
    size = len(board)
    row, col = (cell_no - 1) // size, (cell_no - 1) % size

    board[row][col] = turn_mark(turn)

def has_mark(board: list[list[str]], cell_no: int) -> bool:
    # row = (cell_no - 1) // SIZE (len(board))
    # col = (cell_no - 1) % SIZE (len(board))
    size = len(board)
    row, col = (cell_no - 1) // size, (cell_no - 1) % size

    return board[row][col] != " " # Space states that the cell is empty

def update_turn():
    # n = len(PLAYERS) = 2
    # TURN = 0 = (0 + 1) % n = 1 % n = 1
    # TURN = 1 = (1 + 1) % n = 2 % n = 0
    global TURN
    TURN = (TURN + 1) % len(PLAYERS)

def horizontal_check(board: list[list[str]], turn: int):
    assert(turn >= 0 or turn < len(PLAYERS)) # Turn is dependent on the number of players

    global WINNER

    [_, mark] = PLAYERS[turn]
    player_mark = turn_mark(turn)

    for row in board:
        matched = 0

        for cell in row:
            # If the cell is not the specified player's mark, break out of the loop
            if cell != player_mark:
                break

            matched += 1

        if matched == len(row):
            WINNER = turn

            for i in range(SIZE):
                row[i] = f"{GREEN_FG}{mark}{RESET}"

            return

def vertical_check(board: list[list[str]], turn: int):
    assert(turn >= 0 or turn < len(PLAYERS)) # Turn is dependent on the number of players

    global WINNER

    [_, mark] = PLAYERS[turn]
    player_mark = turn_mark(turn)

    # [" ", " ", " "]
    # [" ", " ", " "]
    # [" ", " ", " "]

    for i in range(SIZE):
        matched = 0

        for j in range(SIZE):
            cell = board[j][i]
            if cell != player_mark:
                break

            matched += 1

        if matched == SIZE:
            WINNER = turn

            for j in range(SIZE):
                board[j][i] = f"{GREEN_FG}{mark}{RESET}"

            return

def diagonal_check(board: list[list[str]], turn: int):
    assert(turn >= 0 or turn < len(PLAYERS)) # Turn is dependent on the number of players

    global WINNER

    [_,mark] = PLAYERS[turn]
    player_mark = turn_mark(turn)

    # [" ", " ", " "]
    # [" ", " ", " "]
    # [" ", " ", " "]

    # Diagonal [i][i]
    matched = 0
    for i in range(SIZE):
        cell = board[i][i]
        if cell != player_mark:
            break

        matched += 1        

    if matched == SIZE:
        WINNER = turn

        for i in range(SIZE):
            board[i][i] = f"{GREEN_FG}{mark}{RESET}"

        return

    # Anti-Diagonal [i][SIZE - (i + 1)]
    matched = 0
    for i in range(SIZE):
        cell = board[i][SIZE - (i + 1)]
        if cell != player_mark:
            break

        matched += 1

    if matched == SIZE:
        WINNER = turn

        for i in range(SIZE):
            board[i][SIZE - (i + 1)] = f"{GREEN_FG}{mark}{RESET}"

        return

def check_winner(board: list[list[str]], turn: int):
     # Horizontal Check
    horizontal_check(board, turn)
    if WINNER != -1:
        return

    # Vertical Check
    vertical_check(board, turn)
    if WINNER != -1:
        return

    # Diagonal Check
    diagonal_check(board, turn)
    if WINNER != -1:
        return

def has_empty_cells(board: list[list[str]]) -> bool:
    for row in board:
        for cell in row:
            if cell == " ":
                return True

    return False

def turn_mark(turn: int) -> str:
    [color, mark] = PLAYERS[turn]
    return f"{color}{mark}{RESET}"

# Global board
BOARD: list[list[str]] = create_board(SIZE)

def reset():
    global WINNER, BOARD, TURN

    WINNER = -1 # Reset the winner back to -1 (Draw)
    TURN = 0 # Reset turn to whatever turn you want
    BOARD = create_board(SIZE) # Re-create the board

if __name__ == "__main__":
    while True: # Program Loop
        print_board(BOARD)

        while has_empty_cells(BOARD) and WINNER == -1:
            [color, mark] = PLAYERS[TURN]

            # Try to detect invalid inputs
            try:
                cell_no = int(input(f"Enter cell number to place your mark [{color}{mark}{RESET}]: "))

                # Range checker to avoid invalid cell numbers
                if cell_no < 1 or cell_no > (SIZE ** 2):
                    print(f"Invalid cell number: {cell_no}")
                    continue

                # Check if the cell already has a mark
                if (has_mark(BOARD, cell_no)):
                    print(f"Cell number {cell_no} already has a mark!")
                    continue

                set_cell(BOARD, cell_no, TURN)
                check_winner(BOARD, TURN) # Check winner immediately
                print_board(BOARD)
                update_turn()

                continue
                
            except KeyboardInterrupt:
                break

            except Exception as exc:
                print("Invalid cell number!")
                continue

        if WINNER == -1:
            print("DRAW")
        else:
            [color, mark]
            print(f"Winner: {turn_mark(WINNER)}")

        option = input("Play again [Y/N]: ")
        if option.lower() == "y":
            reset() # Reset the game
            continue
        else:
            print("Thank you for playing!")
            break