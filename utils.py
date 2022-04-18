from board import Board
def isMouseOnBoard(mouse_pos, board: Board):
    return mouse_pos[0] < board.border[0] + board.width and mouse_pos[0] > board.border[0] and \
        mouse_pos[1] < board.border[1] + \
        board.height and mouse_pos[1] > board.border[1]

def getSquare(pos, board: Board):
    row_pos = int((pos[0]-board.border[0])//board.SQUARE_SIZE)
    col_pos = int((pos[1]-board.border[1])//board.SQUARE_SIZE)
    return row_pos, col_pos
