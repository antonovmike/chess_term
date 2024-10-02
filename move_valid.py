import pieces

class MoveValidator:
    def valid_move(self, source_row: int, source_col: int, dest_row: int, dest_col: int, board: str):
        raise NotImplementedError("Subclasses must implement this method")

class ChessPieceValidator(MoveValidator):
    @staticmethod
    def swap_pawn(case: str, row: int):
        piece_type = input("Enter the name of a new piece: r, h, b, or q: ").lower()
        if piece_type in pieces.piece_names:
            new_piece = globals()[pieces.piece_names[piece_type]](case)
        else:
            print("Wrong input:", piece_type)
            return ChessPieceValidator.swap_pawn(case, row)
        return new_piece

class PawnValidator(MoveValidator):
    def __init__(self, color: str, board):
        self.color = color
        self.type = "p"
        self.first_move = True
        self.board = board

    def valid_move(self, source_row: int, source_col: int, dest_row: int, dest_col: int, board):
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
            new_piece = ChessPieceValidator.swap_pawn("Lower case", 8)
            self.board[dest_row][dest_col].piece = new_piece
        elif self.color == "upper" and dest_row == 7:
            new_piece = ChessPieceValidator.swap_pawn("Upper case", 1)
            self.board[dest_row][dest_col].piece = new_piece
