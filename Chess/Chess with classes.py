import pygame

# grid colors
# 1 is square the piece is from
# 2 square can be advanced to
# 3 square can be captured
# 4 2 squares up pawns
# 5 Castling to the left
# 6 Castling to the right

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CHESS_WHITE = (238, 238, 210)
CHESS_BLACK = (118, 150, 86)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (169, 169, 169)
GRID_H, GRID_W = 64, 64
PIECE_TUPLE = ('R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R')
PIECE_DICT = {0: 'P', 1: 'R', 2: 'N', 3: 'B', 4: 'Q', 5: 'K'}
# PIECE_DICT = {'Pawn': 0, 'Rook': 1, 'Knight': 2, 'Bishop': 3, 'Queen': 4, 'King': 5}
FPS = 120


def get_key(val) -> int:
    for key, value in PIECE_DICT.items():
        if val == value:
            return key


#  to split the images into equal squares
def load_tile_table(image) -> list:
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width // 64):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height // 64):
            rect = (tile_x * 64, tile_y * 64, 64, 64)
            line.append(image.subsurface(rect))
    return tile_table


class ChessMove:
    """Class used to record the chess movements"""

    def __init__(self, piece: int, from_coord: tuple = (0, 0), to_coord: tuple = (0, 0), capture: bool = False,
                 en_passant_capture: bool = False, castling_flag: bool = False, en_passant_flag: bool = False,
                 queen_castle: bool = False, king_castle: bool = False,
                 check: bool = False, mate: bool = False):
        self.piece = piece
        self.x_from, self.y_from = from_coord
        self.x_to, self.y_to = to_coord
        self.capture = capture;
        self.en_passant_capture = en_passant_capture
        self.castling_flag = castling_flag;
        self.en_passant_flag = en_passant_flag
        self.queen_castle = queen_castle;
        self.king_castle = king_castle
        self.check = check;
        self.mate = mate
        self.promotion = 0


class Piece:
    """The super class for the pieces"""

    def __init__(self, color: bool, row: int, column: int):
        self.color = color
        self.row = row
        self.column = column
        self.num = 0
        self.castling = False
        self.en_passant = False

    def set_row(self, row: int):
        self.row = row

    def set_column(self, column: int):
        self.column = column

    def can_move_to(self, board):
        pass


class Pawn(Piece):
    def __init__(self, color: bool, row: int, column: int):
        super().__init__(color, row, column)

    def can_move_to(self, board):
        grid_x, grid_y = self.row, self.column
        if not self.color:
            if grid_y < 7:
                if (board.grid[grid_x - 1][grid_y + 1] and board.grid[grid_x - 1][grid_y + 1].color) \
                        or (board.grid[grid_x][grid_y + 1] and board.grid[grid_x][
                    grid_y + 1].en_passant):  # If can capture to the right
                    last_piece = board.grid[grid_x - 1][grid_y + 1]
                    board.grid[grid_x - 1][grid_y + 1] = self
                    if not board.is_king_in_check(False):
                        board.grid_color[grid_x - 1][grid_y + 1] = 3
                    board.grid[grid_x - 1][grid_y + 1] = last_piece
            if 0 < grid_y:
                if board.grid[grid_x - 1][grid_y - 1] and board.grid[grid_x - 1][grid_y - 1].color \
                        or (board.grid[grid_x][grid_y - 1] and board.grid[grid_x][
                    grid_y - 1].en_passant):  # If can capture to the right:  # or left, color red
                    last_piece = board.grid[grid_x - 1][grid_y - 1]
                    board.grid[grid_x - 1][grid_y - 1] = self
                    if not board.is_king_in_check(False):
                        board.grid_color[grid_x - 1][grid_y - 1] = 3
                    board.grid[grid_x - 1][grid_y - 1] = last_piece
            if grid_x == 6:  # First movement for white pawn
                if board.grid[grid_x - 1][grid_y] == 0:  # If nothing ahead of it
                    board.grid[grid_x - 1][grid_y] = self  # put the pawn there
                    if not board.is_king_in_check(board.player_turn):  # and check if it makes check
                        board.grid_color[grid_x - 1][grid_y] = 2  # then color it blue
                    board.grid[grid_x - 1][grid_y] = 0  # Remove the pawn from the square ahead
                    if board.grid[grid_x - 2][grid_y] == 0:
                        board.grid[grid_x - 2][grid_y] = self
                        if not board.is_king_in_check(board.player_turn):
                            board.grid_color[grid_x - 2][grid_y] = 4
                        board.grid[grid_x - 2][grid_y] = 0
            else:  # Other movements
                if board.grid[grid_x - 1][grid_y] == 0:
                    board.grid[grid_x - 1][grid_y] = self
                    if not board.is_king_in_check(board.player_turn):
                        board.grid_color[grid_x - 1][grid_y] = 2
                    board.grid[grid_x - 1][grid_y] = 0
        elif self.color:
            if grid_y < 7:
                if (board.grid[grid_x + 1][grid_y + 1] and not board.grid[grid_x + 1][grid_y + 1].color) \
                        or (board.grid[grid_x][grid_y + 1] and board.grid[grid_x][
                    grid_y + 1].en_passant):  # If can capture to the right
                    last_piece = board.grid[grid_x + 1][grid_y + 1]
                    board.grid[grid_x + 1][grid_y + 1] = self
                    if not board.is_king_in_check(True):
                        board.grid_color[grid_x + 1][grid_y + 1] = 3
                    board.grid[grid_x + 1][grid_y + 1] = last_piece
            if 0 < grid_y:
                if (board.grid[grid_x + 1][grid_y - 1] and not board.grid[grid_x + 1][grid_y - 1].color) \
                        or (board.grid[grid_x][grid_y - 1] and board.grid[grid_x][
                    grid_y - 1].en_passant):  # or left, color red
                    last_piece = board.grid[grid_x + 1][grid_y - 1]
                    board.grid[grid_x + 1][grid_y - 1] = self
                    if not board.is_king_in_check(True):
                        board.grid_color[grid_x + 1][grid_y - 1] = 3
                    board.grid[grid_x + 1][grid_y - 1] = last_piece
            if grid_x == 1:  # First movement for black pawn
                if board.grid[grid_x + 1][grid_y] == 0:
                    board.grid[grid_x + 1][grid_y] = self
                    if not board.is_king_in_check(board.player_turn):
                        board.grid_color[grid_x + 1][grid_y] = 2
                    board.grid[grid_x + 1][grid_y] = 0
                    if board.grid[grid_x + 2][grid_y] == 0:
                        board.grid[grid_x + 2][grid_y] = self
                        if not board.is_king_in_check(board.player_turn):
                            board.grid_color[grid_x + 2][grid_y] = 4
                        board.grid[grid_x + 2][grid_y] = 0
            else:  # Other movements
                if board.grid[grid_x + 1][grid_y] == 0:
                    board.grid[grid_x + 1][grid_y] = self
                    if not board.is_king_in_check(board.player_turn):
                        board.grid_color[grid_x + 1][grid_y] = 2
                    board.grid[grid_x + 1][grid_y] = 0


