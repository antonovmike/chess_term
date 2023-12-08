class Cell:
    def __init__(self, color, piece=None):
        self.color = color
        self.piece = piece

    def __repr__(self):
        if self.piece is None:
            return self.color
        else:
            return self.color[0] + self.piece.__repr__() + self.color[1:]


class Player:
    def __init__(self):
        self.name
        pass


class ChessPiece:
    def __init__(self, color):
        self.type = None
        self.color = color

    def __repr__(self):
        if self.color == "lower":
            return self.type.lower()
        else:
            return self.type.upper()

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        raise NotImplementedError("Subclasses must implement this method")


class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "p"
        self.first_move = True

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        # Pawns can only move forward
        # Pawns can only capture diagonally
        if self.color == "lower":
            forward = 1
        else:
            forward = -1

        if self.first_move:
            valid = (
                dest_row == source_row - 1 * forward
                and dest_col == source_col
                or dest_row == source_row - 2 * forward
                and dest_col == source_col
            )
            if valid:
                self.first_move = False
        else:
            valid = dest_row == source_row - 1 * forward and dest_col == source_col

        # The pawn cannot attack straight forward, only diagonally
        if valid:
            dest_cell = board[dest_row][dest_col]
            if dest_cell.piece is not None:
                return False
        else:
            dest_cell = board[dest_row][dest_col]
            if dest_cell.piece is not None and dest_row == source_row - forward:
                return True

        return valid


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
        if abs(source_row - dest_row) <= 1 and abs(source_col - dest_col) <= 1:
            return True
        else:
            return False


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


def create_board():
    pieces_order = ["r", "h", "b", "q", "k", "b", "h", "r"]
    empty_order = [None for _ in range(8)]

    board = []
    for i in range(8):
        row = []
        for j in range(8):
            color = ":::" if (i + j) % 2 == 0 else "   "
            if i == 0:
                piece = globals()[piece_names[pieces_order[j].upper()]]("upper")
            elif i == 1:
                piece = Pawn("upper")
            elif i >= 6:
                piece = Pawn("lower")
                if i == 7:
                    piece = globals()[piece_names[pieces_order[j]]]("lower")
            else:
                piece = empty_order[j]
            row.append(Cell(color, piece))
        board.append(row)
    return board


board = create_board()


def move_piece():
    upper_losses = []
    lower_losses = []

    while True:
        try:
            source = input("Enter the coordinates of the source cell: ")
            destination = input("Enter the coordinates of the target cell: ")

            if source == 'quit' or destination == 'quit':
                break
            elif source == 'exit' or destination == 'exit':
                break
            elif len(source) != 2 or len(destination) != 2:
                raise ValueError("The coordinates must be one letter and one digit")

            source_row = 8 - int(source[1])
            source_col = ord(source[0]) - ord("a")
            target_row = 8 - int(destination[1])
            target_col = ord(destination[0]) - ord("a")

            if board[source_row][source_col].piece is None:
                raise ValueError("There is no Player 1 piece on this square")

            piece = board[source_row][source_col].piece.type

            if board[target_row][target_col].piece is not None:
                if piece.isupper() and board[target_row][target_col].piece.type.isupper():
                    raise ValueError("Cannot capture a piece of the same case")
                elif piece.islower and board[target_row][target_col].piece.type.islower():
                    raise ValueError("Cannot capture a piece of the same case")
                elif piece.isupper():
                    lost_piece = board[target_row][target_col].piece.type
                    key = piece_names[lost_piece]
                    lower_losses.append(key)
                elif piece.islower():
                    lost_piece = board[target_row][target_col].piece.type
                    key = piece_names[lost_piece.upper()]
                    upper_losses.append(key)

            # Check the piece
            piece = board[source_row][source_col].piece
            if not piece.valid_move(source_row, source_col, target_row, target_col):
                value = piece_names[piece.type]
                raise ValueError(f"Invalid move for {value}")

            board[target_row][target_col].piece = board[source_row][source_col].piece
            board[source_row][source_col].piece = None

            print_board()
            print("Upper Case losses:", *upper_losses, sep=" ")
            print("Lower Case losses:", *lower_losses)

        except ValueError as e:
            print(f"Error: {e}")


def print_board():
    print("  +---+---+---+---+---+---+---+---+")
    for row in range(8):
        print(f"{8 - row} |", end="")
        for col in range(8):
            cell = board[row][col]
            if cell.piece is None:
                print(f"{cell}|", end="")
            else:
                cell = str(cell)
                print(f"{cell[:3]}|", end="")
        print("\n  +---+---+---+---+---+---+---+---+")
    print("    a   b   c   d   e   f   g   h")


print_board()
move_piece()
