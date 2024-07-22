from Piece import Piece
from Rook import Rook

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False

    def valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if self.is_on_board(new_row, new_col):
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))

        # Enroque
        if not self.has_moved and not self.in_check(board):
            # Enroque corto
            if self.can_castle_kingside(board):
                moves.append((row, col + 2))
            # Enroque largo
            if self.can_castle_queenside(board):
                moves.append((row, col - 2))

        return moves

    def can_castle_kingside(self, board):
        row, col = self.position
        rook = board[row][7]
        if isinstance(rook, Rook) and not rook.has_moved:
            if board[row][col + 1] is None and board[row][col + 2] is None:
                return True
        return False

    def can_castle_queenside(self, board):
        row, col = self.position
        rook = board[row][0]
        if isinstance(rook, Rook) and not rook.has_moved:
            if board[row][col - 1] is None and board[row][col - 2] is None and board[row][col - 3] is None:
                return True
        return False

    def move(self, position):
        self.position = position
        self.has_moved = True

    def in_check(self, board):
        # Lógica para determinar si el rey está en jaque
        pass

    def is_on_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