class Rook(Piece):
    def __init__(self, color: bool, row: int, column: int):
        super().__init__(color, row, column)
        self.num = 1
        self.castling = True

    def can_move_to(self, board):
        super().can_move_to(board)
        grid_x, grid_y = self.row, self.column
        while grid_x < 7:
            grid_x += 1
            if board.grid[grid_x][grid_y] == 0:  # If nothing there, color blue and keep going
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 2
                board.grid[grid_x][grid_y] = 0
            elif board.grid[grid_x][grid_y].color != self.color:  # If enemy, color red and stop
                last_piece = board.grid[grid_x][grid_y]
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 3
                board.grid[grid_x][grid_y] = last_piece
                break
            elif board.grid[grid_x][grid_y].color == self.color:  # If friendly, stop
                break
        grid_x, grid_y = self.row, self.column
        while grid_x > 0:
            grid_x -= 1
            if board.grid[grid_x][grid_y] == 0:  # If nothing there, color blue and keep going
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 2
                board.grid[grid_x][grid_y] = 0
            elif board.grid[grid_x][grid_y].color != self.color:  # If enemy, color red and stop
                last_piece = board.grid[grid_x][grid_y]
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 3
                board.grid[grid_x][grid_y] = last_piece
                break
            elif board.grid[grid_x][grid_y].color == self.color:  # If friendly, stop
                break
        grid_x, grid_y = self.row, self.column
        while grid_y < 7:
            grid_y += 1
            if board.grid[grid_x][grid_y] == 0:  # If nothing there, color blue and keep going
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 2
                board.grid[grid_x][grid_y] = 0
            elif board.grid[grid_x][grid_y].color != self.color:  # If enemy, color red and stop
                last_piece = board.grid[grid_x][grid_y]
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 3
                board.grid[grid_x][grid_y] = last_piece
                break
            elif board.grid[grid_x][grid_y].color == self.color:  # If friendly, stop
                break
        grid_x, grid_y = self.row, self.column
        while grid_y > 0:
            grid_y -= 1
            if board.grid[grid_x][grid_y] == 0:  # If nothing there, color blue and keep going
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 2
                board.grid[grid_x][grid_y] = 0
            elif board.grid[grid_x][grid_y].color != self.color:  # If enemy, color red and stop
                last_piece = board.grid[grid_x][grid_y]
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 3
                board.grid[grid_x][grid_y] = last_piece
                break
            elif board.grid[grid_x][grid_y].color == self.color:  # If friendly, stop
                break


class Knight(Piece):
    def __init__(self, color: bool, row: int, column: int):
        super().__init__(color, row, column)
        self.num = 2

    def can_move_to(self, board):
        for x in range(-2, 3):
            for y in range(-2, 3):
                if x != 0 and y != 0 and abs(x) != abs(y):
                    if 0 <= self.row + x < 8 and 0 <= self.column + y < 8:
                        if board.grid[self.row + x][self.column + y] == 0:  # If nothing there, color blue
                            board.grid[self.row + x][self.column + y] = self
                            if not board.is_king_in_check(board.player_turn):
                                board.grid_color[self.row + x][self.column + y] = 2
                            board.grid[self.row + x][self.column + y] = 0
                        elif board.grid[self.row + x][self.column + y].color != self.color:  # If enemy, color red
                            last_piece = board.grid[self.row + x][self.column + y]
                            board.grid[self.row + x][self.column + y] = self
                            if not board.is_king_in_check(board.player_turn):
                                board.grid_color[self.row + x][self.column + y] = 3
                            board.grid[self.row + x][self.column + y] = last_piece


