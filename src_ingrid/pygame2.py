# 
# IMPORTAÇÕES
# 
import pygame                 # biblioteca de jogos
import random                 # para gerar números aleatórios (posição, velocidade)
from pygame.locals import *   # traz as constantes do pygame: K_UP, K_SPACE, RLEACCEL...

# 
# CONSTANTES (valores que não mudam durante o jogo)
# 
LARGEUR_ECRAN = 800   # largura da janela, em pixels
HAUTEUR_ECRAN = 600   # altura da janela, em pixels


# 
# CLASSE VAISSEAU (a nave do jogador)
# Herda de pygame.sprite.Sprite: ganha tudo que um "objeto do jogo" já sabe fazer
# 
class Vaisseau(pygame.sprite.Sprite):

    def __init__(self):
        # Inicializa a parte herdada do Sprite (sempre a primeira linha)
        super(Vaisseau, self).__init__()

        # Carrega a imagem da nave e ajusta o tamanho para 60x50
        self.surf = pygame.image.load("src/ressources/vaisseau.png").convert()
        self.surf = pygame.transform.scale(self.surf, (60, 50))

        # Torna o preto (0, 0, 0) transparente
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # O "rect" guarda a posição e o tamanho da nave (começa no canto 0,0)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        # --- Movimento com as setas do teclado ---
        # move_ip(x, y) desloca a nave; no pygame o y cresce para BAIXO
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # --- Tiro com a barra de espaço ---
        # Só cria um míssil novo se não houver nenhum na tela (1 tiro por vez)
        if pressed_keys[K_SPACE]:
            if len(le_missile.sprites()) < 1:
                missile = Missile(self.rect.center)  # sai do centro da nave
                tous_sprites.add(missile)            # para ser desenhado
                le_missile.add(missile)              # para ser contado/colidir

        # --- Impede a nave de sair da tela ---
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN


