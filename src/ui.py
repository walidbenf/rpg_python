"""
Module pour les éléments d'interface utilisateur
"""
import pygame
from .constants import WHITE


class Button:
    """Classe pour les boutons interactifs"""

    def __init__(self, x, y, width, height, text, color, hover_color, font):
        """
        Initialise un bouton

        Args:
            x (int): Position X
            y (int): Position Y
            width (int): Largeur du bouton
            height (int): Hauteur du bouton
            text (str): Texte affiché
            color (tuple): Couleur normale (R, G, B)
            hover_color (tuple): Couleur au survol (R, G, B)
            font: Police pygame pour le texte
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = font

    def draw(self, surface):
        """
        Dessine le bouton

        Args:
            surface: Surface pygame où dessiner
        """
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 3)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Gère les événements du bouton

        Args:
            event: Événement pygame

        Returns:
            bool: True si le bouton a été cliqué, False sinon
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def update_text(self, new_text):
        """
        Met à jour le texte du bouton

        Args:
            new_text (str): Nouveau texte à afficher
        """
        self.text = new_text
