import pygame
from Piece import Piece
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King

class Board:
    def __init__(self):
        self.tile_size = 100
        self.rows = 8
        self.cols = 8
        self.grid = self.create_initial_board()
        self.selected_piece = None
        self.valid_moves = []
        self.current_turn = 'white'  # Inicia el turno con las blancas
        self.promotion_pending = False
        self.promotion_pos = None
        self.promotion_color = None
        self.en_passant_target = None  # Para rastrear el peón que puede ser capturado al paso
        self.game_over = False  # Para controlar el estado del juego

    def create_initial_board(self):
        board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        # Colocar las piezas iniciales
        for col in range(self.cols):
            board[1][col] = Pawn('black', (1, col))
            board[6][col] = Pawn('white', (6, col))
        # Colocar torres
        board[0][0] = Rook('black', (0, 0))
        board[0][7] = Rook('black', (0, 7))
        board[7][0] = Rook('white', (7, 0))
        board[7][7] = Rook('white', (7, 7))
        
        # Colocar caballos
        board[0][1] = Knight('black', (0, 1))
        board[0][6] = Knight('black', (0, 6))
        board[7][1] = Knight('white', (7, 1))
        board[7][6] = Knight('white', (7, 6))
        # Colocar alfiles
        board[0][2] = Bishop('black', (0, 2))
        board[0][5] = Bishop('black', (0, 5))
        board[7][2] = Bishop('white', (7, 2))
        board[7][5] = Bishop('white', (7, 5))
        # Colocar reinas
        board[0][3] = Queen('black', (0, 3))
        board[7][3] = Queen('white', (7, 3))
        # Colocar reyes
        board[0][4] = King('black', (0, 4))
        board[7][4] = King('white', (7, 4))
        return board

    def select_piece(self, row, col):
        if self.game_over:
            return
        piece = self.grid[row][col]
        if self.selected_piece:
            # Si ya hay una pieza seleccionada, la deseleccionamos
            self.selected_piece = None
            self.valid_moves = []

        if piece and piece.color == self.current_turn:
            # Seleccionar la pieza si existe y pertenece al jugador actual
            self.selected_piece = piece
            self.valid_moves = piece.valid_moves(self.grid)

    def move_piece(self, row, col):
        if self.game_over:
            return
        if (row, col) in self.valid_moves:
            old_row, old_col = self.selected_piece.position

            # Lógica de enroque
            if isinstance(self.selected_piece, King) and abs(col - old_col) == 2:
                # Movimiento de enroque
                rook_col = 0 if col < old_col else 7
                new_rook_col = 3 if col < old_col else 5
                rook = self.grid[old_row][rook_col]
                self.grid[old_row][rook_col] = None
                self.grid[old_row][new_rook_col] = rook
                rook.move((old_row, new_rook_col))

            # Lógica de captura al paso
            if isinstance(self.selected_piece, Pawn) and (col, row) == self.en_passant_target:
                self.grid[old_row][col] = None  # Captura el peón al paso

            captured_piece = self.grid[row][col]
            self.grid[old_row][old_col] = None
            self.grid[row][col] = self.selected_piece
            self.selected_piece.move((row, col))

            # Si el peón se movió dos casillas, actualizar en_passant_target
            if isinstance(self.selected_piece, Pawn) and abs(row - old_row) == 2:
                self.en_passant_target = (col, (old_row + row) // 2)
            else:
                self.en_passant_target = None

            # Verificar captura del rey
            if isinstance(captured_piece, King):
                self.game_over = True
                self.show_victory_message(captured_piece.color)

            self.selected_piece = None
            self.valid_moves = []

            if isinstance(self.grid[row][col], Pawn) and (row == 0 or row == 7):
                self.promotion_pending = True
                self.promotion_pos = (row, col)
                self.promotion_color = self.grid[row][col].color
            else:
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def cancel_selection(self):
        self.selected_piece = None
        self.valid_moves = []

    def handle_click(self, pos):
        if self.game_over:
            return
        col, row = pos[0] // self.tile_size, pos[1] // self.tile_size
        if self.promotion_pending:
            self.handle_promotion(row, col)
        elif self.selected_piece:
            if (row, col) in self.valid_moves:
                self.move_piece(row, col)
            elif (row, col) == self.selected_piece.position:
                self.cancel_selection()
            else:
                piece = self.grid[row][col]
                if piece and piece.color == self.current_turn:
                    self.select_piece(row, col)
                else:
                    self.cancel_selection()
        else:
            self.select_piece(row, col)

    def handle_promotion(self, row, col):
        if row == 0 and col in range(4):
            pieces = [Queen, Rook, Bishop, Knight]
            selected_piece = pieces[col](self.promotion_color, self.promotion_pos)  # Crear la pieza seleccionada
            self.grid[self.promotion_pos[0]][self.promotion_pos[1]] = selected_piece  # Colocar la nueva pieza en el tablero
            self.promotion_pending = False  # Finalizar el proceso de promoción
            self.promotion_pos = None
            self.promotion_color = None
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def show_victory_message(self, defeated_color):
        winner_color = 'white' if defeated_color == 'black' else 'black'
        self.game_over_message = f"{winner_color.capitalize()} wins!"

    def draw(self, screen):
        colors = [(255, 255, 255), (0, 0, 0)]
        for row in range(self.rows):
            for col in range(self.cols):
                color = colors[(row + col) % 2]
                rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)

                piece = self.grid[row][col]
                if piece is not None:
                    # Dibujar la pieza (aquí puedes agregar imágenes de las piezas)
                    piece_text = piece.__class__.__name__[0]
                    font = pygame.font.Font(None, 74)
                    text = font.render(piece_text, True, (200, 0, 0) if piece.color == 'white' else (0, 0, 200))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

                # Dibujar los movimientos válidos
                if (row, col) in self.valid_moves:
                    pygame.draw.circle(screen, (0, 255, 0), rect.center, 15)

        # Resaltar la pieza seleccionada
        if self.selected_piece:
            piece_rect = pygame.Rect(self.selected_piece.position[1] * self.tile_size,
                                     self.selected_piece.position[0] * self.tile_size,
                                     self.tile_size, self.tile_size)
            pygame.draw.rect(screen, (0, 255, 0), piece_rect, 3)
        
        if self.promotion_pending:
            self.draw_promotion_choices(screen)

        if self.game_over:
            self.draw_victory_message(screen)

    def draw_promotion_choices(self, screen):
        promotion_rect = pygame.Rect(0, 0, self.tile_size * 4, self.tile_size)
        pygame.draw.rect(screen, (200, 200, 200), promotion_rect)
        pieces = ['Q', 'R', 'B', 'N']
        for i, piece in enumerate(pieces):
            font = pygame.font.Font(None, 74)
            text = font.render(piece, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.tile_size * i + self.tile_size // 2, self.tile_size // 2))
            screen.blit(text, text_rect)

    def draw_victory_message(self, screen):
        font = pygame.font.Font(None, 74)
        if hasattr(self, 'game_over_message'):
            message = self.game_over_message
            text = font.render(message, True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.tile_size * self.cols // 2, self.tile_size * self.rows // 2))
            screen.blit(text, text_rect)
