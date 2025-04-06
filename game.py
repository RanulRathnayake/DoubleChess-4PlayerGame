import pygame

from const import *
from board import Board
from dragger import Dragger
from square import Square

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.font = pygame.font.SysFont('monospace', 18, bold=True)


    def show_bg(self, surface, offset_x=0):
        for row in range(ROWS):
            for col in range(COLS):
                color = (234, 235, 200) if (row + col) % 2 == 0 else (119, 154, 88)
                rect = (offset_x + col * SQSIZE, (row + 4) * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)


    """ def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row+col)%2 == 0:
                    color = (234,235,200)
                else:
                    color = (119,154,88)
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface,color,rect)

                if col == 0:

                    color = (119,154,88) if row % 2 == 0 else (234,235,200)
                    lbl = self.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    surface.blit(lbl, lbl_pos)
                if row == 7:

                    color = (119,154,88) if (row + col) % 2 == 0 else (234,235,200)
                    lbl = self.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, SCREEN_HEIGHT - 20)
                    surface.blit(lbl, lbl_pos) """


    def show_pieces(self, surface, offset_x=0):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = (offset_x + col * SQSIZE + SQSIZE // 2, (row + 4) * SQSIZE + SQSIZE // 2)
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    """ def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col*SQSIZE+SQSIZE//2, row*SQSIZE+SQSIZE//2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
 """
    def show_moves(self, surface, offset_x=0):
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                rect = (offset_x + move.final.col * SQSIZE, (move.final.row + 4) * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    """ def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:

                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect) """



    def show_last_move(self, surface, offset_x=0):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                rect = (offset_x + pos.col * SQSIZE, (pos.row + 4) * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    """def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial,final]:
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)"""

    def show_hover(self, surface, offset_x=0):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (offset_x + self.hovered_sqr.col * SQSIZE, (self.hovered_sqr.row + 4) * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    """def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)"""

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]