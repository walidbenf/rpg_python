"""
RPG Tour par Tour - Jeu Pygame
Point d'entrée principal du jeu
"""
import pygame
import sys
from src.game import Game
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    """Fonction principale du jeu"""
    # Initialisation de Pygame
    pygame.init()

    # Configuration de l'écran
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Tour par Tour")
    clock = pygame.time.Clock()

    # Chargement des polices
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)

    # Création du jeu
    game = Game(screen, font_large, font_medium, font_small)

    # Boucle principale
    running = True
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(FPS)

    # Nettoyage
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
