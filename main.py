import pygame
from pathlib import Path
import random

#Initialise pygame

pygame.init()

#Donne un titre à la fenêtre

pygame.display.set_caption("Trump Invaders 1.0")

largeur_ecran = 1024
hauteur_ecran = 800

#définit le taille de la fenêtre

screen = pygame.display.set_mode((largeur_ecran, hauteur_ecran))

#initialisation de la page menu

etat_jeu = "menu"

#gérer le son du jeu

pygame.mixer.init()

#afficher le score du jeu

pygame.font.init()


#crée le chemin vers le dossier ressources pour récupérer les images et autres

DOSSIER_PROJET = Path(__file__).resolve().parent

#son missile
son_missile = pygame.mixer.Sound(str(DOSSIER_PROJET / "ressources" / "missile.wav"))
#son explosion
son_explosion = pygame.mixer.Sound(str(DOSSIER_PROJET / "ressources" / "explosion.wav"))
#son game over
son_game_over = str(DOSSIER_PROJET / "ressources" / "gameover.mp3")
#son menu accueil
son_main_menu = str(DOSSIER_PROJET / "ressources" / "main_menu.mp3")
#son du jeu
son_jeu = str(DOSSIER_PROJET / "ressources" / "jeu.mp3")

def changer_musique(musique):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(musique)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

def changer_musique_game_over(musique):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(musique)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(0)


#  HIGHSCORE : fichier pour stocker le score le plus élevé

FICHIER_HIGHSCORE = DOSSIER_PROJET / "highscore.txt"

def charger_highscore():
    # Lire le contenu du fichier et le convertir en entier, ou retourner 0 si le fichier n'existe pas ou est vide
    try:
        return int(FICHIER_HIGHSCORE.read_text())
    except (FileNotFoundError, ValueError):
        return 0

def sauvegarder_highscore(valeur):
    # Écrire la valeur du score dans le fichier
    FICHIER_HIGHSCORE.write_text(str(valeur))

highscore = charger_highscore()
nouveau_record = False   

#Ajout de la police du texte

titre = pygame.font.Font(str(DOSSIER_PROJET / "ressources" / "DS-DIGI.TTF"), 72) 
police_score = pygame.font.Font(str(DOSSIER_PROJET / "ressources" / "DS-DIGI.TTF"), 50)
police_rejouer = pygame.font.Font(str(DOSSIER_PROJET / "ressources" / "DS-DIGI.TTF"), 30)

#ajoute le fond d'écran du jeu

background = pygame.image.load(str(DOSSIER_PROJET / "ressources" / "background.png")).convert()

background = pygame.transform.scale(background, (largeur_ecran, hauteur_ecran))

#ajoute le fond d ecran d'accueil du jeu

background_menu = pygame.image.load(str(DOSSIER_PROJET / "ressources" / "ecrans_accueil.png")).convert()

background_menu = pygame.transform.scale(background_menu, (largeur_ecran, hauteur_ecran))

#ajoute le fond d'écrand de game over

background_gameover = pygame.image.load(str(DOSSIER_PROJET / "ressources" / "game_over.png")).convert()

background_menu = pygame.transform.scale(background_menu, (largeur_ecran, hauteur_ecran))

if etat_jeu == "menu":
    
    screen.blit(background_menu, (0, 0))
    changer_musique(son_main_menu)

#ajout d'une horloge pour créer le framerate du jeu 

clock = pygame.time.Clock()

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self._scoreCourant = 0
        self._setText()

    def _setText(self):
        self.surf = police_score.render("Score :" + str(self._scoreCourant), True, (255, 255, 255))
        self.rect = self.surf.get_rect(center = (largeur_ecran - 900, 25))

    def update(self):
        self._setText()

    def incremente(self, valeur):
        self._scoreCourant = self._scoreCourant + valeur

#Création du vaisseau en tant que sprite / objet

class Vaisseau(pygame.sprite.Sprite):
    def __init__(self):
        super(Vaisseau, self).__init__()
        #ajoute l'image du vaisseau et la redimensionne pour qu elle soit adapté à l'écran
        self.surf = pygame.image.load(str(DOSSIER_PROJET / "ressources" / "vaisseau.png")).convert_alpha() # type: ignore
        self.surf = pygame.transform.scale(self.surf, (150, 120)) # type: ignore
        #initialise la position du vaisseau au centre de  l'éfcran
        self.rect = self.surf.get_rect(center = (100, hauteur_ecran/2))
        self.rect.inflate_ip(-50, -50)
