import pygame
from const import *
class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos
    
    def save_initial(self, pos, offset_x=0):
        x, y = pos
        self.initial_row = y // SQSIZE - 4
        self.initial_col = (x - offset_x) // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    def update_blit(self, surface, offset_x=0):
        self.piece.set_texture(size=128)
        img = pygame.image.load(self.piece.texture)
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)
