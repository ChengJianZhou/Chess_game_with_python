from Piece import Piece

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.first_move = True  # Para controlar el primer movimiento
        self.can_be_captured_en_passant = False  # Para rastrear si puede ser capturado al paso

    def valid_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1
        row, col = self.position

        # Movimiento hacia adelante
        if self.is_on_board(row + direction, col) and board[row + direction][col] is None:
            moves.append((row + direction, col))
            # Movimiento doble hacia adelante en el primer movimiento
            if self.first_move and self.is_on_board(row + 2 * direction, col) and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))

        # Capturas
        if self.is_on_board(row + direction, col - 1) and board[row + direction][col - 1] is not None and board[row + direction][col - 1].color != self.color:
            moves.append((row + direction, col - 1))
        if self.is_on_board(row + direction, col + 1) and board[row + direction][col + 1] is not None and board[row + direction][col + 1].color != self.color:
            moves.append((row + direction, col + 1))

        # Captura al paso
        if self.is_on_board(row, col - 1) and isinstance(board[row][col - 1], Pawn) and board[row][col - 1].color != self.color and board[row][col - 1].can_be_captured_en_passant:
            moves.append((row + direction, col - 1))
        if self.is_on_board(row, col + 1) and isinstance(board[row][col + 1], Pawn) and board[row][col + 1].color != self.color and board[row][col + 1].can_be_captured_en_passant:
            moves.append((row + direction, col + 1))

        return moves

    def move(self, position):
        if abs(position[0] - self.position[0]) == 2:  # Si el peón se mueve dos filas hacia adelante
            self.can_be_captured_en_passant = True
        else:
            self.can_be_captured_en_passant = False
        self.position = position
        self.first_move = False  # Una vez que el peón se mueve, ya no es el primer movimiento

    def is_on_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
