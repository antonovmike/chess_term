class Piece:
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return self.type


class Cell:
    def __init__(self, color, piece=None):
        self.color = color
        self.piece = piece

    def __repr__(self):
        if self.piece is None:
            return self.color
        else:
            return self.color[0] + self.piece.__repr__() + self.color[1:]


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
    pawns_order = ['p' for _ in range(8)]
    empty_order = [None for _ in range(8)]

    board = []
    for i in range(8):
        row = []
        for j in range(8):
            color = ':::' if (i + j) % 2 == 0 else '   '
            if i == 0:
                piece = Piece(pieces_order[j].upper())
            elif i == 1:
                piece = Piece(pawns_order[j].upper())
            elif i >= 6:
                piece = Piece(pieces_order[j] if i == 7 else pawns_order[j])
            else:
                piece = empty_order[j]
            row.append(Cell(color, piece))
        board.append(row)
    return board


board = create_board()


def move_piece():
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

            # Here we should probably add an algorithm defining the rules
            # of chess piece movement
            piece = board[source_row][source_col].piece.type
            if piece in piece_names:
                print(f"The piece is a {piece_names[piece]}.")

            if board[dest_row][dest_col].piece is not None:
                raise ValueError("The destination cell is already occupied")

            board[dest_row][dest_col].piece = board[source_row][source_col].piece
            board[source_row][source_col].piece = None

            print_board()

        except ValueError as e:
            print(f"Error: {e}")


def print_board():
    # print('Payer 1')
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
    # print('Payer 2')


print_board()
move_piece()
