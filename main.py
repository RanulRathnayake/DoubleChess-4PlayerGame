import sys
import pygame

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Double Chess Boards")
        self.game1 = Game(flip = False)
        self.game2 = Game(flip = True)

        for row in self.game2.board.squares:
            for square in row:
                if square.has_piece():
                    piece = square.piece
                    piece.color = 'white' if piece.color == 'black' else 'black'


    def mainloop(self):
        screen = self.screen
        game1 = self.game1
        game2 = self.game2
        board1 = game1.board
        board2 = game2.board
        dragger1 = game1.dragger
        dragger2 = game2.dragger

        while True:
            screen.fill((0, 0, 0))

            # Board 1
            game1.show_bg(screen, offset_x=0)
            game1.show_last_move(screen, offset_x=0)
            game1.show_moves(screen, offset_x=0)
            game1.show_pieces(screen, offset_x=0)
            game1.show_hover(screen, offset_x=0)

            if dragger1.dragging:
                dragger1.update_blit(screen, offset_x=0)

            # Board 2
            game2.show_bg(screen, offset_x=8 * SQSIZE)
            game2.show_last_move(screen, offset_x=8 * SQSIZE)
            game2.show_moves(screen, offset_x=8 * SQSIZE)
            game2.show_pieces(screen, offset_x=8 * SQSIZE)
            game2.show_hover(screen, offset_x=8 * SQSIZE)

            if dragger2.dragging:
                dragger2.update_blit(screen, offset_x=8 * SQSIZE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = x // SQSIZE
                    row = y // SQSIZE - 4

                    if 0 <= row < 8:
                        if 0 <= col < 8:
                            # board 1
                            dragger = dragger1
                            board = board1
                            game = game1
                            offset_x = 0
                            actual_col = col
                        elif 8 <= col < 16:
                            # board 2
                            dragger = dragger2
                            board = board2
                            game = game2
                            offset_x = 8 * SQSIZE
                            actual_col = col - 8
                        else:
                            continue
                        if board.squares[row][actual_col].has_piece():
                            piece = board.squares[row][actual_col].piece
                            if piece.color == game.next_player:
                                board.calc_moves(piece, row, actual_col, bool=True)
                                dragger.save_initial(event.pos, offset_x)
                                dragger.drag_piece(piece)

                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    col = x // SQSIZE
                    row = y // SQSIZE - 4

                    if 0 <= row < 8:
                        if 0 <= col < 8:
                            game1.set_hover(row, col)
                            if dragger1.dragging:
                                dragger1.update_mouse(event.pos)
                        elif 8 <= col < 16:
                            game2.set_hover(row, col - 8)
                            if dragger2.dragging:
                                dragger2.update_mouse(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    col = x // SQSIZE
                    row = y // SQSIZE - 4

                    if 0 <= row < 8:
                        if 0 <= col < 8:
                            dragger = dragger1
                            board = board1
                            game = game1
                            actual_col = col
                        elif 8 <= col < 16:
                            dragger = dragger2
                            board = board2
                            game = game2
                            actual_col = col - 8
                        else:
                            continue

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            released_row = dragger.mouseY // SQSIZE - 4
                            released_col = (dragger.mouseX // SQSIZE) - (8 if col >= 8 else 0)

                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            if board.valid_move(dragger.piece, move):
                                board.move(dragger.piece, move)
                                game.next_turn()

                            dragger.undrag_piece()

            pygame.display.update()

main = Main()
main.mainloop()







""" import sys
import pygame

from const import *
from game import Game
from square import Square
from move import Move
class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    # print(event.pos)

                    clicked_row = dragger.mouseY//SQSIZE
                    clicked_col = dragger.mouseX//SQSIZE

                    # print(dragger.mouseX, clicked_col)
                    # print(dragger.mouseY, clicked_row)

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()


                    dragger.undrag_piece()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop() """