class Bishop(Piece):
    def __init__(self, color: bool, row: int, column: int):
        super().__init__(color, row, column)
        self.num = 3

    def can_move_to(self, board):
        super().can_move_to(board)
        grid_x, grid_y = self.row, self.column  # temp grid cood to cycle thru
        while grid_x < 7 and grid_y < 7:  # While loops for all 4 diagonals
            grid_x += 1
            grid_y += 1
            if board.grid[grid_x][grid_y] == 0:  # If nothing there, color blue and keep going
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 2
                board.grid[grid_x][grid_y] = 0
            elif board.grid[grid_x][grid_y].color != self.color:  # If enemy, color red and stop
                last_piece = board.grid[grid_x][grid_y]
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 3
                board.grid[grid_x][grid_y] = last_piece
                break
            elif board.grid[grid_x][grid_y].color == self.color:  # If friendly, stop
                break
        grid_x, grid_y = self.row, self.column
        while grid_x > 0 and grid_y > 0:
            grid_x -= 1
            grid_y -= 1
            if board.grid[grid_x][grid_y] == 0:  # If nothing there, color blue and keep going
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 2
                board.grid[grid_x][grid_y] = 0
            elif board.grid[grid_x][grid_y].color != self.color:  # If enemy, color red and stop
                last_piece = board.grid[grid_x][grid_y]
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 3
                board.grid[grid_x][grid_y] = last_piece
                break
            elif board.grid[grid_x][grid_y].color == self.color:  # If friendly, stop
                break
        grid_x, grid_y = self.row, self.column
        while grid_x < 7 and grid_y > 0:
            grid_x += 1
            grid_y -= 1
            if board.grid[grid_x][grid_y] == 0:  # If nothing there, color blue and keep going
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 2
                board.grid[grid_x][grid_y] = 0
            elif board.grid[grid_x][grid_y].color != self.color:  # If enemy, color red and stop
                last_piece = board.grid[grid_x][grid_y]
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 3
                board.grid[grid_x][grid_y] = last_piece
                break
            elif board.grid[grid_x][grid_y].color == self.color:  # If friendly, stop
                break
        grid_x, grid_y = self.row, self.column
        while grid_x > 0 and grid_y < 7:
            grid_x -= 1
            grid_y += 1
            if board.grid[grid_x][grid_y] == 0:  # If nothing there, color blue and keep going
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 2
                board.grid[grid_x][grid_y] = 0
            elif board.grid[grid_x][grid_y].color != self.color:  # If enemy, color red and stop
                last_piece = board.grid[grid_x][grid_y]
                board.grid[grid_x][grid_y] = self
                if not board.is_king_in_check(board.player_turn):
                    board.grid_color[grid_x][grid_y] = 3
                board.grid[grid_x][grid_y] = last_piece
                break
            elif board.grid[grid_x][grid_y].color == self.color:  # If friendly, stop
                break


class Queen(Bishop, Rook):
    def __init__(self, color: bool, row: int, column: int):
        Piece.__init__(self, color, row, column)
        self.num = 4

    def can_move_to(self, board):
        super().can_move_to(board)
        # Bishop.can_move_to(self, board)
        # Rook.can_move_to(self, board)


class King(Piece):
    def __init__(self, color: bool, row: int, column: int):
        super().__init__(color, row, column)
        self.num = 5
        self.castling = True

    def can_move_to(self, board):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not (x == 0 and y == 0) and 0 <= self.row + x < 8 and 0 <= self.column + y < 8:
                    if board.grid[self.row + x][self.column + y] == 0:  # If nothing there, color blue
                        board.grid[self.row + x][self.column + y] = self
                        if not board.is_king_in_check(board.player_turn):
                            board.grid_color[self.row + x][self.column + y] = 2
                        # else:
                        # grid_color[grid_x + x][grid_y + y] = 4
                        board.grid[self.row + x][self.column + y] = 0
                    elif board.grid[self.row + x][self.column + y].color != self.color:  # If enemy, color red
                        last_piece = board.grid[self.row + x][self.column + y]
                        board.grid[self.row + x][self.column + y] = self
                        if not board.is_king_in_check(board.player_turn):
                            board.grid_color[self.row + x][self.column + y] = 3
                        board.grid[self.row + x][self.column + y] = last_piece
                board.grid[self.row][self.column] = self
                if self.castling and not board.is_king_in_check(board.player_turn):
                    if board.grid[self.row][0] and board.grid[self.row][0].castling:  # Castling on the left side
                        if not board.grid[self.row][3]:
                            board.grid[self.row][3] = self
                            if not board.is_king_in_check(board.player_turn):
                                if board.grid[self.row][2] == 0:
                                    board.grid[self.row][2] = self
                                    if not board.is_king_in_check(board.player_turn) \
                                            and not board.grid[self.row][1]:
                                        board.grid_color[self.row][2] = 5
                                    board.grid[self.row][2] = 0
                            board.grid[self.row][3] = 0
                    if board.grid[self.row][7] and board.grid[self.row][7].castling:  # Castling on the right side
                        if not board.grid[self.row][5]:
                            board.grid[self.row][5] = self
                            if not board.is_king_in_check(board.player_turn):
                                board.grid[self.row][5] = 0
                                if not board.grid[self.row][6]:
                                    board.grid[self.row][6] = self
                                    if not board.is_king_in_check(board.player_turn):
                                        board.grid[self.row][6] = 0
                                        board.grid_color[self.row][6] = 6
                                    board.grid[self.row][6] = 0
                            board.grid[self.row][5] = 0
                board.grid[self.row][self.column] = 0


