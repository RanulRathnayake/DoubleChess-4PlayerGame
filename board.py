from const import *
from square import Square
from piece import *
from move import Move
import copy


class Board:
    def __init__(self):
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook


                if rook and rook.moves:
                    self.move(rook, rook.moves[-1])

        piece.moved = True
        piece.clear_moves()

        self.last_move = move

    """def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True
        piece.clear_moves()
        self.last_move = move
        """

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_board = copy.deepcopy(self)

        temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece

        if not temp_piece:
            return True

        temp_board.move(temp_piece, move)

        king_pos = None
        for row in range(ROWS):
            for col in range(COLS):
                square = temp_board.squares[row][col]
                if isinstance(square.piece, King) and square.piece.color == piece.color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:
            return True

        for row in range(ROWS):
            for col in range(COLS):
                square = temp_board.squares[row][col]
                if square.has_enemy_piece(piece.color):
                    attacker = square.piece
                    temp_board.calc_moves(attacker, row, col, bool=False)
                    for m in attacker.moves:
                        if (m.final.row, m.final.col) == king_pos:
                            return True

        return False


    """ def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False """

    def calc_moves(self, piece, row, col, bool=True):

        def pawn_moves():
            # move forward
            steps = 1 if piece.moved else 2
            start = row + piece.dir
            end = row + (piece.dir * (1+steps))
            for possible_moves in range(start, end, piece.dir):
                if Square.in_range(possible_moves):
                    if self.squares[possible_moves][col].is_empty():
                        initial = Square(row,col)
                        final = Square(possible_moves,col)
                        move = Move(initial,final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else: break
                else: break

            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):

                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    else: break
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            directions = [
                (-1, 0), (-1, 1), (0, 1), (1, 1),
                (1, 0), (1, -1), (0, -1), (-1, -1)
            ]

            for dx, dy in directions:
                r, c = row + dx, col + dy

                if Square.in_range(r, c):
                    target_square = self.squares[r][c]
                    if target_square.is_empty_or_enemy(piece.color):
                        initial = self.squares[row][col]
                        final = self.squares[r][c]
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            if not piece.moved:
                current_square = self.squares[row][col]
                current_check = self.in_check(piece, Move(current_square, current_square))
                if not current_check:

                    left_rook = self.squares[row][0].piece
                    if isinstance(left_rook, Rook) and not left_rook.moved:
                        if all(self.squares[row][c].is_empty() for c in range(1, 4)):
                            move_through = Move(current_square, self.squares[row][3])
                            move_final = Move(current_square, self.squares[row][2])
                            if not self.in_check(piece, move_through) and not self.in_check(piece, move_final):
                                piece.left_rook = left_rook
                                moveK = Move(current_square, self.squares[row][2])
                                moveR = Move(self.squares[row][0], self.squares[row][3])
                                piece.add_move(moveK)
                                left_rook.add_move(moveR)

                    right_rook = self.squares[row][7].piece
                    if isinstance(right_rook, Rook) and not right_rook.moved:
                        if all(self.squares[row][c].is_empty() for c in range(5, 7)):
                            move_through = Move(current_square, self.squares[row][5])
                            move_final = Move(current_square, self.squares[row][6])
                            if not self.in_check(piece, move_through) and not self.in_check(piece, move_final):
                                piece.right_rook = right_rook
                                moveK = Move(current_square, self.squares[row][6])
                                moveR = Move(self.squares[row][7], self.squares[row][5])
                                piece.add_move(moveK)
                                right_rook.add_move(moveR)

        """def king_moves():
            adjs = [
                (row - 1, col + 0),
                (row - 1, col + 1),
                (row + 0, col + 1),
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1),
            ]

            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                piece.left_rook = left_rook
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                left_rook.add_move(moveR)
                                piece.add_move(moveK)
                                if not bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK) 

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                piece.right_rook = right_rook

                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                right_rook.add_move(moveR)
                                piece.add_move(moveK)
                                if not bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)"""


        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knight
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))