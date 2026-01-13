class Piece:
    def __init__(self, color):
        self.color = color
        self.radius = 0  # animation

class Pawn(Piece):
    value = 1
    type = "pawn"
    symbol = {"white": "♙", "black": "♟"}

class Rook(Piece):
    value = 5
    type = "rook"
    symbol = {"white": "♖", "black": "♜"}

class Knight(Piece):
    value = 3
    type = "knight"
    symbol = {"white": "♘", "black": "♞"}

class Bishop(Piece):
    value = 3
    type = "bishop"
    symbol = {"white": "♗", "black": "♝"}

class Queen(Piece):
    value = 9
    type = "queen"
    symbol = {"white": "♕", "black": "♛"}

class King(Piece):
    value = 1000
    type = "king"
    symbol = {"white": "♔", "black": "♚"}
