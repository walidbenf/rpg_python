"""
Module pour le menu principal du jeu
"""
import pygame
from .ui import Button
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK,
    BLUE, GOLD, RED, PURPLE
)


class Menu:
    """Classe pour le menu principal"""

    def __init__(self, screen, font_large, font_medium, font_small):
        """
        Initialise le menu

        Args:
            screen: Surface pygame principale
            font_large: Grande police
            font_medium: Police moyenne
            font_small: Petite police
        """
        self.screen = screen
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small

        # État du menu
        self.state = "main"  # main, options, credits
        self.selected_action = None

        # Créer les boutons
        self._create_buttons()

    def _create_buttons(self):
        """Crée les boutons du menu"""
        button_width = 300
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 50

        # Boutons du menu principal
        self.main_buttons = [
            Button(
                button_x, start_y,
                button_width, button_height,
                "Jouer", BLUE, PURPLE, self.font_medium
            ),
            Button(
                button_x, start_y + 80,
                button_width, button_height,
                "Options", BLUE, PURPLE, self.font_medium
            ),
            Button(
                button_x, start_y + 160,
                button_width, button_height,
                "Quitter", RED, GOLD, self.font_medium
            )
        ]

        # Bouton retour pour les sous-menus
        self.back_button = Button(
            50, SCREEN_HEIGHT - 100,
            150, 50,
            "Retour", BLUE, PURPLE, self.font_small
        )

    def handle_events(self, event):
        """
        Gère les événements du menu

        Args:
            event: Événement pygame

        Returns:
            str: Action sélectionnée ('play', 'quit', None)
        """
        if self.state == "main":
            # Gérer les clics sur les boutons principaux
            for i, button in enumerate(self.main_buttons):
                if button.handle_event(event):
                    if i == 0:  # Jouer
                        return "play"
                    elif i == 1:  # Options
                        self.state = "options"
                    elif i == 2:  # Quitter
                        return "quit"

        elif self.state == "options":
            # Gérer le bouton retour
            if self.back_button.handle_event(event):
                self.state = "main"

        return None

    def draw(self):
        """Dessine le menu"""
        # Fond
        self.screen.fill(BLACK)

        if self.state == "main":
            self._draw_main_menu()
        elif self.state == "options":
            self._draw_options()

    def _draw_main_menu(self):
        """Dessine le menu principal"""
        # Titre
        title_text = self.font_large.render("RPG ROGUELIKE", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Sous-titre
        subtitle_text = self.font_small.render("Aventure Tour par Tour", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Dessiner les boutons
        for button in self.main_buttons:
            button.draw(self.screen)

        # Instructions
        info_text = self.font_small.render(
            "Traversez les étages et battez tous les ennemis !",
            True, WHITE
        )
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(info_text, info_rect)

    def _draw_options(self):
        """Dessine le menu des options"""
        # Titre
        title_text = self.font_large.render("OPTIONS", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)

        # Info (pour l'instant juste un placeholder)
        info_lines = [
            "Volume: 100%",
            "Difficulté: Normal",
            "Résolution: 800x600",
            "",
            "(Options à venir...)"
        ]

        y = 250
        for line in info_lines:
            text = self.font_small.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 40

        # Bouton retour
        self.back_button.draw(self.screen)