#Déplacement du vaisseau et tir de missile
    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -7)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 7)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-7, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(7, 0)
        if pressed_keys[pygame.K_SPACE]:
            
            if len(le_missile.sprites()) < 1:
                missile = Missile(self.rect.center) 
                all_sprite.add(missile) 
                le_missile.add(missile)
        
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > 1024:
            self.rect.right = 1024

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > 800:
            self.rect.bottom = 800   

#création de la classe missile pour gérer les missiles du vaisseau
class Missile(pygame.sprite.Sprite):
    def __init__(self, center_missile):
        super().__init__()
        self.surf = pygame.image.load(str(DOSSIER_PROJET / "ressources" / "missile.png")).convert_alpha() 
        self.surf = pygame.transform.scale(self.surf, (40, 20))
        self.rect = self.surf.get_rect(center = center_missile) 
        #supprime le missile quand il sort de l'écran
        son_missile.play()
        son_missile.set_volume(0.2)
    def update(self):
        self.rect.move_ip(15, 0)
        if self.rect.left > largeur_ecran:
            self.kill()

#création de la classe ennemis
class Ennemis(pygame.sprite.Sprite):
    def __init__(self):
        super(Ennemis, self).__init__()
        self.surf = pygame.image.load(str(DOSSIER_PROJET / "ressources" / "ennemi.png")).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100, 80))
        self.rect = self.surf.get_rect(center = (largeur_ecran + 25, random.randint(0, hauteur_ecran)))
        self.rect.inflate_ip(-30, -30)
        self.speed = random.randint(5, 20)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#création de la classe explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_vaisseau):
        super(Explosion, self).__init__()
        self._compteur = 5
        self.surf = pygame.image.load(str(DOSSIER_PROJET / "ressources" / "explosion.png")).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100, 80))
        self.rect = self.surf.get_rect(center = center_vaisseau)
        son_explosion.play()
        son_explosion.set_volume(0.7)
    def update(self):
        self._compteur -= 1
        if self._compteur == 0:
            self.kill()

#ajout du vaisseau à l'écran et à la liste des sprites

vaisseau = Vaisseau() 
score = Score()

#Appeler tous les sprites du jeu pour les gérer plus facilement

all_sprite = pygame.sprite.Group()
le_missile = pygame.sprite.Group()
les_ennemis = pygame.sprite.Group()
les_explosions = pygame.sprite.Group()

#ajoute les vaisseau et le score dans all sprite pour les actualiser
all_sprite.add(vaisseau) 
all_sprite.add(score)

# Ajoute un ennemi toutes les 500 millisecondes

AJOUTE_ENNEMY = pygame.USEREVENT + 1
pygame.time.set_timer(AJOUTE_ENNEMY, 500)  


#initialisation de la boucle du jeu

continuer = True

#Lancement de la boucle pour faire tourner le jeu 

