PRETO = (0, 0, 0)

class Reta:
    def __init__(self, t1, t2):
        # Extrai as coordenadas X e Y das tuplas
        self.x1, self.y1 = t1
        self.x2, self.y2 = t2

    def reta_dda(self, tela):
        print("Traçando reta usando DDA")
        # 1. Calcula as diferenças (Deltas)
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        
        # 2. Descobre o número total de passos baseando-se no maior deslocamento absoluto
        passos = max(abs(dx), abs(dy))
        
        # Proteção: Se a pessoa clicou duas vezes exatamente no mesmo pixel
        if passos == 0:
            tela.set_at((self.x1, self.y1), PRETO)
            return
            
        # 3. Calcula a taxa de incremento para os eixos (Isso vai gerar números com decimais)
        x_inc = dx / passos
        y_inc = dy / passos
        
        # 4. Define o ponto de partida (usamos float porque vamos somar decimais a eles)
        x = float(self.x1)
        y = float(self.y1)
        
        # 5. Loop de rasterização: damos um passo de cada vez até o destino
        for i in range(passos + 1):
            # Arredonda a posição atual para o pixel inteiro mais próximo e pinta
            tela.set_at((round(x), round(y)), PRETO)
            
            # Prepara a posição para o próximo pixel da iteração seguinte
            x += x_inc
            y += y_inc

    def reta_bresenham(self, tela):
        print("Traçando reta usando Bresenham")
        # Pegamos os valores do objeto (self)
        x, y = self.x1, self.y1
        x2, y2 = self.x2, self.y2
        
        # 1. Distâncias absolutas (o tamanho total do deslocamento)
        dx = abs(x2 - x)
        dy = abs(y2 - y)
        
        # 2. Descobre a direção do passo (para frente ou para trás)
        passo_x = 1 if x < x2 else -1
        passo_y = 1 if y < y2 else -1
        
        # 3. O erro unificado inicial
        erro = dx - dy
        
        # Loop de rasterização
        while True:
            # Pinta o pixel na posição atual
            tela.set_at((x, y), PRETO)
            
            # Condição de parada: se desenhamos o último pixel, encerra o loop
            if x == x2 and y == y2:
                break
                
            # Dobramos o erro atual para facilitar a comparação sem usar decimais
            e2 = 2 * erro
            
            # 4. Decisão de movimento no eixo X
            if e2 > -dy:
                erro -= dy
                x += passo_x
                
            # 5. Decisão de movimento no eixo Y
            if e2 < dx:
                erro += dx
                y += passo_y

class Circunferencia:
    def __init__(self, x, y, raio):
        self.x = x
        self.y = y
        self.raio = raio

    def circ_Bresenham(self, tela):
        # 1. Iniciamos no "topo" do círculo (imaginando o centro em 0,0)
        x = 0
        y = self.raio
        
        # 2. A variável de decisão inicial do Bresenham para círculos
        d = 3 - (2 * self.raio)
        
        # 3. O laço roda apenas enquanto X for menor ou igual a Y (Isso equivale a 45 graus)
        while x <= y:
            
            # 4. A Mágica da Simetria de 8 vias! 
            # Somamos self.x e self.y para transladar o cálculo para o centro real do objeto
            tela.set_at((self.x + x, self.y + y), (0, 0, 0)) # Octante 1
            tela.set_at((self.x - x, self.y + y), (0, 0, 0)) # Octante 2
            tela.set_at((self.x + x, self.y - y), (0, 0, 0)) # Octante 8
            tela.set_at((self.x - x, self.y - y), (0, 0, 0)) # Octante 7
            tela.set_at((self.x + y, self.y + x), (0, 0, 0)) # Octante 3
            tela.set_at((self.x - y, self.y + x), (0, 0, 0)) # Octante 4
            tela.set_at((self.x + y, self.y - x), (0, 0, 0)) # Octante 6
            tela.set_at((self.x - y, self.y - x), (0, 0, 0)) # Octante 5
            
            # 5. Atualiza a variável de decisão
            if d < 0:
                # O ponto ideal ainda está na mesma linha, andamos só no X
                d = d + (4 * x) + 6
            else:
                # O ponto ideal invadiu o pixel de baixo, andamos no X e no Y
                d = d + 4 * (x - y) + 10
                y -= 1
                
            x += 1
