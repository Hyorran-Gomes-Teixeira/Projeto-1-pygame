import math
import random
import pygame.draw
import pygame
import os
import sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)


pygame.init()
pygame.mixer.init()

som_tiro = pygame.mixer.Sound("tiro.mp3")
som_explosao = pygame.mixer.Sound("explosao.mp3")

tela_largura = 800
tela_altura = 600

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
RED = (255, 0, 0)

tela = pygame.display.set_mode((tela_largura, tela_altura))
borda = 5

player = 30
player = pygame.Rect((300, 530, player, player))
player_veloc = 1

enemy_tamanho = 30
enemy = pygame.Rect((600, 200, enemy_tamanho, enemy_tamanho))

bloco1 = pygame.Rect((100, 450, 100, 50))
bloco2 = pygame.Rect((350, 450, 100, 50))
bloco3 = pygame.Rect((600, 450, 100, 50))
bloco_invisivel = pygame.Rect((5, 410, 800, 190))
vida_bloco1 = 10
vida_bloco2 = 10
vida_bloco3 = 10

tiros = []
tiro_larg = 5
tiro_alt = 10
tiro_veloc = 1
tiro_enemy = []


pygame.display.set_caption("Tiro and tiros")
fonte = pygame.font.Font(None, 36)
pontos = 0

run = True
while run:
    tela.fill((PRETO))
    pygame.draw.rect(tela, (0, 0, 0), bloco_invisivel)
    pygame.draw.rect(tela, BRANCO, (0, 0, tela_largura, tela_altura), borda)
    pygame.draw.rect(tela, (255, 255, 255), player)

    if vida_bloco1 > 0:
        pygame.draw.rect(tela, (255, 255, 255), bloco1)
    if vida_bloco2 > 0:
        pygame.draw.rect(tela, (255, 255, 255), bloco2)
    if vida_bloco3 > 0:
        pygame.draw.rect(tela, (255, 255, 255), bloco3)

    if enemy:
        pygame.draw.rect(tela, (255, 0, 0), enemy)

    if enemy:
        for tiro in tiros:
            tiro.move_ip(0, -tiro_veloc)
            if tiro.bottom < 0:
                tiros.remove(tiro)

    if enemy:
        for tiro in tiro_enemy:
            tiro.move_ip(0, tiro_veloc)
            if tiro.top > tela_altura:
                tiro_enemy.remove(tiro)

    for tiro in tiros:
        if tiro.colliderect(enemy):
            tiros.remove(tiro)
            enemy = None
            pontos += 1
            som_explosao.play()
            break

    for tiro in tiro_enemy:
        if tiro.colliderect(player):
            tiro_enemy.remove(tiro)
            run = False
            break

    for tiro in tiro_enemy:
        if tiro.colliderect(bloco1) and vida_bloco1 > 0:
            vida_bloco1 -= 1
            tiro_enemy.remove(tiro)
        elif tiro.colliderect(bloco2) and vida_bloco2 > 0:
            vida_bloco2 -= 1
            tiro_enemy.remove(tiro)
        elif tiro.colliderect(bloco3) and vida_bloco3 > 0:
            vida_bloco3 -= 1
            tiro_enemy.remove(tiro)

    while not enemy or enemy.colliderect(bloco_invisivel):
        enemy_x = random.randint(borda, tela_largura - borda - enemy_tamanho)
        enemy_y = random.randint(borda, tela_altura - borda - enemy_tamanho)
        enemy = pygame.Rect(enemy_x, enemy_y, enemy_tamanho, enemy_tamanho)

    if random.randint(0, 1000) < 1:
        novo_tiro_enemy = pygame.Rect(enemy.centerx - tiro_larg // 2,
                                      enemy.bottom, tiro_larg, tiro_alt)
        tiro_enemy.append(novo_tiro_enemy)

    for tiro in tiro_enemy:
        pygame.draw.rect(tela, RED, tiro)

    for tiro in tiros:
        pygame.draw.rect(tela, BRANCO, tiro)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] and player.left > borda:
        player.move_ip(-player_veloc, 0)

    elif key[pygame.K_d] and player.right < tela_largura - borda:
        player.move_ip(player_veloc, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                novo_tiro = pygame.Rect(player.centerx - tiro_larg // 2,
                                        player.top - tiro_alt, tiro_larg,
                                        tiro_alt)
                tiros.append(novo_tiro)
                som_tiro.play()

    texto_pontos = fonte.render("Pontos: " + str(pontos), True, BRANCO)
    tela.blit(texto_pontos, (10, 10))

    if vida_bloco1 > 0:
        texto_bloco1 = fonte.render("" + str(vida_bloco1), True, PRETO)
        tela.blit(texto_bloco1, (bloco1.x + bloco1.width // 2 - 10,
                                 bloco1.y + bloco1.height // 2 - 10))

    if vida_bloco2 > 0:
        texto_bloco2 = fonte.render(str(vida_bloco2), True, PRETO)
        tela.blit(texto_bloco2, (bloco2.x + bloco2.width // 2 - 10,
                                 bloco2.y + bloco2.height // 2 - 10))

    if vida_bloco3 > 0:
        texto_bloco3 = fonte.render(str(vida_bloco3), True, PRETO)
        tela.blit(texto_bloco3, (bloco3.x + bloco3.width // 2 - 10,
                                 bloco3.y + bloco3.height // 2 - 10))

    pygame.display.update()
pygame.quit()
