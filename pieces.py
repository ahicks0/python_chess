import pygame
import os

PIECE_SIZE = (64, 75)  # (w,h)


class Pawn:
    def __init__(self, screen, color) -> None:
        self.piece = pygame.image.load(os.path.join(
            os.getcwd(), f"resources/pawn_{color}.png"))
        self.piece = pygame.transform.scale(self.piece, PIECE_SIZE)
        self.position = (-1, -1)
        self.color = color
        self.opposite_color = "white" if self.color == "black" else "black"
        self.initial = True

    def movement(self, board):
        end_pos = []
        # Black goes down => +1; white goes up => -1
        direction = -1 if self.color == "white" else 1

        # Standard. No need to check bottom edge as it will not be a pawn anymore at this point
        if board.board[self.position[0]+direction][self.position[1]]["piece"] is None:
            end_pos.append((self.position[0]+direction, self.position[1]))

        if board.board[self.position[0]+2*direction][self.position[1]]["piece"] is None and self.initial:
            end_pos.append((self.position[0]+2*direction, self.position[1]))

        # Diagonal Left
        if self.position[1] > 0:
            diag_left = board.board[self.position[0] +
                                    direction][self.position[1]-1]["piece"]
            if diag_left is not None and diag_left.color == self.opposite_color:
                end_pos.append(
                    (self.position[0]+direction, self.position[1]-1))

        # Diagonal Right
        if self.position[1] < 7:
            diag_right = board.board[self.position[0] +
                                     direction][self.position[1]+1]["piece"]
            if diag_right is not None and diag_right.color == self.opposite_color:
                end_pos.append(
                    (self.position[0]+direction, self.position[1]+1))

        return end_pos


class King:
    def __init__(self, screen, color) -> None:
        self.piece = pygame.image.load(os.path.join(
            os.getcwd(), f"resources/king_{color}.png"))
        self.piece = pygame.transform.scale(self.piece, PIECE_SIZE)
        self.position = (-1, -1)
        self.color = color
        self.opposite_color = "white" if self.color == "black" else "black"
        self.initial = True

    def movement(self, board):
        end_pos = []
        # Generate list of coords of squares around, then filter
        for i in range(self.position[0]-1, self.position[0]+1+1):
            for j in range(self.position[1]-1, self.position[1]+1+1):
                if i < 0 or j < 0 or i > 7 or j > 7:
                    # Out of board
                    continue
                if (i, j) == self.position:
                    # Initial position
                    continue
                potential_square = board.board[i][j]
                if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                    # Can't take friendly
                    continue
                end_pos.append((i, j))
        return end_pos


class Queen:
    def __init__(self, screen, color) -> None:
        self.piece = pygame.image.load(os.path.join(
            os.getcwd(), f"resources/queen_{color}.png"))
        self.piece = pygame.transform.scale(self.piece, PIECE_SIZE)
        self.position = (-1, -1)
        self.color = color
        self.initial = True

    def movement(self, board):
        # Generate all possible lists
        end_pos = []
        # Up / Down
        for direction in [-1, 1]:
            for i in range(1, 8):
                if self.position[0]-i*direction < 0 or self.position[0]-i*direction > 7:
                    # Out of board
                    continue
                potential_square = board.board[self.position[0] -
                                               i*direction][self.position[1]]
                if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                    # Can't take friendly
                    break

                if potential_square['piece'] is not None and potential_square['piece'].color != self.color:
                    # Can take and stop
                    end_pos.append(
                        (self.position[0]-i*direction, self.position[1]))
                    break
                end_pos.append(
                    (self.position[0]-i*direction, self.position[1]))

        # Left / Right
        for direction in [-1, 1]:
            for i in range(1, 8):
                if self.position[1]-i*direction < 0 or self.position[1]-i*direction > 7:
                    continue
                potential_square = board.board[self.position[0]
                                               ][self.position[1]-i*direction]
                if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                    # Can't take friendly
                    break

                if potential_square['piece'] is not None and potential_square['piece'].color != self.color:
                    # Can take and stop
                    end_pos.append(
                        (self.position[0], self.position[1]-i*direction))
                    break
                end_pos.append(
                    (self.position[0], self.position[1]-i*direction))

        # Diagonals
        for direction_row in [-1, 1]:
            for direction_col in [-1, 1]:
                for i in range(1, 8):
                    if self.position[1]-i*direction_col < 0 or self.position[1]-i*direction_col > 7 or self.position[0]-i*direction_row < 0 or self.position[0]-i*direction_row > 7:
                        # Out of board
                        continue
                    potential_square = board.board[self.position[0] -
                                                   i*direction_row][self.position[1]-i*direction_col]
                    if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                        # Can't take friendly
                        break

                    if potential_square['piece'] is not None and potential_square['piece'].color != self.color:
                        # Can take and stop
                        end_pos.append(
                            (self.position[0]-i*direction_row, self.position[1]-i*direction_col))
                        break
                    end_pos.append(
                        (self.position[0]-i*direction_row, self.position[1]-i*direction_col))
        return end_pos


