import pygame
import sys
from utils.classes import Reta

def desenhar_reta_DDA(t1, t2):
    print("Traçando reta usando o algoritmo DDA")
    
    # Extrai as coordenadas X e Y das tuplas
    x1, y1 = t1
    x2, y2 = t2
    
    # 1. Calcula as diferenças (Deltas)
    dx = x2 - x1
    dy = y2 - y1
    
    # 2. Descobre o número total de passos baseando-se no maior deslocamento absoluto
    passos = max(abs(dx), abs(dy))
    
    # Proteção: Se a pessoa clicou duas vezes exatamente no mesmo pixel
    if passos == 0:
        tela.set_at((x1, y1), PRETO)
        return
        
    # 3. Calcula a taxa de incremento para os eixos (Isso vai gerar números com decimais)
    x_inc = dx / passos
    y_inc = dy / passos
    
    # 4. Define o ponto de partida (usamos float porque vamos somar decimais a eles)
    x = float(x1)
    y = float(y1)
    
    # 5. Loop de rasterização: damos um passo de cada vez até o destino
    for i in range(passos + 1):
        # Arredonda a posição atual para o pixel inteiro mais próximo e pinta
        tela.set_at((round(x), round(y)), PRETO)
        
        # Prepara a posição para o próximo pixel da iteração seguinte
        x += x_inc
        y += y_inc

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