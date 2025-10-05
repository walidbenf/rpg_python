"""
Module principal du jeu - Gestion de la logique de jeu (Roguelike)
"""
import pygame
import random
import os
from .character import Character, ImageCharacter
from .ui import Button
from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE,
    GOLD, GRAY, PURPLE, PLAYER_HP, PLAYER_ATTACK, PLAYER_DEFENSE, PLAYER_X, PLAYER_Y,
    ENEMY_X, ENEMY_Y, STARTING_POTIONS, POTION_HEAL_AMOUNT,
    ENEMY_ACTION_DELAY, MESSAGE_DURATION, ENEMY_TYPES, MAX_FLOOR, FLOOR_HEAL_PERCENT, DARK_GRAY
)


class Game:
    """Classe principale du jeu - Version Roguelike"""

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

        # Statistiques de la run
        self.floor = 1
        self.gold = 0
        self.enemies_killed = 0
        self.total_damage_dealt = 0
        self.total_damage_taken = 0

        # Stats de base du joueur (pour reset)
        self.base_hp = PLAYER_HP
        self.base_attack = PLAYER_ATTACK
        self.base_defense = PLAYER_DEFENSE

        # Personnages
        self.player = None
        self.enemy = None
        self._init_player()
        self._spawn_enemy()

        # Inventaire
        self.potions = STARTING_POTIONS

        # État du jeu
        self.state = "player_turn"  # player_turn, enemy_turn, victory, rewards, game_over, pause
        self.message = f"Étage {self.floor} - À l'attaque !"
        self.message_timer = MESSAGE_DURATION
        self.return_to_menu = False  # Flag pour signaler le retour au menu

        # Boutons
        self.action_buttons = []
        self.reward_buttons = []
        self.pause_buttons = []
        self._create_action_buttons()
        self._create_pause_buttons()

    def _init_player(self):
        """Initialise ou réinitialise le joueur"""
        if self.player is None:
            # Chemin vers l'image du personnage
            image_path = os.path.join("assets", "fonts", "characters", "rogue-mage.png")

            # Créer le joueur avec l'image
            self.player = ImageCharacter(
                "Rogue Mage",
                self.base_hp,
                self.base_hp,
                self.base_attack,
                self.base_defense,
                PLAYER_X,
                PLAYER_Y,
                image_path,
                scale=3  # Ajustez la taille selon vos besoins
            )
        else:
            # Conserve les stats actuelles pour la progression
            self.player.x = PLAYER_X
            self.player.y = PLAYER_Y
            self.player.is_defending = False

    def _spawn_enemy(self):
        """Génère un ennemi basé sur l'étage actuel"""
        # Détermine le type d'ennemi selon l'étage
        if self.floor <= 3:
            enemy_type = "goblin"
        elif self.floor <= 6:
            enemy_type = random.choice(["goblin", "orc"])
        elif self.floor <= 10:
            enemy_type = random.choice(["orc", "troll"])
        elif self.floor <= 15:
            enemy_type = random.choice(["troll", "demon"])
        else:
            enemy_type = random.choice(["demon", "dragon"])

        # Récupère les stats de l'ennemi
        enemy_data = ENEMY_TYPES[enemy_type]

        # Scaling basé sur l'étage (augmente légèrement les stats)
        floor_multiplier = 1 + (self.floor - 1) * 0.1
        hp = int(enemy_data["hp"] * floor_multiplier)
        attack = int(enemy_data["attack"] * floor_multiplier)
        defense = int(enemy_data["defense"] * floor_multiplier)

        self.enemy = Character(
            enemy_data["name"],
            hp, hp, attack, defense,
            ENEMY_X, ENEMY_Y,
            enemy_data["color"]
        )
        self.enemy.gold_reward = int(enemy_data["gold"] * floor_multiplier)

    def _create_action_buttons(self):
        """Crée les boutons d'action"""
        button_y = 500
        button_spacing = 210
        self.action_buttons = [
            Button(50, button_y, 180, 60, "Attaquer", RED,
                  (255, 100, 100), self.font_medium),
            Button(50 + button_spacing, button_y, 180, 60, "Défendre", BLUE,
                  (100, 100, 255), self.font_medium),
            Button(50 + button_spacing * 2, button_y, 180, 60,
                  f"Potion ({self.potions})", GREEN, (100, 255, 100), self.font_medium),
        ]

    def _create_reward_buttons(self):
        """Crée les boutons de récompense après victoire"""
        center_x = SCREEN_WIDTH // 2
        button_y = 300
        button_spacing = 120

        self.reward_buttons = [
            Button(center_x - 260, button_y, 160, 70, "+15 HP Max", RED,
                  (255, 100, 100), self.font_medium),
            Button(center_x - 85, button_y, 160, 70, "+3 Attaque", PURPLE,
                  (180, 100, 234), self.font_medium),
            Button(center_x + 90, button_y, 160, 70, "+2 Défense", BLUE,
                  (100, 100, 255), self.font_medium),
        ]

        # Ajoute un bouton potion si le joueur en a moins de 5
        if self.potions < 5:
            self.reward_buttons.append(
                Button(center_x - 85, button_y + button_spacing, 160, 70,
                      "+2 Potions", GREEN, (100, 255, 100), self.font_medium)
            )

    def _create_pause_buttons(self):
        """Crée les boutons du menu pause"""
        center_x = SCREEN_WIDTH // 2
        button_y = 250
        button_spacing = 100

        self.pause_buttons = [
            Button(center_x - 125, button_y, 250, 60, "Reprendre", GREEN,
                  (100, 255, 100), self.font_medium),
            Button(center_x - 125, button_y + button_spacing, 250, 60,
                  "Retour au Menu", RED, (255, 100, 100), self.font_medium),
        ]

    def update_potion_button(self):
        """Met à jour le texte du bouton potion"""
        if len(self.action_buttons) > 2:
            self.action_buttons[2].update_text(f"Potion ({self.potions})")

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
            self.total_damage_dealt += damage
            self.show_message(f"Tu infliges {damage} dégâts !")

            if not self.enemy.is_alive():
                self.enemies_killed += 1
                self.gold += self.enemy.gold_reward
                self.state = "rewards"
                self.show_message(f"Victoire ! +{self.enemy.gold_reward} Or", 300)
                self._create_reward_buttons()
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
        self.total_damage_taken += damage
        self.show_message(f"{self.enemy.name} t'inflige {damage} dégâts !")

        if not self.player.is_alive():
            self.state = "game_over"
            self.show_message("Défaite... Game Over !", 300)
            return

        # Retour au tour du joueur
        self.state = "player_turn"

    def apply_reward(self, reward_type):
        """
        Applique une récompense choisie par le joueur

        Args:
            reward_type (str): Type de récompense
        """
        if reward_type == "hp":
            self.player.max_hp += 15
            heal = self.player.heal(15)
            self.show_message(f"+15 HP Max ! ({heal} HP restaurés)")
        elif reward_type == "attack":
            self.player.attack += 3
            self.show_message("+3 Attaque ! Tu es plus fort !")
        elif reward_type == "defense":
            self.player.defense += 2
            self.show_message("+2 Défense ! Tu es plus résistant !")
        elif reward_type == "potions":
            self.potions += 2
            self.update_potion_button()
            self.show_message("+2 Potions ! Garde-les précieusement !")

        # Passe à l'étage suivant
        self._next_floor()

    def _next_floor(self):
        """Passe à l'étage suivant"""
        self.floor += 1

        # Vérifier si le joueur a gagné
        if self.floor > MAX_FLOOR:
            self.state = "victory_final"
            self.show_message(f"Tu as conquis la tour ! Score: {self.gold}", 500)
            return

        # Soigne légèrement le joueur entre les étages
        heal_amount = int(self.player.max_hp * FLOOR_HEAL_PERCENT)
        healed = self.player.heal(heal_amount)

        # Génère un nouvel ennemi
        self._spawn_enemy()

        # Réinitialise l'état
        self.state = "player_turn"
        self.show_message(f"Étage {self.floor} - {self.enemy.name} apparaît ! (+{healed} HP)", MESSAGE_DURATION * 2)
        self.reward_buttons = []

    def reset_game(self):
        """Réinitialise le jeu complètement"""
        self.floor = 1
        self.gold = 0
        self.enemies_killed = 0
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        self.potions = STARTING_POTIONS

        # Réinitialise le joueur aux stats de base
        self.player = Character("Héros", self.base_hp, self.base_hp,
                               self.base_attack, self.base_defense, PLAYER_X, PLAYER_Y)

        self._spawn_enemy()
        self.state = "player_turn"
        self.message = f"Nouvelle aventure ! Étage {self.floor}"
        self.update_potion_button()
        self.reward_buttons = []

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
                pygame.time.set_timer(pygame.USEREVENT, 0)
                self.enemy_action()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Basculer entre pause et jeu
                    if self.state == "pause":
                        self.state = self.previous_state
                    elif self.state in ["player_turn", "enemy_turn", "victory", "rewards"]:
                        self.previous_state = self.state
                        self.state = "pause"

                # Redémarrer avec ESPACE
                if event.key == pygame.K_SPACE and (self.state == "game_over" or self.state == "victory_final"):
                    self.reset_game()

            # Gestion du menu pause
            if self.state == "pause":
                for i, button in enumerate(self.pause_buttons):
                    if button.handle_event(event):
                        if i == 0:  # Reprendre
                            self.state = self.previous_state
                        elif i == 1:  # Retour au menu
                            self.return_to_menu = True
                        break

            # Gestion des boutons d'action
            elif self.state == "player_turn":
                for i, button in enumerate(self.action_buttons):
                    if button.handle_event(event):
                        actions = ["attack", "defend", "potion"]
                        if i < len(actions):
                            self.player_action(actions[i])

            # Gestion des boutons de récompense
            elif self.state == "rewards":
                for i, button in enumerate(self.reward_buttons):
                    if button.handle_event(event):
                        rewards = ["hp", "attack", "defense", "potions"]
                        if i < len(rewards):
                            self.apply_reward(rewards[i])
                        break

            # Mettre à jour l'état de survol des boutons
            for button in self.action_buttons + self.reward_buttons:
                button.handle_event(event)

        return True

    def update(self):
        """Met à jour la logique du jeu"""
        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self):
        """Dessine le jeu"""
        # Fond
        self.screen.fill(DARK_GRAY)

        # Titre et informations d'étage
        title = self.font_large.render(f"Etage {self.floor}/{MAX_FLOOR}", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title, title_rect)

        # Statistiques (or, ennemis tués)
        stats_y = 80
        gold_text = self.font_small.render(f"Or: {self.gold}", True, GOLD)
        kills_text = self.font_small.render(f"Ennemis: {self.enemies_killed}", True, WHITE)
        self.screen.blit(gold_text, (20, stats_y))
        self.screen.blit(kills_text, (150, stats_y))

        # Dessiner les personnages
        if self.player:
            self.player.draw(self.screen, self.font_small)
        if self.enemy and self.state not in ["rewards", "game_over", "victory_final"]:
            self.enemy.draw(self.screen, self.font_small)

        # Message
        if self.message_timer > 0 or self.state in ["game_over", "victory_final"]:
            message_color = GREEN if self.state == "victory_final" else RED if self.state == "game_over" else WHITE
            message_surface = self.font_medium.render(self.message, True, message_color)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))

            # Fond du message
            padding = 20
            bg_rect = message_rect.inflate(padding * 2, padding)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, message_color, bg_rect, 3)

            self.screen.blit(message_surface, message_rect)

        # Boutons d'action (pendant le tour du joueur)
        if self.state == "player_turn":
            for button in self.action_buttons:
                button.draw(self.screen)

        # Boutons de récompense
        elif self.state == "rewards":
            # Titre des récompenses
            reward_title = self.font_large.render("Choisis ta recompense !", True, GOLD)
            reward_rect = reward_title.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(reward_title, reward_rect)

            for button in self.reward_buttons:
                button.draw(self.screen)

        # Indicateur de tour
        turn_text = ""
        turn_color = WHITE
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

        # Écran de game over avec statistiques
        if self.state == "game_over":
            self._draw_game_over()

        # Écran de victoire finale
        elif self.state == "victory_final":
            self._draw_victory()

        # Menu pause
        elif self.state == "pause":
            self._draw_pause_menu()

        # Instructions
        if self.state in ["game_over", "victory_final"]:
            restart_text = self.font_small.render("Appuie sur ESPACE pour recommencer", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(restart_text, restart_rect)
        elif self.state != "pause":
            help_text = self.font_small.render("ESC pour menu pause", True, GRAY)
            self.screen.blit(help_text, (10, SCREEN_HEIGHT - 30))

        pygame.display.flip()

    def _draw_game_over(self):
        """Dessine l'écran de game over avec statistiques"""
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        spacing = 35

        stats = [
            f"Etage atteint: {self.floor}",
            f"Ennemis vaincus: {self.enemies_killed}",
            f"Or collecte: {self.gold}",
            f"Degats infliges: {self.total_damage_dealt}",
            f"Degats subis: {self.total_damage_taken}",
        ]

        for i, stat in enumerate(stats):
            stat_surface = self.font_medium.render(stat, True, WHITE)
            stat_rect = stat_surface.get_rect(center=(center_x, start_y + i * spacing))
            self.screen.blit(stat_surface, stat_rect)

    def _draw_victory(self):
        """Dessine l'écran de victoire finale"""
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        spacing = 35

        # Message de félicitations
        congrats = self.font_large.render("VICTOIRE TOTALE !", True, GOLD)
        congrats_rect = congrats.get_rect(center=(center_x, 200))
        self.screen.blit(congrats, congrats_rect)

        stats = [
            f"Score Final: {self.gold} Or",
            f"Ennemis vaincus: {self.enemies_killed}",
            f"Degats infliges: {self.total_damage_dealt}",
        ]

        for i, stat in enumerate(stats):
            stat_surface = self.font_medium.render(stat, True, WHITE)
            stat_rect = stat_surface.get_rect(center=(center_x, start_y + i * spacing))
            self.screen.blit(stat_surface, stat_rect)

    def _draw_pause_menu(self):
        """Dessine le menu pause"""
        # Overlay semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Titre
        title = self.font_large.render("PAUSE", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Dessiner les boutons
        for button in self.pause_buttons:
            button.draw(self.screen)

        # Instruction
        help_text = self.font_small.render("ESC pour reprendre", True, WHITE)
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(help_text, help_rect)
