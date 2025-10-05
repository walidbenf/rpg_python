"""
Module pour les personnages du jeu
"""
import pygame
import random
import os
from .constants import (
    WHITE, GREEN, RED, GRAY, DARK_GRAY, GOLD, LIGHT_BLUE,
    DEFENSE_REDUCTION, ATTACK_VARIANCE
)


class Character:
    """Classe de base pour les personnages"""

    def __init__(self, name, hp, max_hp, attack, defense, x, y, color=None):
        """
        Initialise un personnage

        Args:
            name (str): Nom du personnage
            hp (int): Points de vie actuels
            max_hp (int): Points de vie maximum
            attack (int): Puissance d'attaque
            defense (int): Défense
            x (int): Position X à l'écran
            y (int): Position Y à l'écran
            color (tuple): Couleur du personnage (R, G, B) - optionnel
        """
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.x = x
        self.y = y
        self.is_defending = False
        self.base_color = color  # Couleur personnalisée pour les ennemis

    def take_damage(self, damage):
        """
        Applique les dégâts au personnage

        Args:
            damage (int): Dégâts bruts reçus

        Returns:
            int: Dégâts réellement subis après défense
        """
        actual_damage = max(1, damage - self.defense)
        if self.is_defending:
            actual_damage = int(actual_damage * DEFENSE_REDUCTION)
        self.hp -= actual_damage
        self.hp = max(0, self.hp)
        return actual_damage

    def attack_target(self, target):
        """
        Attaque une cible

        Args:
            target (Character): La cible à attaquer

        Returns:
            int: Dégâts infligés
        """
        damage = self.attack + random.randint(-ATTACK_VARIANCE, ATTACK_VARIANCE)
        actual_damage = target.take_damage(damage)
        return actual_damage

    def heal(self, amount):
        """
        Soigne le personnage

        Args:
            amount (int): Quantité de HP à restaurer

        Returns:
            int: HP réellement restaurés
        """
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def is_alive(self):
        """
        Vérifie si le personnage est vivant

        Returns:
            bool: True si vivant, False sinon
        """
        return self.hp > 0

    def draw(self, surface, font_small):
        """
        Dessine le personnage à l'écran

        Args:
            surface: Surface pygame où dessiner
            font_small: Police pour le texte
        """
        # Corps (cercle coloré selon HP)
        if self.base_color:
            # Utilise la couleur personnalisée pour les ennemis
            color = self.base_color if self.hp > 0 else GRAY
        else:
            # Couleur dynamique basée sur les HP pour le joueur
            color = GREEN if self.hp > self.max_hp // 2 else RED if self.hp > 0 else GRAY
        pygame.draw.circle(surface, color, (self.x, self.y), 40)

        # Nom
        name_text = font_small.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x, self.y - 60))
        surface.blit(name_text, name_rect)

        # Barre de vie
        bar_width = 100
        bar_height = 10
        bar_x = self.x - bar_width // 2
        bar_y = self.y + 50

        # Fond de la barre
        pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))

        # Barre de vie actuelle
        hp_ratio = self.hp / self.max_hp
        current_bar_width = int(bar_width * hp_ratio)
        hp_color = GREEN if hp_ratio > 0.5 else GOLD if hp_ratio > 0.25 else RED
        pygame.draw.rect(surface, hp_color, (bar_x, bar_y, current_bar_width, bar_height))

        # Bordure
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        # Texte HP
        hp_text = font_small.render(f"{self.hp}/{self.max_hp}", True, WHITE)
        hp_rect = hp_text.get_rect(center=(self.x, bar_y + bar_height + 15))
        surface.blit(hp_text, hp_rect)

        # Indicateur de défense
        if self.is_defending:
            shield_text = font_small.render("🛡️", True, LIGHT_BLUE)
            surface.blit(shield_text, (self.x + 30, self.y - 30))


class ImageCharacter(Character):
    """Classe pour les personnages avec des images (sprites)"""

    def __init__(self, name, hp, max_hp, attack, defense, x, y, image_path, scale=2):
        """
        Initialise un personnage avec image

        Args:
            name (str): Nom du personnage
            hp (int): Points de vie actuels
            max_hp (int): Points de vie maximum
            attack (int): Puissance d'attaque
            defense (int): Défense
            x (int): Position X à l'écran
            y (int): Position Y à l'écran
            image_path (str): Chemin vers l'image du personnage
            scale (int): Facteur d'échelle pour l'image (default: 2)
        """
        super().__init__(name, hp, max_hp, attack, defense, x, y)

        # Charger l'image
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            # Mettre à l'échelle l'image
            width = self.original_image.get_width() * scale
            height = self.original_image.get_height() * scale
            self.image = pygame.transform.scale(self.original_image, (int(width), int(height)))
            self.rect = self.image.get_rect(center=(x, y))
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image {image_path}: {e}")
            self.image = None
            self.rect = None

    def draw(self, surface, font_small):
        """
        Dessine le personnage avec son image à l'écran

        Args:
            surface: Surface pygame où dessiner
            font_small: Police pour le texte
        """
        # Dessiner l'image si elle existe
        if self.image and self.rect:
            # Appliquer un effet si mort
            if self.hp <= 0:
                # Image en gris si mort
                gray_image = self.image.copy()
                gray_image.fill((128, 128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(gray_image, self.rect)
            else:
                surface.blit(self.image, self.rect)
        else:
            # Fallback sur le dessin par défaut si l'image n'a pas pu être chargée
            super().draw(surface, font_small)
            return

        # Nom
        name_text = font_small.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x, self.y - self.rect.height // 2 - 20))
        surface.blit(name_text, name_rect)

        # Barre de vie
        bar_width = 100
        bar_height = 10
        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.rect.height // 2 + 10

        # Fond de la barre
        pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))

        # Barre de vie actuelle
        hp_ratio = self.hp / self.max_hp
        current_bar_width = int(bar_width * hp_ratio)
        hp_color = GREEN if hp_ratio > 0.5 else GOLD if hp_ratio > 0.25 else RED
        pygame.draw.rect(surface, hp_color, (bar_x, bar_y, current_bar_width, bar_height))

        # Bordure
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        # Texte HP
        hp_text = font_small.render(f"{self.hp}/{self.max_hp}", True, WHITE)
        hp_rect = hp_text.get_rect(center=(self.x, bar_y + bar_height + 15))
        surface.blit(hp_text, hp_rect)

        # Indicateur de défense
        if self.is_defending:
            shield_text = font_small.render("🛡️", True, LIGHT_BLUE)
            surface.blit(shield_text, (self.x + self.rect.width // 2, self.y - self.rect.height // 2))
