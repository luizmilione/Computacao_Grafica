class Reta:
    def __init__(self, t1, t2):
        # Extrai as coordenadas X e Y das tuplas
        self.x1, self.y1 = t1
        self.x2, self.y2 = t2

    def reta_dda(self, tela):
        PRETO = (0, 0, 0)
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
        x = float(x1)
        y = float(y1)
        
        # 5. Loop de rasterização: damos um passo de cada vez até o destino
        for i in range(passos + 1):
            # Arredonda a posição atual para o pixel inteiro mais próximo e pinta
            tela.set_at((round(x), round(y)), PRETO)
            
            # Prepara a posição para o próximo pixel da iteração seguinte
            x += x_inc
            y += y_inc