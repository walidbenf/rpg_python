"""
Module principal du jeu - Gestion de la logique de jeu
"""
import pygame
from .character import Character
from .ui import Button
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE,
    GOLD, GRAY, PLAYER_HP, PLAYER_ATTACK, PLAYER_DEFENSE, PLAYER_X, PLAYER_Y,
    ENEMY_HP, ENEMY_ATTACK, ENEMY_DEFENSE, ENEMY_X, ENEMY_Y,
    STARTING_POTIONS, POTION_HEAL_AMOUNT, ENEMY_ACTION_DELAY, MESSAGE_DURATION
)


class Game:
    """Classe principale du jeu"""

    def __init__(self, screen, font_large, font_medium, font_small):
        """
        Initialise le jeu

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

        # Personnages
        self.player = Character("Héros", PLAYER_HP, PLAYER_HP, PLAYER_ATTACK,
                                PLAYER_DEFENSE, PLAYER_X, PLAYER_Y)
        self.enemy = Character("Goblin", ENEMY_HP, ENEMY_HP, ENEMY_ATTACK,
                              ENEMY_DEFENSE, ENEMY_X, ENEMY_Y)

        # Inventaire
        self.potions = STARTING_POTIONS

        # État du jeu
        self.state = "player_turn"  # player_turn, enemy_turn, victory, defeat
        self.message = "À ton tour !"
        self.message_timer = 0

        # Boutons d'action
        self._create_buttons()

    def _create_buttons(self):
        """Crée les boutons d'action"""
        button_y = 500
        button_spacing = 210
        self.buttons = [
            Button(50, button_y, 180, 60, "Attaquer", RED,
                  (255, 100, 100), self.font_medium),
            Button(50 + button_spacing, button_y, 180, 60, "Défendre", BLUE,
                  (100, 100, 255), self.font_medium),
            Button(50 + button_spacing * 2, button_y, 180, 60,
                  f"Potion ({self.potions})", GREEN, (100, 255, 100), self.font_medium),
        ]

    def update_potion_button(self):
        """Met à jour le texte du bouton potion"""
        self.buttons[2].update_text(f"Potion ({self.potions})")

    def show_message(self, message, duration=MESSAGE_DURATION):
        """
        Affiche un message temporaire

        Args:
            message (str): Message à afficher
            duration (int): Durée en frames
        """
        self.message = message
        self.message_timer = duration

    def player_action(self, action):
        """
        Exécute l'action du joueur

        Args:
            action (str): Type d'action ('attack', 'defend', 'potion')
        """
        if self.state != "player_turn":
            return

        self.player.is_defending = False

        if action == "attack":
            damage = self.player.attack_target(self.enemy)
            self.show_message(f"Tu infliges {damage} dégâts !")

            if not self.enemy.is_alive():
                self.state = "victory"
                self.show_message("Victoire ! Tu as vaincu l'ennemi !", 300)
                return

        elif action == "defend":
            self.player.is_defending = True
            self.show_message("Tu te défends ! Dégâts réduits de 50%")

        elif action == "potion":
            if self.potions > 0:
                healed = self.player.heal(POTION_HEAL_AMOUNT)
                self.potions -= 1
                self.update_potion_button()
                self.show_message(f"Tu te soignes de {healed} HP !")
            else:
                self.show_message("Plus de potions !")
                return

        # Passer au tour de l'ennemi
        self.state = "enemy_turn"
        pygame.time.set_timer(pygame.USEREVENT, ENEMY_ACTION_DELAY)

    def enemy_action(self):
        """L'ennemi effectue son action"""
        if self.state != "enemy_turn":
            return

        self.enemy.is_defending = False

        # L'ennemi attaque toujours (IA simple)
        damage = self.enemy.attack_target(self.player)
        self.show_message(f"{self.enemy.name} t'inflige {damage} dégâts !")

        if not self.player.is_alive():
            self.state = "defeat"
            self.show_message("Défaite... Tu as été vaincu !", 300)
            return

        # Retour au tour du joueur
        self.state = "player_turn"

    def reset_game(self):
        """Réinitialise le jeu"""
        self.player = Character("Héros", PLAYER_HP, PLAYER_HP, PLAYER_ATTACK,
                                PLAYER_DEFENSE, PLAYER_X, PLAYER_Y)
        self.enemy = Character("Goblin", ENEMY_HP, ENEMY_HP, ENEMY_ATTACK,
                              ENEMY_DEFENSE, ENEMY_X, ENEMY_Y)
        self.potions = STARTING_POTIONS
        self.state = "player_turn"
        self.message = "Nouveau combat ! À ton tour !"
        self.update_potion_button()

    def handle_events(self):
        """
        Gère les événements du jeu

        Returns:
            bool: False si on doit quitter, True sinon
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.USEREVENT:
                # Timer pour l'action de l'ennemi
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Désactive le timer
                self.enemy_action()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                # Redémarrer avec ESPACE
                if event.key == pygame.K_SPACE and (self.state == "victory" or self.state == "defeat"):
                    self.reset_game()

            # Gestion des boutons
            if self.state == "player_turn":
                if self.buttons[0].handle_event(event):
                    self.player_action("attack")
                elif self.buttons[1].handle_event(event):
                    self.player_action("defend")
                elif self.buttons[2].handle_event(event):
                    self.player_action("potion")

            # Mettre à jour l'état de survol des boutons
            for button in self.buttons:
                button.handle_event(event)

        return True

    def update(self):
        """Met à jour la logique du jeu"""
        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self):
        """Dessine le jeu"""
        # Fond
        from .constants import DARK_GRAY
        self.screen.fill(DARK_GRAY)

        # Titre
        title = self.font_large.render("RPG Tour par Tour", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title, title_rect)

        # Dessiner les personnages
        self.player.draw(self.screen, self.font_small)
        self.enemy.draw(self.screen, self.font_small)

        # Message
        if self.message_timer > 0 or self.state in ["victory", "defeat"]:
            message_color = GREEN if self.state == "victory" else RED if self.state == "defeat" else WHITE
            message_surface = self.font_medium.render(self.message, True, message_color)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))

            # Fond du message
            padding = 20
            bg_rect = message_rect.inflate(padding * 2, padding)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, message_color, bg_rect, 3)

            self.screen.blit(message_surface, message_rect)

        # Boutons (seulement pendant le tour du joueur)
        if self.state == "player_turn":
            for button in self.buttons:
                button.draw(self.screen)

        # Indicateur de tour
        turn_text = ""
        if self.state == "player_turn":
            turn_text = "Ton Tour"
            turn_color = GREEN
        elif self.state == "enemy_turn":
            turn_text = "Tour Ennemi"
            turn_color = RED

        if turn_text:
            turn_surface = self.font_medium.render(turn_text, True, turn_color)
            turn_rect = turn_surface.get_rect(center=(SCREEN_WIDTH // 2, 420))
            self.screen.blit(turn_surface, turn_rect)

        # Instructions de fin de jeu
        if self.state in ["victory", "defeat"]:
            restart_text = self.font_small.render("Appuie sur ESPACE pour recommencer", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(restart_text, restart_rect)

        # Instructions générales
        help_text = self.font_small.render("ESC pour quitter", True, GRAY)
        self.screen.blit(help_text, (10, SCREEN_HEIGHT - 30))

        pygame.display.flip()
