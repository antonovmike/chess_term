class Cell:
    def __init__(self, color, piece=None):
        self.color = color
        self.piece = piece

    def __repr__(self):
        if self.piece is None:
            return self.color
        else:
            return self.color[0] + self.piece.__repr__() + self.color[1:]


class ChessPiece:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        if self.color == 'white':
            return self.type.lower()
        else:
            return self.type.upper()

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        raise NotImplementedError("Subclasses must implement this method")


class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "p"


class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "r"


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


class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "q"


class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.type = "k"


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
    "p": "Pawn"
}


def create_board():
    pieces_order = ['r', 'h', 'b', 'q', 'k', 'b', 'h', 'r']
    empty_order = [None for _ in range(8)]

    board = []
    for i in range(8):
        row = []
        for j in range(8):
            color = ':::' if (i + j) % 2 == 0 else '   '
            if i == 0:
                piece = globals()[piece_names[pieces_order[j].upper()]]('black')
            elif i == 1:
                piece = Pawn('black')
            elif i >= 6:
                piece = globals()[piece_names[pieces_order[j]]]('white') if i == 7 else Pawn('white')
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
            destination = input("Enter the coordinates of the destination cell: ")

            if len(source) != 2 or len(destination) != 2:
                raise ValueError("The coordinates must be one letter and one digit")

            source_row = 8 - int(source[1])
            source_col = ord(source[0]) - ord('a')
            dest_row = 8 - int(destination[1])
            dest_col = ord(destination[0]) - ord('a')

            if board[source_row][source_col].piece is None:
                raise ValueError("There is no Player 1 piece on this square")

            piece = board[source_row][source_col].piece.type

            if board[dest_row][dest_col].piece is not None:
                if piece.isupper() and board[dest_row][dest_col].piece.type.isupper():
                    raise ValueError("Cannot capture a piece of the same case")
                elif piece.isupper():
                    lower_losses.append(board[dest_row][dest_col].piece)
                elif piece.islower():
                    upper_losses.append(board[dest_row][dest_col].piece)

            # Check if the piece is Knight
            piece = board[source_row][source_col].piece
            if not piece.valid_move(source_row, source_col, dest_row, dest_col):
                raise ValueError("Invalid move for the Knight")

            board[dest_row][dest_col].piece = board[source_row][source_col].piece
            board[source_row][source_col].piece = None

            print_board()
            print('Upper Case losses:', upper_losses)
            print('Lower Case losses:', lower_losses)

        except ValueError as e:
            print(f"Error: {e}")


def print_board():
    print('  +---+---+---+---+---+---+---+---+')
    for row in range(8):
        print(f'{8 - row} |', end='')
        for col in range(8):
            cell = board[row][col]
            if cell.piece is None:
                print(f'{cell}|', end='')
            else:
                cell = str(cell)
                print(f'{cell[:3]}|', end='')
        print('\n  +---+---+---+---+---+---+---+---+')
    print('    a   b   c   d   e   f   g   h')


print_board()
move_piece()
