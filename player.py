class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        pass

    def valid_player(self, piece_color):
        if self.color == piece_color:
            return True
        else:
            return False
