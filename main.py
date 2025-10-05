"""
RPG Tour par Tour - Jeu Pygame
Point d'entrée principal du jeu
"""
import pygame
import sys
from src.menu import Menu
from src.game import Game
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    """Fonction principale du jeu"""
    # Initialisation de Pygame
    pygame.init()

    # Configuration de l'écran
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Roguelike")
    clock = pygame.time.Clock()

    # Chargement des polices
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)

    # Création du menu
    menu = Menu(screen, font_large, font_medium, font_small)
    game = None

    # État de l'application
    current_state = "menu"  # menu, game
    running = True

    # Boucle principale
    while running:
        # Gestion des événements selon l'état
        if current_state == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                action = menu.handle_events(event)
                if action == "play":
                    # Créer une nouvelle partie
                    game = Game(screen, font_large, font_medium, font_small)
                    current_state = "game"
                elif action == "quit":
                    running = False

        elif current_state == "game":
            # Le jeu gère ses propres événements
            if not game.handle_events():
                running = False

        # Mise à jour et affichage
        if current_state == "menu":
            menu.draw()
        elif current_state == "game":
            game.update()
            game.draw()

            # Vérifier si on doit retourner au menu
            if game.return_to_menu:
                current_state = "menu"
                game = None

        pygame.display.flip()
        clock.tick(FPS)

    # Nettoyage
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
