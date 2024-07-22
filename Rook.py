from Piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False

    def valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for drow, dcol in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * drow, col + i * dcol
                if not self.is_on_board(new_row, new_col):
                    break
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def move(self, position):
        self.position = position
        self.has_moved = True

    def is_on_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