class Knight:
    def __init__(self, screen, color) -> None:
        self.piece = pygame.image.load(os.path.join(
            os.getcwd(), f"resources/knight_{color}.png"))
        self.piece = pygame.transform.scale(self.piece, PIECE_SIZE)
        self.position = (-1, -1)
        self.color = color
        self.initial = True

    def movement(self, board):
        end_pos = []
        for direction_row in [-1, 1]:
            for direction_col in [-1, 1]:
                if self.position[1]-direction_col < 0 or self.position[1]-direction_col > 7 or self.position[0] - 2*direction_row < 0 or self.position[0] - 2 * direction_row > 7:
                    # Out of board
                    continue
                potential_square = board.board[self.position[0] -
                                               2*direction_row][self.position[1]-direction_col]
                if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                    # Can't take friendly
                    continue
                end_pos.append(
                    (self.position[0] - 2*direction_row, self.position[1]-direction_col))

        for direction_row in [-1, 1]:
            for direction_col in [-1, 1]:
                if self.position[1]-2*direction_col < 0 or self.position[1]-2*direction_col > 7 or self.position[0] - direction_row < 0 or self.position[0] - direction_row > 7:
                    # Out of board
                    continue
                potential_square = board.board[self.position[0] -direction_row][self.position[1]-2*direction_col]
                if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                    # Can't take friendly
                    continue
                end_pos.append(
                    (self.position[0] - direction_row, self.position[1]-2*direction_col))

        return end_pos


class Bishop:
    def __init__(self, screen, color) -> None:
        self.piece = pygame.image.load(os.path.join(
            os.getcwd(), f"resources/bishop_{color}.png"))
        self.piece = pygame.transform.scale(self.piece, PIECE_SIZE)
        self.position = (-1, -1)
        self.color = color
        self.initial = True

    def movement(self, board):
        # Diagonals
        end_pos = []
        for direction_row in [-1, 1]:
            for direction_col in [-1, 1]:
                for i in range(1, 8):
                    if self.position[1]-i*direction_col < 0 or self.position[1]-i*direction_col > 7 or self.position[0]-i*direction_row < 0 or self.position[0]-i*direction_row > 7:
                        # Out of board
                        continue
                    potential_square = board.board[self.position[0] -
                                                   i*direction_row][self.position[1]-i*direction_col]
                    if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                        # Can't take friendly
                        break

                    if potential_square['piece'] is not None and potential_square['piece'].color != self.color:
                        # Can take and stop
                        end_pos.append(
                            (self.position[0]-i*direction_row, self.position[1]-i*direction_col))
                        break
                    end_pos.append(
                        (self.position[0]-i*direction_row, self.position[1]-i*direction_col))
        return end_pos


class Rook:
    def __init__(self, screen, color) -> None:
        self.piece = pygame.image.load(os.path.join(
            os.getcwd(), f"resources/rook_{color}.png"))
        self.piece = pygame.transform.scale(self.piece, PIECE_SIZE)
        self.position = (-1, -1)
        self.color = color
        self.initial = True

    def movement(self, board):
        end_pos = []
        # Up / Down
        for direction in [-1, 1]:
            for i in range(1, 8):
                if self.position[0]-i*direction < 0 or self.position[0]-i*direction > 7:
                    # Out of board
                    continue
                potential_square = board.board[self.position[0] -
                                               i*direction][self.position[1]]
                if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                    # Can't take friendly
                    break

                if potential_square['piece'] is not None and potential_square['piece'].color != self.color:
                    # Can take and stop
                    end_pos.append(
                        (self.position[0]-i*direction, self.position[1]))
                    break
                end_pos.append(
                    (self.position[0]-i*direction, self.position[1]))

        # Left / Right
        for direction in [-1, 1]:
            for i in range(1, 8):
                if self.position[1]-i*direction < 0 or self.position[1]-i*direction > 7:
                    continue
                potential_square = board.board[self.position[0]
                                               ][self.position[1]-i*direction]
                if potential_square['piece'] is not None and potential_square['piece'].color == self.color:
                    # Can't take friendly
                    break

                if potential_square['piece'] is not None and potential_square['piece'].color != self.color:
                    # Can take and stop
                    end_pos.append(
                        (self.position[0], self.position[1]-i*direction))
                    break
                end_pos.append(
                    (self.position[0], self.position[1]-i*direction))
        return end_pos
