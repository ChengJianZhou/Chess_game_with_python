# main.py

import pygame
from Board import Board

def main():
    pygame.init()

    # Configurar la pantalla y otros elementos de Pygame
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Ajedrez")

    board = Board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.handle_click(pos)

        screen.fill((255, 255, 255))  # Llenar la pantalla con blanco
        board.draw(screen)  # Dibujar el tablero y las piezas

        pygame.display.flip()  # Actualizar la pantalla

    pygame.quit()

if __name__ == "__main__":
    main()
