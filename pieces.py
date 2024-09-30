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
    def __init__(self, color: str):
        self.type = None
        self.color = color

    def __repr__(self):
        return self.type if self.color == "lower" else self.type.upper()

    def valid_move(self, source_row, source_col, dest_row, dest_col):
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def swap_pawn(case: str, row: int):
        piece_type = input("Enter the name of a new piece: r, h, b, or q: ").lower()
        if piece_type in piece_names:
            new_piece = globals()[piece_names[piece_type]](case)
        else:
            print("Wrong input:", piece_type)
            return ChessPiece.swap_pawn(case, row)
        return new_piece


class Pawn(ChessPiece):
    def __init__(self, color: str, board: str):
        super().__init__(color)
        self.type = "p"
        self.first_move = True
        self.board = board

    def valid_move(self, source_row: int, source_col: int, dest_row: int, dest_col: int, board: str):
        forward = 1 if self.color == "lower" else -1

        valid = dest_row == source_row - 1 * forward and dest_col == source_col
        if self.first_move:
            valid = valid or (dest_row == source_row - 2 * forward and dest_col == source_col)
            if valid:
                self.first_move = False

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

    def check_reached_edge(self, dest_row: int, dest_col: int):
        if self.color == "lower" and dest_row == 0:
            new_piece = ChessPiece.swap_pawn("Lower case", 8)
            self.board[dest_row][dest_col].piece = new_piece
        elif self.color == "upper" and dest_row == 7:
            new_piece = ChessPiece.swap_pawn("Upper case", 1)
            self.board[dest_row][dest_col].piece = new_piece


class Rook(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)
        self.type = "r"

    def valid_move(self, source_row: int, source_col: int, dest_row: int, dest_col: int):
        if source_row == dest_row or source_col == dest_col:
            return True
        else:
            return False


class Knight(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)
        self.type = "h"

    def valid_move(self, source_row: int, source_col: int, dest_row: int, dest_col: int):
        if abs(source_row - dest_row) == 2 and abs(source_col - dest_col) == 1:
            return True
        elif abs(source_row - dest_row) == 1 and abs(source_col - dest_col) == 2:
            return True
        else:
            return False


class Bishop(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)
        self.type = "b"

    def valid_move(self, source_row: int, source_col: int, dest_row: int, dest_col: int):
        if abs(source_row - dest_row) == abs(source_col - dest_col):
            return True
        else:
            return False


class Queen(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)
        self.type = "q"

    def valid_move(self, source_row: int, source_col: int, dest_row: int, dest_col: int):
        if source_row == dest_row or source_col == dest_col:
            return True
        elif abs(source_row - dest_row) == abs(source_col - dest_col):
            return True
        else:
            return False


class King(ChessPiece):
    def __init__(self, color: str):
        super().__init__(color)
        self.type = "k"

    def valid_move(self, source_row: int, source_col: int, dest_row: int, dest_col: int):
        print("coordinates", self, source_row, source_col, dest_row, dest_col)
        if source_row - dest_row == 1 and source_col - dest_col == 1:
            return True
        else:
            return False
