# 🎮 RPG Roguelike Tour par Tour

Un roguelike en tour par tour où tu dois gravir une tour de 20 étages remplie de monstres de plus en plus puissants !

## 📋 Description

Ce projet est un RPG roguelike où le joueur affronte des ennemis dans un système de combat au tour par tour. Progresse à travers les étages, améliore ton personnage, gère tes ressources et essaie d'atteindre le sommet de la tour ! Chaque victoire te permet de choisir une récompense pour devenir plus fort, mais attention : une seule mort et c'est le game over !

## ✨ Fonctionnalités

### 🏰 Système Roguelike
- **20 étages à conquérir** avec difficulté progressive
- **5 types d'ennemis** : Goblin, Orc, Troll, Démon, Dragon
- **Ennemis qui deviennent plus forts** à chaque étage
- **Permadeath** : Une seule vie par run !
- **Score et statistiques** détaillées

### ⚔️ Combat Tour par Tour
- **3 actions stratégiques** :
  - 🗡️ **Attaquer** : Inflige des dégâts à l'ennemi
  - 🛡️ **Défendre** : Réduit les dégâts reçus de 50%
  - 🧪 **Potion** : Restaure 30 HP (stockage limité)

### 🎁 Système de Progression
- **Récompenses après chaque victoire** (choix parmi) :
  - +15 HP Maximum
  - +3 Attaque
  - +2 Défense
  - +2 Potions
- **Soins entre les étages** : 30% de tes HP max restaurés
- **Système d'or** : Accumule de l'or pour ton score

### 🎨 Interface
- Barres de vie colorées et dynamiques
- Ennemis avec couleurs uniques par type
- Messages de combat en temps réel
- Boutons interactifs avec effets de survol
- Statistiques affichées en permanence
- Écrans de victoire/défaite détaillés

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd /home/wawa/pygame
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   # ou
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Comment jouer

### Lancer le jeu

```bash
python main.py
```

### Commandes

- **Clic gauche** : Sélectionner une action (Attaquer, Défendre, Potion)
- **ESPACE** : Recommencer après une victoire ou une défaite
- **ESC** : Quitter le jeu

### Règles du jeu

1. **Tour du joueur** : Choisissez une action parmi les trois disponibles
2. **Tour de l'ennemi** : L'ennemi attaque automatiquement
3. **Victoire** : Réduire les HP de l'ennemi à 0
4. **Défaite** : Si vos HP tombent à 0

### Statistiques de départ

#### 🦸 Héros
- HP : 100
- Attaque : 20
- Défense : 5
- Potions : 3

#### 👹 Ennemis (Stats de base)

**Goblin** (Étages 1-3)
- HP : 40 | Attaque : 12 | Défense : 2 | Or : 10

**Orc** (Étages 4-6)
- HP : 70 | Attaque : 18 | Défense : 5 | Or : 25

**Troll** (Étages 7-10)
- HP : 100 | Attaque : 22 | Défense : 8 | Or : 40

**Démon** (Étages 11-15)
- HP : 140 | Attaque : 28 | Défense : 10 | Or : 60

**Dragon** (Étages 16-20)
- HP : 200 | Attaque : 35 | Défense : 15 | Or : 100

_Note : Les stats augmentent de 10% par étage !_

## 📁 Structure du projet

```
pygame/
│
├── main.py              # Point d'entrée du jeu
├── requirements.txt     # Dépendances Python
├── README.md           # Ce fichier
│
├── src/                # Code source
│   ├── __init__.py     # Init du package
│   ├── constants.py    # Constantes du jeu
│   ├── character.py    # Classe Character
│   ├── ui.py          # Éléments d'interface (Button)
│   └── game.py        # Logique principale du jeu
│
└── assets/            # Ressources (actuellement vide)
    ├── fonts/         # Polices personnalisées
    └── sounds/        # Effets sonores
```

## 🛠️ Architecture

Le projet suit une architecture modulaire :

- **constants.py** : Centralise toutes les constantes (couleurs, dimensions, stats)
- **character.py** : Gère les personnages (joueur et ennemis)
- **ui.py** : Composants d'interface utilisateur réutilisables
- **game.py** : Boucle de jeu et logique de combat
- **main.py** : Point d'entrée minimal qui orchestre le tout

## 🎨 Personnalisation

### Modifier les stats des personnages

Éditez `src/constants.py` :
```python
# Stats du joueur
PLAYER_HP = 100
PLAYER_ATTACK = 20
PLAYER_DEFENSE = 5

# Stats de l'ennemi
ENEMY_HP = 60
ENEMY_ATTACK = 15
ENEMY_DEFENSE = 3
```

### Ajouter des couleurs

Ajoutez de nouvelles couleurs dans `src/constants.py` :
```python
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
```

### Modifier le gameplay

- **Potions** : Changez `POTION_HEAL_AMOUNT` et `STARTING_POTIONS`
- **Défense** : Modifiez `DEFENSE_REDUCTION` (0.5 = 50% de réduction)
- **Variance d'attaque** : Ajustez `ATTACK_VARIANCE`

## � Stratégies et Conseils

- **Gère tes potions** : Ne les utilise pas trop tôt !
- **La défense est utile** : Surtout contre les ennemis puissants
- **Équilibre tes améliorations** : Ne néglige ni l'attaque, ni la défense, ni les HP
- **Les premiers étages** : Faciles, mais ne sous-estime pas les suivants
- **Les Dragons** : Très dangereux, prépare-toi bien avant !

## �🔮 Améliorations futures

Idées pour étendre le jeu :

- [ ] Compétences spéciales avec cooldowns
- [ ] Plus de types de récompenses (multiplicateurs, vol de vie, etc.)
- [ ] Événements aléatoires (marchands, fontaines de soin, pièges)
- [ ] Boss spéciaux tous les 5 étages
- [ ] IA ennemie plus variée (patterns d'attaque, compétences)
- [ ] Système de sauvegarde de runs
- [ ] Musique et effets sonores
- [ ] Animations de combat plus élaborées
- [ ] Différentes classes de héros
- [ ] Mode endless (étages infinis)
- [ ] Classement/leaderboard des meilleurs scores

## 📝 Licence

Projet libre à des fins éducatives.

## 👨‍💻 Auteur

Créé pour apprendre Pygame et le développement de jeux en Python.

---

**Bon jeu ! 🎮**
