import pygame
import sys
from utils.classes import Reta

# 1. Inicialização ⚙️
pygame.init() # "Liga" todos os módulos do Pygame

# 2. Configuração da Tela 🖥️
largura = 800
altura = 600
# Cria a janela onde vamos desenhar
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Meu Quadro Branco de CG")

# Define algumas cores no formato RGB (Red, Green, Blue)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Preenche o fundo da tela de branco
tela.fill(BRANCO)

# 3. Loop Principal 🔄
rodando = True
modo_atual = "livre"
pontos_reta = []
array_estruturas = []
while rodando:
    # 4. Captura de Eventos (ex: clicar)
    for evento in pygame.event.get():
        if evento.type == pygame.MOUSEBUTTONDOWN:
            tupla = evento.pos

            if (tupla[0] < 100 and tupla[1] < 40):
                if modo_atual == "livre":
                    modo_atual = "reta"
                    print(f"Mudando o modo para {modo_atual}")
                    continue

            if modo_atual == "reta":
                if len(pontos_reta) < 2:
                    pontos_reta.append(tupla)
                    print("Primeiro clique capturado")
                if len(pontos_reta) == 2:
                    # desenhar_reta_DDA(pontos_reta[0], pontos_reta[1])
                    reta = Reta(pontos_reta[0], pontos_reta[1])
                    reta.reta_dda(tela)
                    array_estruturas.append(reta)
                    pontos_reta.clear()
                    modo_atual = "livre"
                    print(f"Mudando o modo para {modo_atual}")
                    continue

            if modo_atual == "livre": 
                print(f"Desenhando em {tupla[0]}, {tupla[1]}")
                for i in range(0, 800):
                    tela.set_at((i, tupla[1]), PRETO)
                for j in range(0, 600):
                    tela.set_at((tupla[0], j), PRETO)

        if evento.type == pygame.QUIT:
            rodando = False

   
    pygame.draw.rect(tela, (0, 0, 200), (0, 0, 100, 40))

    # 5. Atualização da Tela
    # Pega tudo o que foi desenhado na memória e joga para o monitor
    pygame.display.flip()

# Encerra o programa limparemente
pygame.quit()
sys.exit()