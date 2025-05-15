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

            line_x = 8 * SQSIZE
            pygame.draw.line(screen, (0, 0, 0), (line_x, 4 * SQSIZE), (line_x, (4 + ROWS) * SQSIZE), 4)

            # show captured
            game1.show_captured(screen, offset_x=0, position='top', player_color='black')
            game1.show_captured(screen, offset_x=0, position='bottom', player_color='white')
            game2.show_captured(screen, offset_x=8 * SQSIZE, position='top', player_color='white')
            game2.show_captured(screen, offset_x=8 * SQSIZE, position='bottom', player_color='black')

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
                                captured_piece = board.squares[final.row][final.col].piece
                                if captured_piece:
                                    piece_cls = type(captured_piece)
                                    new_piece = piece_cls(captured_piece.color)
                                    if game is game1:
                                        if captured_piece.color == 'white':
                                            game2.captured_white.append(captured_piece)
                                            game2.board.add_captured_piece_to_board(new_piece, 2)
                                        else:
                                            game2.captured_black.append(captured_piece)
                                            game2.board.add_captured_piece_to_board(new_piece, 2)
                                    else:
                                        if captured_piece.color == 'white':
                                            game1.captured_white.append(captured_piece)
                                            game1.board.add_captured_piece_to_board(new_piece, 1)
                                        else:
                                            game1.captured_black.append(captured_piece)
                                            game1.board.add_captured_piece_to_board(new_piece, 1)

                                board.move(dragger.piece, move)
                                game.next_turn()

                            dragger.undrag_piece()

            pygame.display.update()

main = Main()
main.mainloop()
