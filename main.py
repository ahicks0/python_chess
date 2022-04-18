import sys
import pygame
import time
from board import Board
from pieces import PIECE_SIZE, King
from random import randint


def isMouseOnBoard(mouse_pos, board: Board):
    return mouse_pos[0] < board.border[0] + board.width and mouse_pos[0] > board.border[0] and \
        mouse_pos[1] < board.border[1] + \
        board.height and mouse_pos[1] > board.border[1]


def getSquare(pos, board: Board):
    row_pos = int((pos[0]-board.border[0])//board.SQUARE_SIZE)
    col_pos = int((pos[1]-board.border[1])//board.SQUARE_SIZE)
    return row_pos, col_pos

def wasPieceSelected():
    try:
        return selected_piece is not None
    except NameError:
        return False

pygame.init()

# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (54, 69, 216)
black =(0, 0, 0)

font = pygame.font.Font('freesansbold.ttf', 32)
 
# create a text surface object,
# on which text is drawn on it.
text = font.render(f"Initialising ... ", True, blue, black)
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
 
# set the center of the rectangular object.
textRect.center = (200,200)
 

speed = [2, 2]

infoObject = pygame.display.Info()
size = width, height = (infoObject.current_w, infoObject.current_h-60)
screen = pygame.display.set_mode(size)

board = Board(screen)
board.draw()
board.init_pieces()
#print(board.board)

def draw_pieces(exc=None):
    for lines in board.board:
        for square in lines:
            if square['piece'] is not None and square['piece'] is not exc :
                screen.blit(square['piece'].piece, (square['left'] + 0.5*(board.SQUARE_SIZE -
                            PIECE_SIZE[0]), square['top'] + 0.5*(board.SQUARE_SIZE - PIECE_SIZE[1])))

draw_pieces()
dragging_piece = False
turn = ["white", "black"]
while 1:
    # Mouse cursor
    mouse_pos_px = pygame.mouse.get_pos()
    # Board square hovered by mouse
    col_pos, row_pos = getSquare(mouse_pos_px, board)
    txt = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # ON CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:
             if isMouseOnBoard(mouse_pos_px, board):
                if board.board[row_pos][col_pos]['piece'] is not None and board.board[row_pos][col_pos]['piece'].color==turn[0]:
                    selected_piece = board.board[row_pos][col_pos]['piece']
                    selected_square = (row_pos, col_pos)
                    # Set possible moves by calling movement method
                    moves = selected_piece.movement(board)

        # ON RELEASE
        if event.type == pygame.MOUSEBUTTONUP:
            if wasPieceSelected():
                screen.fill(black)
                board.draw()
                if (row_pos, col_pos) in moves:
                    # Move piece. Might replace existing Piece. Message ?
                    board.board[row_pos][col_pos]['piece'] = selected_piece
                    board.board[selected_square[0]][selected_square[1]]['piece'] = None
                    selected_piece.position = (row_pos, col_pos)
                    selected_piece.initial = False
                    turn = turn[::-1]
                draw_pieces()
            selected_piece = None
            selected_square = None

    # While click is held with a piece
    if pygame.mouse.get_pressed()[0] and wasPieceSelected():
        if isMouseOnBoard(mouse_pos_px,  board):
            # Draw board
            screen.fill(black)
            board.draw(moves)

            # Draw all pieces except one held
            draw_pieces(selected_piece)

            # Draw held piece centered under cursor
            screen.blit(selected_piece.piece, (int(mouse_pos_px[0]-0.5*PIECE_SIZE[0]), int(mouse_pos_px[1]-0.5*PIECE_SIZE[1])))
    
    text = font.render(f"{turn[0]} to play", True, blue, black)

    # Check if game has ended
    b_king = False
    w_king = False
    for l in range(8):
        for sq in range(8):
            p = board.board[l][sq]["piece"]
            if p is not None and isinstance(p, King):
                if p.color == "black":
                    b_king = True
                else:
                    w_king = True

    if b_king is not w_king:
        winner = "Black" if b_king else "White"
        break
    
    screen.blit(text, textRect)
    pygame.display.flip()

while 1:
    time.sleep(0.08)
    # Idle End
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # End animation
    text = font.render(f"{winner} is the winner !", True, (randint(0,255),randint(0,255),randint(0,255)), black)
    screen.blit(text, textRect)
    pygame.display.flip()