"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Jakub Lada
email: jakub.lada@seznam.cz
"""

def print_board(board: list[list[str]]) -> None:
    """Vyprintuje aktuální stav hracího pole."""
    print("+---+---+---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+---+---+")

def check_winner(board: list[list[str]], player: str) -> bool:
    """Zkontroluje, zda daný hráč vyhrál."""
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def print_rules() -> None:
    """Vyprintuje pravidla hry."""
    print("Welcome to Tic Tac Toe")
    print("="*40)
    print("GAME RULES:")
    print("Each player can place one mark (or stone)")
    print("per turn on the 3x3 grid. The WINNER is")
    print("who succeeds in placing three of their")
    print("marks in a:")
    print("* horizontal,")
    print("* vertical or")
    print("* diagonal row")
    print("="*40)
    print("Let's start the game")

def initialize_board() -> list[list[str]]:
    """Inicializuje prázdné hrací pole."""
    return [[" " for _ in range(3)] for _ in range(3)]

def tic_tac_toe() -> None:
    board = initialize_board()  # Inicializace hracího pole přesunuta do samostatné funkce
    current_player = "X"
    moves = 0  # Počet tahů, sleduje kolik tahů bylo provedeno
    print_rules()  # Pravidla zapouzdřena do samostatné funkce

    while moves < 9:
        print_board(board)
        try:
            # Výzva k zadání vstupu s vysvětlením mapování čísel na pozice
            move = int(input(f"Player {current_player} | Please enter your move number (1-9): ")) - 1
            # Převod z 1-9 na indexy hracího pole
            if not (0 <= move < 9):  # Zjednodušená podmínka pro kontrolu platnosti tahu
                print("Invalid move. Please enter a number between 1 and 9.")
                continue
            row, col = divmod(move, 3)
            if board[row][col] != " ":
                print("This position is already taken. Please choose another.")
                continue
            board[row][col] = current_player
            moves += 1
            if check_winner(board, current_player):
                print_board(board)
                print(f"Congratulations, the player {current_player} WON!")
                return
            current_player = "O" if current_player == "X" else "X"
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    print("It's a draw!")

if __name__ == "__main__":
    tic_tac_toe()
