"""
Constantes du jeu RPG
"""

# Dimensions de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 50, 220)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GOLD = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (147, 51, 234)
ORANGE = (255, 140, 0)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)

# Stats du joueur
PLAYER_HP = 100
PLAYER_ATTACK = 20
PLAYER_DEFENSE = 5
PLAYER_X = 200
PLAYER_Y = 300

# Position des ennemis
ENEMY_X = 600
ENEMY_Y = 300

# Types d'ennemis - Structure : (nom, hp, attaque, défense, couleur, récompense_or)
ENEMY_TYPES = {
    "goblin": {
        "name": "Goblin",
        "hp": 40,
        "attack": 12,
        "defense": 2,
        "color": GREEN,
        "gold": 10
    },
    "orc": {
        "name": "Orc",
        "hp": 70,
        "attack": 18,
        "defense": 5,
        "color": ORANGE,
        "gold": 25
    },
    "troll": {
        "name": "Troll",
        "hp": 100,
        "attack": 22,
        "defense": 8,
        "color": PURPLE,
        "gold": 40
    },
    "demon": {
        "name": "Démon",
        "hp": 140,
        "attack": 28,
        "defense": 10,
        "color": DARK_RED,
        "gold": 60
    },
    "dragon": {
        "name": "Dragon",
        "hp": 200,
        "attack": 35,
        "defense": 15,
        "color": GOLD,
        "gold": 100
    }
}

# Objets
STARTING_POTIONS = 3
POTION_HEAL_AMOUNT = 30

# Gameplay
DEFENSE_REDUCTION = 0.5  # Réduction de 50% des dégâts en défense
ATTACK_VARIANCE = 3  # Variance aléatoire de l'attaque (+/- X)
ENEMY_ACTION_DELAY = 1500  # Délai en ms avant l'action de l'ennemi
MESSAGE_DURATION = 120  # Durée d'affichage des messages (frames)

# Roguelike
MAX_FLOOR = 20  # Nombre d'étages maximum
FLOOR_HEAL_PERCENT = 0.3  # Pourcentage de HP restaurés entre les étages
