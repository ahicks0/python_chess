from typing import Tuple
import pygame
from pygame import Rect, Surface
from pieces import *



class Board:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.SQUARE_SIZE = 100
        self.board = []
        self.border = (0,0)
        self.width = self.SQUARE_SIZE*8
        self.height = self.SQUARE_SIZE*8

    def draw(self, highlight = []):
        nb_squares = 8

        w, h = self.screen.get_size()
        offset = self.SQUARE_SIZE*nb_squares/2
        first = True
        for line in range(nb_squares):
            col_list = [(102, 51, 0), (236, 217, 198)]
            col = col_list if line % 2 == 0 else col_list[::-1]
            tmp = []
            for square in range(nb_squares):
                left = w/2-offset + square*self.SQUARE_SIZE
                top = h/2-offset + line*self.SQUARE_SIZE
                if first:
                    self.border = (left,top)
                    first = False
                tmp.append({'left':left, 'top':top, 'piece':None})
                r = Rect(left, top, self.SQUARE_SIZE, self.SQUARE_SIZE)

                # Highlight Square
                if (line, square) in highlight:
                    pygame.draw.rect(self.screen, (77, 184, 59), r)
                else:
                    pygame.draw.rect(self.screen, col[square % 2], r)
            self.board.append(tmp)

    def draw_pieces(self, exc=None):
        for lines in self.board:
            for square in lines:
                if square['piece'] is not None and square['piece'] is not exc :
                    self.screen.blit(square['piece'].piece, (square['left'] + 0.5*(self.SQUARE_SIZE -
                                PIECE_SIZE[0]), square['top'] + 0.5*(self.SQUARE_SIZE - PIECE_SIZE[1])))

    def init_pieces(self):
        c = "black"
        pieces = [Rook(c), Knight(c), Bishop(c), Queen(c), King(c), Bishop(c), Knight(c), Rook(c)]

        pawns = [Pawn(c),Pawn(c),Pawn(c),Pawn(c),Pawn(c),Pawn(c),Pawn(c),Pawn(c)]

        for i, (square,piece) in enumerate(zip(self.board[0],pieces)):
            square.update({"piece":piece})
            piece.position = (0,i)

        for i, (square,piece) in enumerate(zip(self.board[1],pawns)):
            square.update({"piece":piece})
            piece.position = (1,i)

        c = "white"
        pieces = [Rook(c), Knight(c), Bishop(c), Queen(c), King(c), Bishop(c), Knight(c), Rook(c)]

        pawns = [Pawn(c),Pawn(c),Pawn(c),Pawn(c),Pawn(c),Pawn(c),Pawn(c),Pawn(c)]

        for i,(square,piece) in enumerate(zip(self.board[-1],pieces[::-1])):
            square['piece'] = piece
            piece.position = (7,i)

        for i,(square,piece) in enumerate(zip(self.board[-2],pawns)):
            square['piece'] = piece
            piece.position = (6,i)