class Board:
    def __init__(self):
        self.player_turn = False
        self.grid = []
        self.grid_color = []
        self.mouse_piece = 0
        self.captured = []
        self.screen = 0
        self.moves = []
        self.turn_num = 0
        for row in range(8):
            self.grid.append([])
            self.grid_color.append([])
            for column in range(8):
                if row == 1:
                    self.grid[1].append(Pawn(True, 1, column))
                elif row == 6:
                    self.grid[6].append(Pawn(False, 6, column))
                else:
                    self.grid[row].append(0)
                self.grid_color[row].append(0)
        for num1, piece in enumerate(PIECE_TUPLE):
            if piece == 'R':
                self.grid[0][num1] = Rook(True, 0, num1)
                self.grid[7][num1] = Rook(False, 7, num1)
            elif piece == 'N':
                self.grid[0][num1] = Knight(True, 0, num1)
                self.grid[7][num1] = Knight(False, 7, num1)
            elif piece == 'B':
                self.grid[0][num1] = Bishop(True, 0, num1)
                self.grid[7][num1] = Bishop(False, 7, num1)
            elif piece == 'Q':
                self.grid[0][num1] = Queen(True, 0, num1)
                self.grid[7][num1] = Queen(False, 7, num1)
            elif piece == 'K':
                self.grid[0][num1] = King(True, 0, num1)
                self.grid[7][num1] = King(False, 7, num1)

    def promotion(self, piece: int):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if row == 0 and self.grid[0][column] and self.grid[0][column].num == 0:
                    if piece == 1:
                        self.grid[0][column] = Rook(False, row, column)
                    elif piece == 2:
                        self.grid[0][column] = Knight(False, row, column)
                    elif piece == 3:
                        self.grid[0][column] = Bishop(False, row, column)
                    else:
                        self.grid[0][column] = Queen(False, row, column)
                if row == 7 and self.grid[7][column] and self.grid[7][column].num == 0:
                    if piece == 1:
                        self.grid[7][column] = Rook(True, row, column)
                    elif piece == 2:
                        self.grid[7][column] = Knight(True, row, column)
                    elif piece == 3:
                        self.grid[7][column] = Bishop(True, row, column)
                    else:
                        self.grid[7][column] = Queen(True, row, column)

    def clear_grid_markers(self):
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                self.grid_color[row][column] = 0

    def undo(self):  # Allows to undo moves in the game
        if self.moves and not self.mouse_piece:
            if self.moves[-1].promotion:
                self.grid[self.moves[-1].x_to][self.moves[-1].y_to] = Pawn(not bool(len(self.moves) % 2),
                                                                           self.moves[-1].x_to, self.moves[-1].y_to)
            elif self.moves[-1].king_castle:
                if len(self.moves) % 2 == 0:
                    self.grid[0][7] = self.grid[0][5]
                    self.grid[0][4] = self.grid[0][6]
                    self.grid[0][5] = 0
                    self.grid[0][6] = 0
                    self.grid[0][7].castling = True
                    self.grid[0][4].castling = True
                    self.grid[0][7].set_column(7)
                    self.grid[0][4].set_column(4)
                elif len(self.moves) % 2 == 1:
                    self.grid[7][7] = self.grid[7][5]
                    self.grid[7][4] = self.grid[7][6]
                    self.grid[7][5] = 0
                    self.grid[7][6] = 0
                    self.grid[7][7].castling = True
                    self.grid[7][4].castling = True
                    self.grid[7][7].set_column(7)
                    self.grid[7][4].set_column(4)
            elif self.moves[-1].queen_castle:
                if len(self.moves) % 2 == 0:
                    self.grid[0][0] = self.grid[0][3]
                    self.grid[0][4] = self.grid[0][2]
                    self.grid[0][2] = 0
                    self.grid[0][3] = 0
                    self.grid[0][0].castling = True
                    self.grid[0][4].castling = True
                    self.grid[0][0].set_column(0)
                    self.grid[0][4].set_column(4)
                elif len(self.moves) % 2 == 1:
                    self.grid[7][0] = self.grid[7][3]
                    self.grid[7][4] = self.grid[7][2]
                    self.grid[7][2] = 0
                    self.grid[7][3] = 0
                    self.grid[7][0].castling = True
                    self.grid[7][4].castling = True
                    self.grid[7][0].set_column(0)
                    self.grid[7][4].set_column(4)
            elif self.moves[-1].en_passant_capture and len(self.moves) % 2 == 1:
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from] = self.grid[self.moves[-1].x_to][
                    self.moves[-1].y_to]
                self.grid[self.moves[-1].x_to][self.moves[-1].y_to] = 0
                self.grid[self.moves[-1].x_to + 1][self.moves[-1].y_to] = self.captured.pop()
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].row = self.moves[-1].x_from
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].column = self.moves[-1].y_from
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].en_passant = False
            elif self.moves[-1].en_passant_capture and len(self.moves) % 2 == 0:
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from] = self.grid[self.moves[-1].x_to][
                    self.moves[-1].y_to]
                self.grid[self.moves[-1].x_to][self.moves[-1].y_to] = 0
                self.grid[self.moves[-1].x_to - 1][self.moves[-1].y_to] = self.captured.pop()
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].row = self.moves[-1].x_from
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].column = self.moves[-1].y_from
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].en_passant = False
            if self.moves[-1].capture:
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from] = self.grid[self.moves[-1].x_to][
                    self.moves[-1].y_to]
                self.grid[self.moves[-1].x_to][self.moves[-1].y_to] = self.captured.pop()
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].row = self.moves[-1].x_from
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].column = self.moves[-1].y_from
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].en_passant = False
            else:
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from] = self.grid[self.moves[-1].x_to][
                    self.moves[-1].y_to]
                self.grid[self.moves[-1].x_to][self.moves[-1].y_to] = 0
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].row = self.moves[-1].x_from
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].column = self.moves[-1].y_from
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].en_passant = False
            if self.moves[-1].castling_flag:
                self.grid[self.moves[-1].x_from][self.moves[-1].y_from].castling = True
            del self.moves[-1]
            self.player_turn = not self.player_turn

    def is_king_in_check(self, color: bool) -> bool:
        for row in range(8):
            for column in range(8):
                if self.grid[row][column] and self.grid[row][column].num == 5 and self.grid[row][column].color == color:
                    if color:  # check for  white pawns
                        if row < 7:
                            if 0 < column < 7:
                                if (self.grid[row + 1][column - 1]
                                    and not self.grid[row + 1][column - 1].num
                                    and not self.grid[row + 1][column - 1].color) or \
                                        (self.grid[row + 1][column + 1]
                                         and not self.grid[row + 1][column + 1].num
                                         and not self.grid[row + 1][column + 1].color):
                                    return True
                            elif column == 0:
                                if (self.grid[row + 1][column + 1]
                                        and not self.grid[row + 1][column + 1].num
                                        and not self.grid[row + 1][column + 1].color):
                                    return True
                            elif column == 7:
                                if (self.grid[row + 1][column - 1]
                                        and not self.grid[row + 1][column - 1].num
                                        and not self.grid[row + 1][column - 1].color):
                                    return True
                    elif not color:  # check for  black pawns
                        if 0 < row:
                            if 0 < column < 7:
                                if (self.grid[row - 1][column - 1]
                                    and not self.grid[row - 1][column - 1].num
                                    and self.grid[row - 1][column - 1].color) or \
                                        (self.grid[row - 1][column + 1]
                                         and not self.grid[row - 1][column + 1].num
                                         and self.grid[row - 1][column + 1].color):
                                    return True
                            elif column == 0:
                                if (self.grid[row - 1][column + 1]
                                        and not self.grid[row - 1][column + 1].num
                                        and self.grid[row - 1][column + 1].color):
                                    return True
                            elif column == 7:
                                if (self.grid[row - 1][column - 1]
                                        and not self.grid[row - 1][column - 1].num
                                        and self.grid[row - 1][column - 1].color):
                                    return True

                    # check for rooks or queens

                    row1, column1 = row, column
                    while row1 < 7:
                        row1 += 1
                        if self.grid[row1][column1] != 0 and (
                                self.grid[row1][column1].num == 1 or self.grid[row1][column1].num == 4) and \
                                self.grid[row1][column1].color != color:  # If enemy, color red and stop
                            return True
                        elif self.grid[row1][column1] != 0 and (
                                (not (self.grid[row1][column1].num == 1 or self.grid[row1][column1].num == 4)) or
                                self.grid[row1][column1].color == color):
                            break  # if not a r or q or is a friendly, stop
                    row1, column1 = row, column
                    while row1 > 0:
                        row1 -= 1
                        if self.grid[row1][column1] != 0 and (
                                self.grid[row1][column1].num == 1 or self.grid[row1][column1].num == 4) and \
                                self.grid[row1][column1].color != color:  # If enemy, color red and stop
                            return True
                        elif self.grid[row1][column1] != 0 and (
                                (not (self.grid[row1][column1].num == 1 or self.grid[row1][column1].num == 4)) or
                                self.grid[row1][column1].color == color):
                            break  # if not a r or q or is a friendly, stop
                    row1, column1 = row, column
                    while column1 < 7:
                        column1 += 1
                        if self.grid[row1][column1] != 0 and (
                                self.grid[row1][column1].num == 1 or self.grid[row1][column1].num == 4) and \
                                self.grid[row1][column1].color != color:  # If enemy, color red and stop
                            return True
                        if self.grid[row1][column1] != 0 and (
                                (not (self.grid[row1][column1].num == 1 or self.grid[row1][column1].num == 4)) or
                                self.grid[row1][column1].color == color):
                            break  # if not a r or q or is a friendly, stop

                    row1, column1 = row, column
                    while column1 > 0:
                        column1 -= 1
                        if self.grid[row1][column1] != 0 and (
                                self.grid[row1][column1].num == 1 or self.grid[row1][column1].num == 4) and \
                                self.grid[row1][column1].color != color:  # If enemy, color red and stop
                            return True
                        elif self.grid[row1][column1] != 0 and (
                                (not (self.grid[row1][column1].num == 1 or self.grid[row1][column1].num == 4)) or
                                self.grid[row1][column1].color == color):
                            break  # if not a r or q or is a friendly, stop

                    # check for bishops or queens

                    row1, column1 = row, column  # temp grid cood to cycle thru
                    while row1 < 7 and column1 < 7:  # While loops for all 4 diagonals
                        row1 += 1
                        column1 += 1
                        if self.grid[row1][column1] != 0 and (
                                self.grid[row1][column1].num == 3 or self.grid[row1][column1].num == 4) and \
                                self.grid[row1][column1].color != color:  # If enemy, color red and stop
                            return True
                        elif self.grid[row1][column1] != 0 and (
                                (not (self.grid[row1][column1].num == 3 or self.grid[row1][column1].num == 4)) or
                                self.grid[row1][column1].color == color):  # if not a b or q or is a friendly, stop
                            break
                    row1, column1 = row, column
                    while row1 > 0 and column1 > 0:
                        row1 -= 1
                        column1 -= 1
                        if self.grid[row1][column1] != 0 and (
                                self.grid[row1][column1].num == 3 or self.grid[row1][column1].num == 4) and \
                                self.grid[row1][column1].color != color:  # If enemy, color red and stop
                            return True
                        elif self.grid[row1][column1] != 0 and (
                                (not (self.grid[row1][column1].num == 3 or self.grid[row1][column1].num == 4)) or
                                self.grid[row1][column1].color == color):  # if not a b or q or is a friendly, stop
                            break
                    row1, column1 = row, column
                    while row1 < 7 and column1 > 0:
                        row1 += 1
                        column1 -= 1
                        if self.grid[row1][column1] != 0 and (
                                self.grid[row1][column1].num == 3 or self.grid[row1][column1].num == 4) and \
                                self.grid[row1][column1].color != color:  # If enemy, color red and stop
                            return True
                        elif self.grid[row1][column1] != 0 and (
                                (not (self.grid[row1][column1].num == 3 or self.grid[row1][column1].num == 4)) or
                                self.grid[row1][column1].color == color):  # if not a b or q or is a friendly, stop
                            break
                    row1, column1 = row, column
                    while row1 > 0 and column1 < 7:
                        row1 -= 1
                        column1 += 1
                        if self.grid[row1][column1] and (
                                self.grid[row1][column1].num == 3 or self.grid[row1][column1].num == 4) and \
                                self.grid[row1][column1].color != color:  # If enemy, color red and stop
                            return True
                        elif self.grid[row1][column1] and ((not (self.grid[row1][column1].num == 3 or
                                                                      self.grid[row1][column1].num == 4)) or
                                                                self.grid[row1][
                                                                    column1].color == color):  # if not a b or q or is a friendly, stop
                            break

                    # check for knights

                    for x in range(-2, 3):
                        for y in range(-2, 3):
                            if x != 0 and y != 0 and abs(x) != abs(y):
                                if 0 <= row + x < 8 and 0 <= column + y < 8:
                                    if self.grid[row + x][column + y] != 0 and self.grid[row + x][
                                        column + y].num == 2 and \
                                            self.grid[row + x][
                                                column + y].color != color:  # If enemy, color red and stop
                                        return True

                    # check for kings

                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if not (x == 0 and y == 0) and 0 <= row + x < 8 and 0 <= column + y < 8:
                                if self.grid[row + x][column + y] != 0 and self.grid[row + x][column + y].num == 5 and \
                                        self.grid[row + x][column + y].color != color:  # If enemy king return true
                                    return True

        return False

    def check_for_mate(self) -> bool:
        if not self.mouse_piece:
            for row in range(len(self.grid)):
                for column in range(len(self.grid[row])):
                    if self.grid[row][column] and self.grid[row][column].color == self.player_turn:
                        self.mouse_piece = self.grid[row][column]
                        self.grid[row][column] = 0
                        self.mouse_piece.can_move_to(self)
                        for row1 in range(len(self.grid_color)):
                            for column1 in range(len(self.grid_color[row1])):
                                if self.grid_color[row1][column1] == 2 or self.grid_color[row1][column1] == 3 \
                                        or self.grid_color[row1][column1] == 4:
                                    self.grid[row][column] = self.mouse_piece
                                    self.mouse_piece = 0
                                    self.clear_grid_markers()
                                    return False
                        self.grid[row][column] = self.mouse_piece
                        self.mouse_piece = 0
                        self.clear_grid_markers()
            if self.is_king_in_check(self.player_turn):
                if not self.player_turn:
                    print('The game is over, Black wins!')
                else:
                    print('The game is over, White wins!')
                self.moves[-1].mate = True
            else:
                print('Game ended in a draw!')
            return True