while continuer:
    #Gestion des évenements du jeu 
    for event in pygame.event.get():
        #Gestion de la fermetiure de la fenêtre du jeu
        if event.type == pygame.QUIT:
            continuer = False
        #Gestion de la touche echap pour quitter le jeu et la touche espace pour lancer le jeu ou relancer le jeu après un game over
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                continuer = False
        
            if event.key == pygame.K_SPACE and etat_jeu == "menu":
                etat_jeu = "jeu"
                changer_musique(son_jeu)

            if event.key == pygame.K_RETURN and etat_jeu == "game_over":
                etat_jeu = "jeu"
                changer_musique(son_jeu)
                score._scoreCourant = 0
                les_ennemis.empty()
                le_missile.empty()
                les_explosions.empty()
                all_sprite.empty()
                all_sprite.add(vaisseau)
                all_sprite.add(score)
                vaisseau.rect.center = (100, hauteur_ecran/2)   #type: ignore
        #Gestion de l'ajout d'ennemis toutes les 500 ms
        elif event.type == AJOUTE_ENNEMY and etat_jeu == "jeu":
            nouvel_ennemi = Ennemis()
            all_sprite.add(nouvel_ennemi)
            les_ennemis.add(nouvel_ennemi)
    # Initialise les sprites et les updates   
    if etat_jeu == "jeu":    
            
        screen.blit(background, (0, 0))

        screen.blit(vaisseau.surf, vaisseau.rect) # type: ignore 

        touche_appuyee = pygame.key.get_pressed()
            
        vaisseau.update(touche_appuyee) # type: ignore
        
        le_missile.update()
        
        les_ennemis.update()

        les_explosions.update()

        score.update()
        # Prend en compte les explosion en cas de contact entre le vaisseau et les têtes de trump
        if pygame.sprite.spritecollideany(vaisseau, les_ennemis): # type: ignore
            explosion = Explosion(vaisseau.rect.center)
            etat_jeu = "game_over"
            changer_musique_game_over(son_game_over)
            les_explosions.add(explosion)
            all_sprite.add(explosion)

            # Vérifie si le score actuel est supérieur au highscore et met à jour le fichier si nécessaire
            if score._scoreCourant > highscore:
                highscore = score._scoreCourant
                nouveau_record = False
                sauvegarder_highscore(highscore)
                nouveau_record = True

        #lance une boucle et ajoute dans une liste les missiles qui ont détruis les ennemis 
        for missile in le_missile:
            liste_ennemis_touches = pygame.sprite.spritecollide(missile, les_ennemis, True)
            # Détruit les missiles une fois qu'ils ont touché leur cible
            if len(liste_ennemis_touches) > 0:
                missile.kill()
            #Provoque l'explosion lorsque le missile touche sa cible
            for ennemi in liste_ennemis_touches:
                score.incremente(100)
                explosion = Explosion(ennemi.rect.center)
                les_explosions.add(explosion)
                all_sprite.add(explosion)
        #permet d"actualiser les sprites
        for mon_sprite in all_sprite:
            screen.blit(mon_sprite.surf, mon_sprite.rect) # type:ignore
                    #permet d"actualiser les sprites
        for mon_sprite in all_sprite:
            screen.blit(mon_sprite.surf, mon_sprite.rect) # type:ignore

        # HIGHSCORE pendant le jeu
        meilleur = max(highscore, score._scoreCourant)
        texte_hs = police_score.render(f"Highscore : {meilleur}", True, (255, 215, 0))
        texte_hs_rect = texte_hs.get_rect(topright=(largeur_ecran - 20, 5))
        screen.blit(texte_hs, texte_hs_rect)

    #lance l'écrans de game over
    if etat_jeu == "game_over":

        screen.blit(background_gameover, (0, 0))    
        background_gameover = pygame.transform.scale(background_gameover, (largeur_ecran, hauteur_ecran))

        # Créer un panneau semi-transparent
        panneau = pygame.Surface((largeur_ecran - 500, 200), pygame.SRCALPHA)
        panneau.fill((0, 0, 0, 190))
        panneau_rect = panneau.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 + 175))
        screen.blit(panneau, panneau_rect)

        # Titre "GAME OVER" en rouge
        texte_game_over = titre.render("GAME OVER", True, (255, 50, 50))
        screen.blit(texte_game_over, texte_game_over.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 + 85)))

        # Pontuation finale en blanc
        texte_score_final = police_score.render(f"Score final : {score._scoreCourant}", True, (255, 255, 255))
        screen.blit(texte_score_final, texte_score_final.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 + 150)))

        # HIGHSCORE
        if nouveau_record:
            texte_highscore = police_score.render(f"NOUVEAU RECORD : {highscore} !", True, (255, 215, 0))
        else:
            texte_highscore = police_score.render(f"Highscore : {highscore}", True, (255, 215, 0))
        screen.blit(texte_highscore, texte_highscore.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 + 205)))
        

        # Invite à rejouer en jaune
        texte_rejouer = police_rejouer.render("ENTREE : REJOUER", True, (255, 220, 0))
        texte_rejouer_rect = texte_rejouer.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 + 215))
        screen.blit(texte_rejouer, texte_rejouer_rect)

        #Echape pour quitter
        texte_quitter = police_rejouer.render("ECHAP : QUTTER", True, (255, 220, 0))
        texte_quitter_rect = texte_rejouer.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 + 250))
        screen.blit(texte_quitter, texte_quitter_rect)
    pygame.display.flip()
    #vitessse du jeu (60 images /seconde)
    clock.tick(60)

pygame.quit


