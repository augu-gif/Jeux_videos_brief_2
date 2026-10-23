# Space Invaders

Un jeu vidéo développé en Python avec Pygame dans le cadre de mon apprentissage du développement de jeux vidéo.

## Fonctionnalités

- Affichage d'un vaisseau spatial
- Affichage d'un arrière-plan
- Système de missiles

*Les fonctionnalités présentées seront complétées au fur et à mesure du développement.*

## Technologies

- Python 3
- Pygame

## Prérequis

- Python 3.10 ou supérieur
- Git
- pip

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/augu-gif/Jeux_videos_brief_2
cd Jeux_videos_brief_2
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
```

### 3. Activer l'environnement virtuel

Sous Linux et macOS :

```bash
source .venv/bin/activate
```

Sous Windows :

```powershell
.venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
pip install pygame
```

### 5. Lancer le jeu

```bash
python main.py
```

## Structure du projet

```text
space-invaders/
├── main.py
├── requirements.txt
├── README.md
└── ressources/
    ├── vaisseau.png
    ├── background.png
    └── missile.png
```

## Configuration des ressources

Les images sont stockées dans le dossier `ressources/`. Le jeu doit utiliser des chemins relatifs au projet plutôt qu'un chemin spécifique à un ordinateur.

Exemple recommandé :

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESSOURCES_DIR = BASE_DIR / "ressources"

vaisseau = pygame.image.load(
    str(RESSOURCES_DIR / "vaisseau.png")
).convert_alpha()
```

## Dépendances

Le fichier `requirements.txt` contient les bibliothèques Python nécessaires au projet.

## Auteur

Augustin Montruil

Ingrid Gusmão


