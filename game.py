import pygame

from const import *
from board import Board
from dragger import Dragger
from square import Square
from collections import Counter

class Game:


    def __init__(self, flip = False):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board(flip = flip)
        self.dragger = Dragger()
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.captured_white = []  # white pieces captured by black
        self.captured_black = []  # black pieces captured by white

    def show_captured(self, surface, offset_x=0, position='top', player_color='white'):

        y = (2.9 * SQSIZE) if position == 'top' else (12 * SQSIZE) + 10

        # Which list to use
        captured = self.captured_black if player_color == 'black' else self.captured_white
        count_by_type = Counter(type(p).__name__ for p in captured)

        grouped = {}
        for piece in captured:
            name = type(piece).__name__
            if name not in grouped:
                grouped[name] = (piece, count_by_type[name])  # one of each type

        # Draw each group
        x = offset_x + 10
        for piece_type, (piece, count) in grouped.items():
            piece.set_texture(size=80)
            img = pygame.image.load(piece.texture)
            img_rect = img.get_rect(topleft=(x, y + 1))
            surface.blit(img, img_rect)

            if count > 1:
                label = self.font.render(f"x{count}", True, (63, 125, 88))
                surface.blit(label, (x + 1, y + 5))

            x += 100  # spacing between groups

    def show_bg(self, surface, offset_x=0):
        is_second_board = offset_x > 0  # Any non-zero offset means it's the second board

        area_height = SQSIZE
        area_width = SQSIZE * 8
        y = (2.9 * SQSIZE)
        rect = pygame.Rect(offset_x, y, area_width, area_height)
        pygame.draw.rect(surface, (187, 216, 163), rect, border_radius=6)

        y = (12 * SQSIZE) + 10
        rect = pygame.Rect(offset_x, y, area_width, area_height)
        pygame.draw.rect(surface, (187, 216, 163), rect, border_radius=6)

        for row in range(ROWS):
            for col in range(COLS):
                # Square color
                color = (234, 235, 200) if (row + col) % 2 == 0 else (119, 154, 88)
                rect = (offset_x + col * SQSIZE, (row + 4) * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                # Rank labels (numbers on left side)
                if col == 0:
                    text_color = (119, 154, 88) if row % 2 == 0 else (234, 235, 200)
                    label_num = row + 1 if is_second_board else ROWS - row
                    label = self.font.render(str(label_num), True, text_color)
                    label_pos = (offset_x + 5, (row + 4) * SQSIZE + 5)
                    surface.blit(label, label_pos)

                # File labels (letters on bottom)
                if row == 7:
                    text_color = (119, 154, 88) if (row + col) % 2 == 0 else (234, 235, 200)
                    label = self.font.render(Square.get_alphacol(col), True, text_color)
                    label_pos = (offset_x + col * SQSIZE + 2, (row + 4) * SQSIZE + 60)
                    surface.blit(label, label_pos)

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

    def show_moves(self, surface, offset_x=0):
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                rect = (offset_x + move.final.col * SQSIZE, (move.final.row + 4) * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface, offset_x=0):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                rect = (offset_x + pos.col * SQSIZE, (pos.row + 4) * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface, offset_x=0):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (offset_x + self.hovered_sqr.col * SQSIZE, (self.hovered_sqr.row + 4) * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]