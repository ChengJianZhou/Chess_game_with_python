# Bishop.py

from Piece import Piece

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def valid_moves(self, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Movimientos diagonales

        for direction in directions:
            for i in range(1, 8):  # El alfil puede moverse hasta 7 casillas en diagonal
                row = self.position[0] + direction[0] * i
                col = self.position[1] + direction[1] * i
                if 0 <= row < 8 and 0 <= col < 8:  # Verificar límites del tablero
                    if board[row][col] is None:
                        moves.append((row, col))
                    elif board[row][col].color != self.color:
                        moves.append((row, col))
                        break
                    else:
                        break
                else:
                    break

        return moves
