

import pygame
from board import Board
from pieces import *
import random

# --- MENU & TEXT DRAWING ---

def draw_text_center(win, text, size, color, pos):
    font = pygame.font.SysFont("comicsans", size)
    render = font.render(text, True, color)
    rect = render.get_rect(center=pos)
    win.blit(render, rect)

class Button:
    def __init__(self, x, y, w, h, text, color, highlight_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.highlight_color = highlight_color
        self.selected = False

    def draw(self, win):
        clr = self.highlight_color if self.selected else self.color
        pygame.draw.rect(win, clr, self.rect)
        draw_text_center(win, self.text, 30, (0,0,0), self.rect.center)

    def is_hover(self, pos):
        return self.rect.collidepoint(pos)


def menu():
    easy_btn = Button(100, 250, 120, 50, "EASY", (200,200,200), (100,255,100))
    med_btn = Button(260, 250, 120, 50, "MEDIUM", (200,200,200), (255,255,100))
    hard_btn = Button(420, 250, 120, 50, "HARD", (200,200,200), (255,100,100))
    start_btn = Button(260, 350, 120, 50, "START", (100,100,255), (100,200,255))

    difficulty = "easy"
    run = True
    while run:
        WIN.fill((50,50,50))
        draw_text_center(WIN, "CHESS GAME", 60, (255,255,255), (WIDTH//2, 150))
        # Draw buttons
        for btn in [easy_btn, med_btn, hard_btn, start_btn]:
            btn.draw(WIN)
        pygame.display.update()

        mx,my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # difficulty buttons
                if easy_btn.is_hover((mx,my)):
                    difficulty="easy"
                elif med_btn.is_hover((mx,my)):
                    difficulty="medium"
                elif hard_btn.is_hover((mx,my)):
                    difficulty="hard"
                elif start_btn.is_hover((mx,my)):
                    return difficulty

        # Highlight selected difficulty
        easy_btn.selected = (difficulty=="easy")
        med_btn.selected = (difficulty=="medium")
        hard_btn.selected = (difficulty=="hard")

# --- SETTINGS ---
WIDTH = HEIGHT = 640
SQUARE_SIZE = WIDTH // 8

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
FONT = pygame.font.SysFont("segoeuisymbol", 48)

# --- GAME STATE ---



# --- GAME STATE ---
difficulty = menu()  # show menu before game starts
board = Board()
selected = None
legal_moves = []
ai_thinking = False
ai_timer = 0
turn = "white"  # "white" = player, "black" = AI


# --- DRAW FUNCTIONS ---
def draw_board(win):
    colors = [(240, 217, 181), (181, 136, 99)]
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(win, colors[(row+col)%2], 
                             (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_turn_indicator(win, turn):
    overlay = pygame.Surface((WIDTH, HEIGHT//2), pygame.SRCALPHA)
    if turn == "white":
        overlay.fill((255,255,255,30))  # soft white glow for player
        win.blit(overlay, (0, HEIGHT//2))  # bottom half
    else:
        overlay.fill((0,0,0,30))  # soft black glow for AI
        win.blit(overlay, (0, 0))  # top half

def draw_hover(win):
    mx, my = pygame.mouse.get_pos()
    row, col = my // SQUARE_SIZE, mx // SQUARE_SIZE
    if 0 <= row < 8 and 0 <= col < 8:
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill((100,150,255,60))
        win.blit(s, (col*SQUARE_SIZE, row*SQUARE_SIZE))

def draw_legal_moves(win, moves):
    for r, c in moves:
        cx, cy = c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2
        pygame.draw.circle(win, (0,255,0), (cx, cy), 10)

import math
def draw_selection(win, pos, turn):
    if pos:
        r, c = pos
        cx, cy = c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2
        # Only pulse for active player
        if (turn == "white" and r >= 4) or (turn == "black" and r < 4):
            radius = 30 + int(5 * math.sin(pygame.time.get_ticks()/200))
            pygame.draw.circle(win, (255,215,0), (cx, cy), radius, 3)
        else:
            pygame.draw.circle(win, (255,215,0), (cx, cy), 30, 3)

def draw_unicode_pieces(win, board):
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            if piece:
                # pop-in animation
                if piece.radius < 48:
                    piece.radius += 3
                x, y = c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2
                symbol = piece.symbol[piece.color]

                # shadow for contrast
                shadow = FONT.render(symbol, True, (0,0,0))
                win.blit(shadow, shadow.get_rect(center=(x+2,y+2)))

                # outline for white pieces on white squares
                outline_color = (20,20,20) if piece.color=="white" else (230,230,230)
                for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    outline = FONT.render(symbol, True, outline_color)
                    win.blit(outline, outline.get_rect(center=(x+dx,y+dy)))

                # main symbol
                text = FONT.render(symbol, True, (245,245,245) if piece.color=="white" else (30,30,30))
                win.blit(text, text.get_rect(center=(x,y)))

# --- MOVE LOGIC FOR EACH PIECE ---
def king_moves(board, row, col):
    moves = []
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr==0 and dc==0: continue
            r,c = row+dr, col+dc
            if 0<=r<8 and 0<=c<8:
                target = board.board[r][c]
                if not target or target.color != board.board[row][col].color:
                    moves.append((r,c))
    return moves

def rook_moves(board, row, col):
    moves=[]
    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        r,c=row+dr,col+dc
        while 0<=r<8 and 0<=c<8:
            target=board.board[r][c]
            if not target: moves.append((r,c))
            elif target.color!=board.board[row][col].color: moves.append((r,c)); break
            else: break
            r+=dr;c+=dc
    return moves

def bishop_moves(board,row,col):
    moves=[]
    for dr,dc in [(1,1),(1,-1),(-1,1),(-1,-1)]:
        r,c=row+dr,col+dc
        while 0<=r<8 and 0<=c<8:
            target=board.board[r][c]
            if not target: moves.append((r,c))
            elif target.color!=board.board[row][col].color: moves.append((r,c)); break
            else: break
            r+=dr;c+=dc
    return moves

def knight_moves(board,row,col):
    moves=[]
    for dr,dc in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
        r,c=row+dr,col+dc
        if 0<=r<8 and 0<=c<8:
            target=board.board[r][c]
            if not target or target.color!=board.board[row][col].color: moves.append((r,c))
    return moves

def pawn_moves(board,row,col):
    moves=[]
    piece=board.board[row][col]
    dir=-1 if piece.color=="white" else 1
    start_row=6 if piece.color=="white" else 1
    # forward
    if 0<=row+dir<8 and board.board[row+dir][col] is None:
        moves.append((row+dir,col))
        if row==start_row and board.board[row+2*dir][col] is None:
            moves.append((row+2*dir,col))
    # captures
    for dc in [-1,1]:
        r,c=row+dir,col+dc
        if 0<=r<8 and 0<=c<8:
            target=board.board[r][c]
            if target and target.color!=piece.color:
                moves.append((r,c))
    return moves

def get_legal_moves(board,row,col):
    piece=board.board[row][col]
    if not piece: return []
    if piece.type=="king": return king_moves(board,row,col)
    elif piece.type=="queen": return rook_moves(board,row,col)+bishop_moves(board,row,col)
    elif piece.type=="rook": return rook_moves(board,row,col)
    elif piece.type=="bishop": return bishop_moves(board,row,col)
    elif piece.type=="knight": return knight_moves(board,row,col)
    elif piece.type=="pawn": return pawn_moves(board,row,col)
    return []


# --- AI MOVE FUNCTION ---

# --- AI MOVE FUNCTION ---
def ai_move(board):
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            if piece and piece.color=="black":
                legal = get_legal_moves(board,r,c)
                for move in legal:
                    moves.append(((r,c),move))
    if not moves:
        return

    if difficulty=="easy":
        move = random.choice(moves)
    elif difficulty=="medium":
        # prefer captures if available
        capture_moves = [m for m in moves if board.board[m[1][0]][m[1][1]]]
        move = random.choice(capture_moves) if capture_moves else random.choice(moves)
    elif difficulty=="hard":
        # simple evaluation: capture highest value piece if possible
        capture_moves = []
        for m in moves:
            target = board.board[m[1][0]][m[1][1]]
            if target:
                capture_moves.append((m, target.value))
        if capture_moves:
            # choose move that captures highest value
            capture_moves.sort(key=lambda x:x[1], reverse=True)
            move = capture_moves[0][0]
        else:
            move = random.choice(moves)

    # execute move
    r1,c1 = move[0]
    r2,c2 = move[1]
    board.move(r1,c1,r2,c2)
    moved_piece = board.board[r2][c2]
    if moved_piece.type=="pawn" and r2==0:
        board.board[r2][c2] = Queen("black")

# --- MAIN LOOP ---
run=True
clock=pygame.time.Clock()



while run:
    clock.tick(60)

    # AI move after delay, only on black's turn
    if turn == "black" and ai_thinking and pygame.time.get_ticks() >= ai_timer:
        ai_move(board)
        ai_thinking = False
        turn = "white"  # switch back to player


    draw_board(WIN)
    draw_turn_indicator(WIN, turn)
    draw_hover(WIN)
    draw_legal_moves(WIN, legal_moves)
    draw_selection(WIN, selected, turn)
    draw_unicode_pieces(WIN, board)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT: run=False
        # Only allow player input on white's turn
        if event.type==pygame.MOUSEBUTTONDOWN and turn == "white":
            mx,my=pygame.mouse.get_pos()
            row,col=my//SQUARE_SIZE,mx//SQUARE_SIZE
            piece=board.board[row][col]

            if selected:
                if (row,col) in legal_moves:
                    r1,c1=selected
                    board.move(r1,c1,row,col)
                    # Pawn promotion
                    moved_piece=board.board[row][col]
                    if moved_piece.type=="pawn" and (row==0 or row==7):
                        board.board[row][col]=Queen(moved_piece.color)
                    # Start AI thinking timer
                    ai_thinking = True
                    ai_timer = pygame.time.get_ticks() + 2000
                    turn = "black"  # switch to AI
                selected=None
                legal_moves=[]
            elif piece:
                selected=(row,col)
                legal_moves=get_legal_moves(board,row,col)