# 
# CLASSE MISSILE (o tiro da nave)
# 
class Missile(pygame.sprite.Sprite):
    def __init__(self, center_missile):
        super(Missile, self).__init__()
        # convert_alpha() mantém a transparência do PNG
        self.surf = pygame.image.load("src/ressources/missile.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (40, 20))
        # O míssil nasce na posição recebida (o centro da nave)
        self.rect = self.surf.get_rect(center=center_missile)

    def update(self):
        # Anda 15 pixels para a direita a cada quadro
        self.rect.move_ip(15, 0)
        # Se saiu pela direita da tela, é removido de todos os grupos
        if self.rect.left > LARGEUR_ECRAN:
            self.kill()


# 
# CLASSE ENNEMI (os inimigos)
# 
class Ennemi(pygame.sprite.Sprite):
    def __init__(self):
        super(Ennemi, self).__init__()
        self.surf = pygame.image.load("src/ressources/ennemi.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (50, 80))
        # Nasce logo depois da borda direita, numa altura aleatória
        self.rect = self.surf.get_rect(
            center=(LARGEUR_ECRAN + 50, random.randint(0, HAUTEUR_ECRAN))
        )
        # Velocidade (randint(5, 5) dá sempre 5; use ex. (3, 8) para variar)
        self.speed = random.randint(5, 5)

    def update(self):
        # Anda para a esquerda na sua velocidade
        self.rect.move_ip(-self.speed, 0)
        # Se saiu pela esquerda, é removido
        if self.rect.right < 0:
            self.kill()


# 
# CLASSE EXPLOSION (aparece por alguns quadros e some)
# 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_vaisseau):
        super(Explosion, self).__init__()
        # Contador: a explosão dura 10 quadros
        self._compteur = 10
        # Obs.: está usando a imagem do míssil; troque por uma de explosão se tiver
        self.surf = pygame.image.load("src/ressources/missile.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100, 80))
        self.rect = self.surf.get_rect(center=center_vaisseau)

    def update(self):
        # Diminui o contador; quando chega a zero, a explosão desaparece
        self._compteur = self._compteur - 1
        if self._compteur == 0:
            self.kill()


# 
# CLASSE ETOILE (estrelas do fundo, passando da direita para a esquerda)
# 
class Etoile(pygame.sprite.Sprite):
    def __init__(self):
        super(Etoile, self).__init__()
        self.surf = pygame.image.load("src/ressources/etoile.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (20, 20))
        # Nasce fora da tela, à direita, numa altura aleatória
        # (começa em 100 para não passar por cima do placar)
        self.rect = self.surf.get_rect(
            center=(LARGEUR_ECRAN + 40, random.randint(100, HAUTEUR_ECRAN))
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# 
# CLASSE SCORE (o placar, desenhado como texto)
# 
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.scoreCourant = 0   # pontuação atual
        self._setText()

    def _setText(self):
        # Transforma o texto em imagem (render) para poder desenhar na tela
        self.surf = police_score.render(
            'Score : ' + str(self.scoreCourant), False, (255, 255, 255)
        )
        # Centralizado no topo da tela
        self.rect = self.surf.get_rect(center=(LARGEUR_ECRAN / 2, 15))

    def update(self):
        # Recria o texto a cada quadro, com a pontuação atualizada
        self._setText()

    def incrementer(self, valeur):
        # Soma pontos ao placar
        self.scoreCourant = self.scoreCourant + valeur


# 
# INICIALIZAÇÃO DO PYGAME E DA JANELA
# 
pygame.init()                                  # liga todos os módulos do pygame
pygame.display.set_caption("Mon jeu Pygame")   # título da janela

# Fonte usada pelo placar
police_score = pygame.font.SysFont("Arial", 36)

# --- Eventos personalizados com temporizador ---
# USEREVENT é um número livre para criar eventos próprios
AJOUTER_ENNEMI = pygame.USEREVENT + 1
pygame.time.set_timer(AJOUTER_ENNEMI, 500)   # dispara a cada 500 ms
AJOUTER_ETOILE = pygame.USEREVENT + 2
pygame.time.set_timer(AJOUTER_ETOILE, 80)    # dispara a cada 80 ms

clock = pygame.time.Clock()   # controla a velocidade do jogo (quadros por segundo)

# Cria a janela do jogo
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))


# 
# GRUPOS DE SPRITES
# Um grupo é uma "caixa" que guarda vários sprites para tratar todos juntos
# 
tous_sprites = pygame.sprite.Group()     # tudo que deve ser desenhado (menos o fundo)
le_missile = pygame.sprite.Group()       # só os mísseis
les_ennemies = pygame.sprite.Group()     # só os inimigos (para colisões)
les_explosions = pygame.sprite.Group()   # só as explosões
les_etoiles = pygame.sprite.Group()      # só as estrelas (fundo)

# Cria a nave e o placar e coloca no grupo geral
vaisseau = Vaisseau()
tous_sprites.add(vaisseau)
score = Score()
tous_sprites.add(score)


# 
# LOOP PRINCIPAL DO JOGO
# Roda várias vezes por segundo até o jogo acabar
# 
continuer = True
while continuer:

    # 
    # 1. EVENTOS: fechar janela, criar inimigos e estrelas
    # 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:          # clicou no X da janela
            continuer = False
        elif event.type == AJOUTER_ENNEMI:     # hora de criar um inimigo
            nouvel_ennemi = Ennemi()
            les_ennemies.add(nouvel_ennemi)
            tous_sprites.add(nouvel_ennemi)
        elif event.type == AJOUTER_ETOILE:     # hora de criar uma estrela
            nouvelle_etoile = Etoile()
            les_etoiles.add(nouvelle_etoile)   # fica fora de tous_sprites (é fundo)

    # 
    # 2. COLISÕES
    # 
    # Nave bateu em algum inimigo -> explosão e fim de jogo
    if pygame.sprite.spritecollideany(vaisseau, les_ennemies):
        vaisseau.kill()
        explosion = Explosion(vaisseau.rect.center)
        les_explosions.add(explosion)
        tous_sprites.add(explosion)
        continuer = False

    # Míssil acertou inimigos -> some o míssil, somem os inimigos, ganha pontos
    for missile in le_missile:
        # O True remove automaticamente os inimigos atingidos
        liste_ennemis_touches = pygame.sprite.spritecollide(missile, les_ennemies, True)
        if len(liste_ennemis_touches) > 0:
            missile.kill()
            score.incrementer(len(liste_ennemis_touches))   # 1 ponto por inimigo
        for ennemi in liste_ennemis_touches:
            explosion = Explosion(ennemi.rect.center)
            les_explosions.add(explosion)
            tous_sprites.add(explosion)

    # 
    # 3. ATUALIZAÇÃO: move tudo
    # 
    touche_appuyee = pygame.key.get_pressed()   # estado de todas as teclas agora
    vaisseau.update(touche_appuyee)
    le_missile.update()       # chama update() de cada míssil do grupo
    les_ennemies.update()
    les_explosions.update()
    les_etoiles.update()
    score.update()

    # 
    # 4. DESENHO: a ordem importa (o que vem depois fica por cima)
    # 
    ecran.fill((0, 0, 0))   # apaga a tela com preto

    # 1º: o fundo (estrelas)
    for etoile in les_etoiles:
        ecran.blit(etoile.surf, etoile.rect)

    # 2º: nave, inimigos, mísseis, explosões e placar
    for mon_sprite in tous_sprites:
        ecran.blit(mon_sprite.surf, mon_sprite.rect)

    pygame.display.flip()   # mostra na tela tudo que foi desenhado

    # 
    # 5. VELOCIDADE: no máximo 30 quadros por segundo
    # 
    clock.tick(30)



# FIM DE JOGO

pygame.time.delay(3000)   # espera 3 segundos mostrando a explosão
pygame.quit()             # fecha o pygame (sempre fora do while)