import pygame
import random
from pygame import *

LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600

class Vaisseau(pygame.sprite.Sprite):

    def __init__(self):
        super(Vaisseau, self).__init__()
        self.surf = pygame.image.load("src/ressources/vaisseau.png").convert()
        self.surf = pygame.transform.scale(self.surf, (60, 50))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            if len(le_missile.sprites()) < 1:
                missile = Missile(self.rect.center)
                tous_sprites.add(missile)
                le_missile.add(missile)
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN

class Missile(pygame.sprite.Sprite):
    def __init__(self, center_missile):
        super(Missile, self).__init__()
        self.surf = pygame.image.load("src/ressources/missile.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (40, 20))
        self.rect = self.surf.get_rect(center=center_missile)

    def update(self):
        self.rect.move_ip(15, 0)
        if self.rect.left > LARGEUR_ECRAN:
            self.kill()

class Ennemi(pygame.sprite.Sprite):
    def __init__(self):
        super(Ennemi, self).__init__()
        self.surf = pygame.image.load("src/ressources/ennemi.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (50, 80))
        self.rect = self.surf.get_rect(center=(LARGEUR_ECRAN + 50, random.randint(0, HAUTEUR_ECRAN)))
        self.speed = random.randint(5, 5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_vaisseau):
        super(Explosion, self).__init__()
        self._compteur = 10
        self.surf = pygame.image.load("src/ressources/missile.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100, 80))
        self.rect = self.surf.get_rect(center=center_vaisseau)

    def update(self):
        self._compteur = self._compteur - 1
        if self._compteur == 0:
            self.kill()

class Etoile(pygame.sprite.Sprite):
    def __init__(self):
        super(Etoile, self).__init__()
        self.surf = pygame.image.load("src/ressources/etoile.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (20, 20))
        self.rect = self.surf.get_rect(
            center=(
                LARGEUR_ECRAN + 40,
                random.randint(100, HAUTEUR_ECRAN)))

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.scoreCourant = 0
        self._setText()

    def _setText(self):
        self.surf = police_score.render(
            'Score : ' + str(self.scoreCourant), False, (255, 255, 255))  
        self.rect = self.surf.get_rect(
            center=(LARGEUR_ECRAN / 2, 15)
            )
    def update(self):
        self._setText()

    def incrementer(self, valeur):
        self.scoreCourant = self.scoreCourant + valeur

pygame.font.init()

police_score = pygame.font.SysFont("Arial", 36)

pygame.init()
pygame.display.set_caption("Mon jeu Pygame")

AJOUTER_ENNEMI = pygame.USEREVENT + 1
pygame.time.set_timer(AJOUTER_ENNEMI, 500)
AJOUTER_ETOILE = pygame.USEREVENT + 2
pygame.time.set_timer(AJOUTER_ETOILE, 80)

clock = pygame.time.Clock()

ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))

tous_sprites = pygame.sprite.Group()
le_missile = pygame.sprite.Group()
les_ennemies = pygame.sprite.Group()
les_explosions = pygame.sprite.Group()
les_etoiles = pygame.sprite.Group()


vaisseau = Vaisseau()
tous_sprites.add(vaisseau)
score = Score()
tous_sprites.add(score)

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        elif event.type == AJOUTER_ENNEMI:
            nouvel_ennemi = Ennemi()
            les_ennemies.add(nouvel_ennemi)
            tous_sprites.add(nouvel_ennemi)
        elif event.type == AJOUTER_ETOILE:
            nouvelle_etoile = Etoile()
            les_etoiles.add(nouvelle_etoile)

    ecran.fill((0, 0, 0))
    
    if pygame.sprite.spritecollideany(vaisseau, les_ennemies):
        vaisseau.kill()
        explosion = Explosion(vaisseau.rect.center)
        les_explosions.add(explosion)
        tous_sprites.add(explosion)
        continuer = False

    for missile in le_missile:
        liste_ennemis_touches = pygame.sprite.spritecollide(missile, les_ennemies, True)
        if len(liste_ennemis_touches) > 0:
            missile.kill()
            score.incrementer(len(liste_ennemis_touches))
        for ennemi in liste_ennemis_touches:
            explosion = Explosion(ennemi.rect.center)
            les_explosions.add(explosion)
            tous_sprites.add(explosion)

    touche_appuyee = pygame.key.get_pressed()
    vaisseau.update(touche_appuyee)
    le_missile.update()
    les_ennemies.update()
    les_explosions.update()
    les_etoiles.update()
    score.update()

    for mon_sprite in tous_sprites:
        ecran.blit(mon_sprite.surf, mon_sprite.rect)
    
    # 1º: fundo (estrelas)
    for etoile in les_etoiles:
        ecran.blit(etoile.surf, etoile.rect)

    # 2º: nave, inimigos, mísseis, explosões
    for mon_sprite in tous_sprites:
        ecran.blit(mon_sprite.surf, mon_sprite.rect)

    ecran.blit(vaisseau.surf, vaisseau.rect)    

    pygame.display.flip()

    clock.tick(30)

pygame.time.delay(3000)

pygame.quit()