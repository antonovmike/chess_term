from player import Player
from board import Cell


player_1 = Player("Player 1", "lower")
player_2 = Player("Player 2", "upper")

piece_names = {
    "K": "King",
    "k": "King",
    "Q": "Queen",
    "q": "Queen",
    "R": "Rook",
    "r": "Rook",
    "B": "Bishop",
    "b": "Bishop",
    "H": "Knight",
    "h": "Knight",
    "P": "Pawn",
    "p": "Pawn",
}


class ChessPiece:
    def __init__(self, color):
        self.type = None
        self.color = color

    def __repr__(self):
        return self.type if self.color == "lower" else self.type.upper()

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        raise NotImplementedError("Subclasses must implement this method")


class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "p"
        self.first_move = True

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        forward = 1 if self.color == "lower" else -1

        valid = dest_row == source_row - 1 * forward and dest_col == source_col
        if self.first_move:
            valid = valid or (dest_row == source_row - 2 * forward and dest_col == source_col)
            if valid:
                self.first_move = False

        # The pawn cannot attack straight forward, only diagonally
        if valid:
            dest_cell = first_board[dest_row][dest_col]
            if dest_cell.piece is not None:
                return False
        else:
            dest_cell = first_board[dest_row][dest_col]
            if dest_cell.piece is not None and dest_row == source_row - forward:
                return True

        return valid

    def check_reached_edge(self, dest_row, dest_col):
        if self.color == "lower" and dest_row == 0:
            new_piece = swap_pawn("Lower case", 8)
            first_board[dest_row][dest_col].piece = new_piece
        elif self.color == "upper" and dest_row == 7:
            new_piece = swap_pawn("Upper case", 1)
            first_board[dest_row][dest_col].piece = new_piece


def swap_pawn(case, row):
    piece_type = input("Enter the name of a new piece: r, h, b, or q: ").lower()

    if piece_type in piece_names:
        new_piece = globals()[piece_names[piece_type]](case)
    else:
        print("Wrong input:", piece_type)
        return swap_pawn(case, row)

    return new_piece



class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "r"

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        if source_row == dest_row or source_col == dest_col:
            return True
        else:
            return False


class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "h"

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        if abs(source_row - dest_row) == 2 and abs(source_col - dest_col) == 1:
            return True
        elif abs(source_row - dest_row) == 1 and abs(source_col - dest_col) == 2:
            return True
        else:
            return False


class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "b"

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        if abs(source_row - dest_row) == abs(source_col - dest_col):
            return True
        else:
            return False


class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "q"

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        if source_row == dest_row or source_col == dest_col:
            return True
        elif abs(source_row - dest_row) == abs(source_col - dest_col):
            return True
        else:
            return False


class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "k"

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        print("coordinates", self, source_row, source_col, dest_row, dest_col)
        if source_row - dest_row == 1 and source_col - dest_col == 1:
            return True
        else:
            return False


def count_distance(source_row, source_col, target_row, target_col):
    horizontal = source_row - target_row
    vertical = source_col - target_col
    print('==>>', horizontal, vertical)


def create_board():
    pieces_order = ["r", "h", "b", "q", "k", "b", "h", "r"]
    empty_order = [None] * 8

    board = []
    for row_index in range(8):
        row = []
        for col_index in range(8):
            color = ":::" if (row_index + col_index) % 2 == 0 else "   "
            if row_index == 0:
                piece = globals()[piece_names[pieces_order[col_index].upper()]]("upper")
            elif row_index == 1:
                piece = Pawn("upper")
            elif row_index >= 6:
                piece = Pawn("lower")
                if row_index == 7:
                    piece = globals()[piece_names[pieces_order[col_index]]]("lower")
            else:
                piece = empty_order[col_index]
            row.append(Cell(color, piece))
        board.append(row)
    return board


first_board = create_board()


def move_piece():
    upper_pieces = []
    lower_pieces = []
    current_player = player_1

    while True:
        try:
            source = input("Enter the coordinates of the source cell: ")
            destination = input("Enter the coordinates of the target cell: ")

            if source.lower() in ("quit", "exit"):
                break
            elif len(source) != 2 or len(destination) != 2:
                raise ValueError("The coordinates must be one letter and one digit")

            source_row, source_col = (8 - int(source[1]), ord(source[0]) - ord("a"))
            target_row, target_col = (8 - int(destination[1]), ord(destination[0]) - ord("a"))

            piece = first_board[source_row][source_col].piece
            if piece is None:
                raise ValueError(f"There is no {current_player.name} piece on this square")

            if piece.type.lower() != 'h':
                if not piece.valid_move(source_row, source_col, target_row, target_col):
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

            print("Upper Case losses:", *[name.upper() for name in upper_pieces])
            print("Lower Case losses:", *[name.lower() for name in lower_pieces])

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
