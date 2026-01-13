from pieces import *

class Board:
    def __init__(self):
        self.board = [[None]*8 for _ in range(8)]
        self.setup()

    def setup(self):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        # Black pieces
        for i in range(8):
            self.board[0][i] = order[i]("black")
            self.board[1][i] = Pawn("black")
        # White pieces
        for i in range(8):
            self.board[7][i] = order[i]("white")
            self.board[6][i] = Pawn("white")

    def move(self, r1, c1, r2, c2):
        piece = self.board[r1][c1]
        if piece:
            self.board[r2][c2] = piece
            self.board[r1][c1] = None
