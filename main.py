from player import Player
from board import Board
from pieces import Pawn


player_1 = Player("Player 1", "lower")
player_2 = Player("Player 2", "upper")


board_instance = Board()
first_board = board_instance.get_board()


def count_distance(source_row: int, source_col: int, target_row: int, target_col: int):
    horizontal = source_row - target_row
    vertical = source_col - target_col
    print('==>>', horizontal, vertical)


def move_piece():
    upper_pieces = []
    lower_pieces = []
    current_player = player_1

    while True:
        try:
            source = input("Enter the coordinates of the source cell: ").strip().lower()
            destination = input("Enter the coordinates of the target cell: ").strip().lower()

            if source in ("quit", "exit"):
                break
            if destination in ("quit", "exit"):
                break

            if len(source) != 2 or len(destination) != 2:
                raise ValueError("The coordinates must be one letter and one digit")

            if source[0] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                raise ValueError("Source column is wrong")
            if destination[0] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                raise ValueError("Destination column is wrong")
            if int(source[1]) < 1 or int(source[1]) > 8:
                raise ValueError("Source row is wrong")
            if int(destination[1]) < 1 or int(destination[1]) > 8:
                raise ValueError("Destination row is wrong")

            source_row, source_col = (8 - int(source[1]), ord(source[0]) - ord("a"))
            target_row, target_col = (8 - int(destination[1]), ord(destination[0]) - ord("a"))

            piece = first_board[source_row][source_col].piece
            if piece is None:
                raise ValueError(f"There is no {current_player.name} piece on this square")

            if piece.type.lower() != 'h':
                if not piece.validate_move(source_row, source_col, target_row, target_col, first_board):
                    raise ValueError("Invalid move")

            if not current_player.valid_player(piece.color):
                continue

            # Check if the target cell is occupied
            if first_board[target_row][target_col].piece is not None:
                if piece.color == first_board[target_row][target_col].piece.color:
                    raise ValueError("Cannot capture a piece of the same case")
                else:
                    lost_piece = first_board[target_row][target_col].piece.type
                    if piece.color == "upper":
                        upper_pieces.append(lost_piece)
                    else:
                        lower_pieces.append(lost_piece.upper())

            first_board[target_row][target_col].piece = piece
            first_board[source_row][source_col].piece = None

            # Check if Pawn reached the last line
            pawn_piece = first_board[target_row][target_col].piece
            if isinstance(pawn_piece, Pawn):
                pawn_piece.check_reached_edge(target_row, target_col)

            print_board()

            print("Upper Case losses:", *[name.upper() for name in lower_pieces])
            print("Lower Case losses:", *[name.lower() for name in upper_pieces])

            if current_player == player_1:
                current_player = player_2
            else:
                current_player = player_1

        except ValueError as e:
            print(f"Error: {e}")

def print_board():
    print("  +---+---+---+---+---+---+---+---+")
    for row in range(8):
        print(f"{8 - row} |", end="")
        for col in range(8):
            cell = first_board[row][col]
            if cell.piece is None:
                print(f"{cell}|", end="")
            else:
                cell = str(cell)
                print(f"{cell[:3]}|", end="")
        print("\n  +---+---+---+---+---+---+---+---+")
    print("    a   b   c   d   e   f   g   h")


print_board()
move_piece()
