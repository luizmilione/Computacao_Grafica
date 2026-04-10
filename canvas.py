import pygame
import sys
from utils.classes import Reta, Circunferencia

# 1. Inicialização ⚙️
pygame.init() # "Liga" todos os módulos do Pygame

# 2. Configuração da Tela 🖥️
largura = 1500
altura = 850
# Cria a janela onde vamos desenhar
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Meu Quadro Branco de CG")

# Define algumas cores no formato RGB (Red, Green, Blue)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 200)
VERMELHO = (200, 0, 0)

# Preenche o fundo da tela de branco
tela.fill(BRANCO)

# Menu de interação
fonte_menu = pygame.font.SysFont(None, 30)
# Reta DDA
pygame.draw.rect(tela, AZUL, (0, 0, 100, 40))
imagem_texto = fonte_menu.render("DDA", True, BRANCO)
tela.blit(imagem_texto, (25, 10))
# Reta Bresenham
pygame.draw.rect(tela, VERMELHO, (100, 0, 110, 40))
imagem_texto = fonte_menu.render("Bresenham", True, BRANCO)
tela.blit(imagem_texto, (100, 10))
# Circulo Bresenham
pygame.draw.rect(tela, AZUL, (210, 0, 110, 40))
imagem_texto = fonte_menu.render("Circulo", True, BRANCO)
tela.blit(imagem_texto, (215, 10))


# 3. Loop Principal 🔄
rodando = True
modo_atual = "livre"
pontos_reta = []
array_estruturas = []
texto_digitado = ""
while rodando:
    # 4. Captura de Eventos (ex: clicar)
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if modo_atual == "circulo":
                if evento.key == pygame.K_BACKSPACE:
                    # Removemos a última letra da nossa variável
                    texto_digitado = texto_digitado[:-1]
                else:
                    # evento.unicode pega o caractere exato que foi digitado
                    caractere = evento.unicode
                    # Só adiciona na tela se for um número
                    if caractere.isdigit():
                        texto_digitado += caractere
                # Desenhamos na tela o número digitado até agora
                pygame.draw.rect(tela, BRANCO, (993, 0, 500, 40))
                imagem_texto = fonte_menu.render(texto_digitado, True, PRETO)
                tela.blit(imagem_texto, (993, 10))
        if evento.type == pygame.MOUSEBUTTONDOWN:
            tupla = evento.pos

            # Usuário clicou no menu
            if (tupla[1] < 40):
                print(f"Pontos X: {tupla[0]}, Y: {tupla[1]}")
                if tupla[0] < 100:
                    modo_atual = "reta"
                    print(f"Mudando o modo para {modo_atual}")
                    pontos_reta.clear()
                    continue
                elif tupla[0] >= 100 and tupla[0] < 210:
                    modo_atual = "reta2"
                    print(f"Mudando o modo para {modo_atual}")
                    pontos_reta.clear()
                    continue
                elif tupla[0] >= 210 and tupla[0] < 330:
                    modo_atual = "circulo"
                    print(f"Mudando o modo para {modo_atual}")
                    pontos_reta.clear()
                    imagem_texto = fonte_menu.render("Digite o Raio do circulo: ", True, PRETO)
                    tela.blit(imagem_texto, (750, 10))
                    continue

            # Estamos capturando os cliques que querem fazer uma reta
            if modo_atual == "reta" or modo_atual == "reta2":
                if len(pontos_reta) < 2:
                    pontos_reta.append(tupla)
                    print("Primeiro clique capturado")
                if len(pontos_reta) == 2:
                    # Instanciando uma reta
                    reta = Reta(pontos_reta[0], pontos_reta[1])
                    if modo_atual == "reta":
                        reta.reta_dda(tela)
                    else:
                        reta.reta_bresenham(tela)
                    array_estruturas.append(reta)
                    pontos_reta.clear()
                    modo_atual = "livre"
                    print(f"Mudando o modo para {modo_atual}")
                    continue

            if modo_atual == "circulo":
                if texto_digitado != "":
                    circulo = Circunferencia(tupla[0], tupla[1], int(texto_digitado))
                    circulo.circ_Bresenham(tela)
                    array_estruturas.append(circulo)
                    modo_atual = "livre"
                    texto_digitado = ""
                    print(f"Mudando o modo para {modo_atual}")
                    pygame.draw.rect(tela, BRANCO, (750, 0, 750, 40))
                    continue


            # if modo_atual == "livre": 
            #     print(f"Desenhando em {tupla[0]}, {tupla[1]}")
            #     for i in range(0, 800):
            #         tela.set_at((i, tupla[1]), PRETO)
            #     for j in range(0, 600):
            #         tela.set_at((tupla[0], j), PRETO)

        if evento.type == pygame.QUIT:
            rodando = False

   


    # 5. Atualização da Tela
    # Pega tudo o que foi desenhado na memória e joga para o monitor
    pygame.display.flip()

# Encerra o programa limparemente
pygame.quit()
sys.exit()