if __name__ == '__main__':
    class Game:
        def __init__(self):
            pygame.init()
            self.font = pygame.font.Font('freesansbold.ttf', 32)
            self.size = (1000, 576)  # 576, 576
            # Set the width and height of the screen [width, height]
            self.screen = pygame.display.set_mode(self.size)
            self.BPieces = pygame.image.load(
                'C:\\Users\\alexm\\PycharmProjects\\MyFirstCodes\\Chess\\Pieces\\MyBPieces.png').convert()
            self.BPieces.set_colorkey(RED)
            self.WPieces = pygame.image.load(
                'C:\\Users\\alexm\\PycharmProjects\\MyFirstCodes\\Chess\\Pieces\\MyWPieces.png').convert()
            self.WPieces.set_colorkey(RED)
            self.BPieceList = load_tile_table(self.BPieces)
            self.WPieceList = load_tile_table(self.WPieces)
            pygame.display.set_caption("Chess Attempt")
            # Loop until the user clicks the close button.
            self.done = False
            # Used to manage how fast the screen updates
            self.clock = pygame.time.Clock()
            self.board = Board()

        def text_on_screen(self, msg, x, y):
            text = self.font.render(msg, True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            self.screen.blit(text, text_rect)

        def run(self):
            while not self.done:
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()

        def events(self):
            # -------- Main Program Loop -----------
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.board.screen == 1 or self.board.screen == 2:
                        y, x = pygame.mouse.get_pos()
                        if event.button == 1 and 190 < x < 254 and 620 < y < 684:
                            self.board.promotion(4)
                            self.board.moves[-1].promotion = 4
                            self.board.screen = 0
                        elif event.button == 1 and 260 < x < 324 and 620 < y < 684:
                            self.board.promotion(3)
                            self.board.moves[-1].promotion = 3
                            self.board.screen = 0
                        elif event.button == 1 and 190 < x < 254 and 690 < y < 754:
                            self.board.promotion(2)
                            self.board.moves[-1].promotion = 2
                            self.board.screen = 0
                        elif event.button == 1 and 260 < x < 324 and 690 < y < 754:
                            self.board.promotion(1)
                            self.board.moves[-1].promotion = 1
                            self.board.screen = 0
                        if self.board.check_for_mate():
                            self.done = True
                    if self.board.screen == 0:
                        if event.button == 1 and 32 < pygame.mouse.get_pos()[0] < 544 and 32 < pygame.mouse.get_pos()[
                            1] < 544:
                            y, x = pygame.mouse.get_pos()
                            grid_x = (x - 32) // GRID_W
                            grid_y = (y - 32) // GRID_H
                            if self.board.grid[grid_x][grid_y] and self.board.mouse_piece == 0 and \
                                    self.board.grid[grid_x][grid_y].color == self.board.player_turn:
                                # If there's something in the square and not the mouse
                                # and the piece belongs to the player
                                pygame.mouse.set_visible(False)
                                self.board.mouse_piece = self.board.grid[grid_x][grid_y]  # Pick up the piece
                                self.board.grid[grid_x][grid_y] = 0  # clear the square
                                self.board.grid_color[grid_x][grid_y] = 1  # color it green
                                self.board.mouse_piece.can_move_to(self.board)
                                # self.board.moves.append(
                                #     chr(97 + grid_y) + str(grid_x + 1) + PIECE_DICT[self.board.mouse_piece.num])
                            elif self.board.grid_color[grid_x][
                                grid_y] and self.board.mouse_piece:
                                # If there's something in the mouse and the piece can go there
                                pygame.mouse.set_visible(True)
                                if self.board.mouse_piece.num == 0 and grid_x == 7 \
                                        and self.board.mouse_piece.color:  # Black promotion
                                    self.board.screen = 2
                                elif self.board.mouse_piece.num == 0 and grid_x == 0 \
                                        and not self.board.mouse_piece.color:  # White promotion
                                    self.board.screen = 1

                                if self.board.grid_color[grid_x][grid_y] == 3 and self.board.grid[grid_x][
                                    grid_y]:  # Add to the list of captured pieces
                                    self.board.captured.append(self.board.grid[grid_x][grid_y])

                                if self.board.grid_color[grid_x][grid_y] == 3 and not self.board.grid[grid_x] \
                                        [grid_y]:  # Remove en passant pawns if captured
                                    if self.board.grid[grid_x + 1][grid_y] and self.board.grid[grid_x + 1] \
                                            [grid_y].en_passant:
                                        self.board.captured.append(self.board.grid[grid_x + 1][grid_y])
                                        self.board.grid[grid_x + 1][grid_y] = 0
                                    if self.board.grid[grid_x - 1][grid_y] and self.board.grid[grid_x - 1] \
                                            [grid_y].en_passant:
                                        self.board.captured.append(self.board.grid[grid_x - 1][grid_y])
                                        self.board.grid[grid_x - 1][grid_y] = 0

                                if self.board.grid_color[grid_x][grid_y] == 5:  # Places the rook after castling
                                    self.board.grid[grid_x][3] = self.board.grid[grid_x][0]
                                    self.board.grid[grid_x][0] = 0
                                    self.board.grid[grid_x][3].column = 3
                                    self.board.grid[grid_x][3].castling = False
                                    self.board.moves.append(ChessMove(5, queen_castle=True))
                                elif self.board.grid_color[grid_x][grid_y] == 6:
                                    self.board.grid[grid_x][5] = self.board.grid[grid_x][7]
                                    self.board.grid[grid_x][7] = 0
                                    self.board.grid[grid_x][5].column = 5
                                    self.board.grid[grid_x][5].castling = False
                                    self.board.moves.append(ChessMove(5, king_castle=True))

                                if self.board.grid_color[grid_x][grid_y] != 4:  # Placement of the piece
                                    if self.board.grid_color[grid_x][grid_y] == 2:
                                        # If square can be advanced to, add to the moves list
                                        self.board.moves.append(ChessMove(self.board.mouse_piece.num,
                                                                          (self.board.mouse_piece.row,
                                                                           self.board.mouse_piece.column)
                                                                          , (grid_x, grid_y)))
                                    elif self.board.grid_color[grid_x][grid_y] == 3 \
                                            and self.board.grid[grid_x][grid_y]:  # if a piece is captured
                                        self.board.moves.append(ChessMove(self.board.mouse_piece.num, (
                                            self.board.mouse_piece.row, self.board.mouse_piece.column),
                                                                          (grid_x, grid_y),
                                                                          True))
                                    elif not self.board.grid[grid_x][grid_y] and self.board.grid_color[grid_x][
                                        grid_y] == 3:  # if an en passant pawn is captured
                                        self.board.moves.append(ChessMove(self.board.mouse_piece.num, (
                                            self.board.mouse_piece.row, self.board.mouse_piece.column),
                                                                          (grid_x, grid_y),
                                                                          True, True))
                                    if self.board.mouse_piece.castling \
                                            and (self.board.mouse_piece.num == 1 or self.board.mouse_piece.num == 5) \
                                            and self.board.grid_color[grid_x][grid_y] != 1:
                                        # remembers where the piece lost the castle flag
                                        self.board.moves[-1].castling_flag = True
                                    self.board.mouse_piece.row, self.board.mouse_piece.column = grid_x, grid_y
                                    self.board.grid[grid_x][grid_y] = self.board.mouse_piece
                                    if self.board.grid[grid_x][grid_y] and self.board.grid[grid_x][grid_y].castling and \
                                            self.board.grid_color[grid_x][grid_y] != 1:  # Remove the castling flag
                                        self.board.grid[grid_x][grid_y].castling = False
                                elif self.board.grid_color[grid_x][grid_y] == 4:  # for en passant
                                    self.board.mouse_piece.en_passant = True
                                    self.board.moves.append(ChessMove(self.board.mouse_piece.num, (
                                        self.board.mouse_piece.row, self.board.mouse_piece.column), (grid_x, grid_y),
                                                                      en_passant_flag=True))
                                    self.board.mouse_piece.row, self.board.mouse_piece.column = grid_x, grid_y
                                    self.board.grid[grid_x][grid_y] = self.board.mouse_piece
                                if self.board.grid_color[grid_x][grid_y] != 1:
                                    self.board.player_turn = not self.board.player_turn  # If the turn player placed on not a green square, change turn player
                                    if self.board.is_king_in_check(self.board.player_turn):
                                        self.board.moves[-1].check = True
                                for row2 in range(len(self.board.grid)):  # Remove en passant tag if not captured
                                    for column2 in range(len(self.board.grid[row2])):
                                        if self.board.grid[row2][column2] and self.board.grid[row2][column2].en_passant \
                                                and self.board.grid[row2][column2].color == self.board.player_turn:
                                            self.board.grid[row2][column2].en_passant = False
                                self.board.mouse_piece = 0
                                self.board.clear_grid_markers()
                                if self.board.check_for_mate():
                                    self.done = True
                        if event.button == 3:
                            # pass
                            self.board.undo()
                        if event.button == 2:
                            y, x = pygame.mouse.get_pos()
                            grid_x = (x - 32) // GRID_W
                            grid_y = (y - 32) // GRID_H
                            if grid_x < 0:  # prevents the game from crashing if clicking outside the 8x8 grid
                                grid_x = 0
                            if grid_x > 7:
                                grid_x = 7
                            if grid_y < 0:
                                grid_y = 0
                            if grid_y > 7:
                                grid_y = 7
                            # print(mouse_piece)
                            print('Row:', grid_x, 'Column:', grid_y)
                            if self.board.grid[grid_x][grid_y]:
                                print(vars(self.board.grid[grid_x][grid_y]))
                            else:
                                print('0')
                            # print(grid_color[grid_x][grid_y])

        # --- Game logic should go here
        def update(self):
            pass

        # --- Screen-clearing code goes here
        def draw(self):
            # Here, we clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            self.screen.fill(CHESS_WHITE)
            # --- Drawing code should go here
            # drawing the board
            for row in range(8):
                self.text_on_screen(str(8 - row), 16, 64 + 64 * row)
                self.text_on_screen(str(8 - row), 560, 64 + 64 * row)
                for column in range(8):
                    self.text_on_screen(chr(97 + column), 64 + 64 * column, 16)
                    self.text_on_screen(chr(97 + column), 64 + 64 * column, 560)
                    if (row % 2 == 0 and column % 2 == 1) or (row % 2 == 1 and column % 2 == 0):
                        pygame.draw.rect(self.screen, CHESS_BLACK, [row * 64 + 32, column * 64 + 32, 64, 64])

            for column in range(8):
                for row in range(8):
                    if self.board.grid_color[column][row] == 1:  # If piece is from last square, draw it green
                        green_sq = pygame.Surface([64, 64])
                        green_sq.fill(GREEN)
                        self.screen.blit(green_sq, [row * 64 + 32, column * 64 + 32])
                    elif self.board.grid_color[column][row] == 2 or self.board.grid_color[column][
                        row] >= 4:  # If square can be advanced to
                        blue_sq = pygame.Surface([64, 64])
                        blue_sq.fill(BLUE)
                        self.screen.blit(blue_sq, [row * 64 + 32, column * 64 + 32])
                    elif self.board.grid_color[column][row] == 3:  # If square can be captured to
                        red_sq = pygame.Surface([64, 64])
                        red_sq.fill(RED)
                        self.screen.blit(red_sq, [row * 64 + 32, column * 64 + 32])
                    if self.board.grid[column][row]:
                        if self.board.grid[column][row].color:
                            self.screen.blit(self.BPieceList[self.board.grid[column][row].num][0],
                                             [row * 64 + 32, column * 64 + 32])
                        elif not self.board.grid[column][row].color:
                            self.screen.blit(self.WPieceList[self.board.grid[column][row].num][0],
                                             [row * 64 + 32, column * 64 + 32])

            if self.board.screen == 1 or self.board.screen == 2:
                white_sq = pygame.Surface([192, 192])
                white_sq.fill(DARK_GRAY)
                self.screen.blit(white_sq, [600, 160])
                if self.board.screen == 1:
                    self.screen.blit(self.WPieceList[4][0], [620, 190])
                    self.screen.blit(self.WPieceList[3][0], [620, 260])
                    self.screen.blit(self.WPieceList[2][0], [690, 190])
                    self.screen.blit(self.WPieceList[1][0], [690, 260])
                else:
                    self.screen.blit(self.BPieceList[4][0], [620, 190])
                    self.screen.blit(self.BPieceList[3][0], [620, 260])
                    self.screen.blit(self.BPieceList[2][0], [690, 190])
                    self.screen.blit(self.BPieceList[1][0], [690, 260])

            if isinstance(self.board.mouse_piece, Piece):  # draws the held piece at the mouse position
                pos = pygame.mouse.get_pos()
                if self.board.mouse_piece.color:
                    self.screen.blit(self.BPieceList[self.board.mouse_piece.num][0],
                                     [pos[0] - 32, pos[1] - 32])
                elif not self.board.mouse_piece.color:
                    self.screen.blit(self.WPieceList[self.board.mouse_piece.num][0],
                                     [pos[0] - 32, pos[1] - 32])

            text = self.font.render(str(int(self.clock.get_fps())), True, BLACK)
            textRect = text.get_rect()
            textRect.midleft = (900, 32)
            self.screen.blit(text, textRect)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self.clock.tick(FPS)


    g = Game()
    while not g.done:
        g.run()
    # Close the window and quit.
    pygame.quit()
    for x in g.board.grid:
        print('[', end='')
        for num, y in enumerate(x):
            if isinstance(y, Piece):  # type(y) == Piece:
                if y.color:
                    local_color = "B"
                else:
                    local_color = "W"
                print(local_color + PIECE_DICT[y.num], end='')
            else:
                print(f'{y:2}', end='')
            if num + 1 != len(x):
                print(',', end='')
        print(']')
    moves = []
    for move in g.board.moves:
        print(vars(move))
        if move.king_castle:
            moves.append("0-0")
        elif move.queen_castle:
            moves.append("0-0-0")
        elif move.capture:
            if move.piece:
                moves.append(PIECE_DICT[move.piece] + 'x' + chr(move.x_to + 97) + str(abs(move.y_to - 8)))
            else:
                moves.append(str(abs(move.x_from - 8)) + 'x' + chr(move.x_to + 97) + str(abs(move.y_to - 8)))
        else:
            if move.piece:
                moves.append(PIECE_DICT[move.piece] + chr(move.x_to + 97) + str(abs(move.y_to - 8)))
            else:
                moves.append(chr(move.x_to + 97) + str(abs(move.y_to - 8)))
        if move.promotion:
            moves[-1] += f'={PIECE_DICT[move.promotion]}'
        if move.mate:
            moves[-1] += '#'
        elif move.check:
            moves[-1] += '+'
    print(g.board.captured)
    print(moves)
    with open("chessmoves.txt", 'w') as f:
        for num, move in enumerate(moves):
            if not num % 2:
                f.write(str((num + 2) // 2) + '. ' + move + ' ')
            else:
                f.write(move + '\n')
        f.close()
    # print(grid[7][0])
    # print(is_king_in_check('B'))
    # print(white_captured)
    # print(black_captured)
