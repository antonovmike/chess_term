from pieces import Bishop, ChessPiece, King, Knight, Pawn, Rook, Queen, piece_names


class Cell:
    def __init__(self, color: str, piece=None):
        self.color = color
        self.piece = piece

    def __repr__(self):
        if self.piece is None:
            return self.color
        else:
            return self.color[0] + self.piece.__repr__() + self.color[1:]


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
                piece = Pawn("upper", board)
            elif row_index >= 6:
                piece = Pawn("lower", board)
                if row_index == 7:
                    piece = globals()[piece_names[pieces_order[col_index]]]("lower")
            else:
                piece = empty_order[col_index]
            row.append(Cell(color, piece))
        board.append(row)
    return board
