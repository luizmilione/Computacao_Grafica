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

class Recorte:
    # Constantes em binário para facilitar a leitura (Bitmask)
    DENTRO = 0   # 0000
    ESQUERDA = 1 # 0001
    DIREITA = 2  # 0010
    BAIXO = 4    # 0100
    CIMA = 8     # 1000

    def __init__(self, x_min, y_min, x_max, y_max):
        # Ajeitei os nomes para combinar com a lógica min/max tradicional
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def obter_codigo(self, x, y):
        """Calcula o código de região de 4 bits para um ponto X, Y"""
        codigo = self.DENTRO
        
        if x < self.x_min:      # À esquerda
            codigo |= self.ESQUERDA
        elif x > self.x_max:    # À direita
            codigo |= self.DIREITA
            
        if y < self.y_min:      # Acima (Pygame Y invertido)
            codigo |= self.CIMA
        elif y > self.y_max:    # Abaixo
            codigo |= self.BAIXO
            
        return codigo

    def processar_reta(self, x1, y1, x2, y2):
        """Executa o algoritmo para uma única reta e retorna as novas coordenadas (ou None)"""
        codigo1 = self.obter_codigo(x1, y1)
        codigo2 = self.obter_codigo(x2, y2)
        aceita = False

        while True:
            # 1. Aceitação Trivial: Ambos estão DENTRO (0000 | 0000 == 0)
            if codigo1 == 0 and codigo2 == 0:
                aceita = True
                break
                
            # 2. Rejeição Trivial: Ambos estão fora na mesma zona (AND bit a bit != 0)
            elif (codigo1 & codigo2) != 0:
                break
                
            # 3. Recorte Necessário: Pelo menos um ponto está fora, vamos encontrar a interseção
            else:
                # Escolhe o ponto que está fora (se código1 for 0, pega o código2)
                codigo_fora = codigo1 if codigo1 != 0 else codigo2
                x, y = 0.0, 0.0

                # Encontra o ponto de interseção usando a fórmula: y = y1 + slope * (x - x1)
                # ou x = x1 + (1 / slope) * (y - y1)
                
                if codigo_fora & self.CIMA:
                    # Ponto está acima da janela
                    x = x1 + (x2 - x1) * (self.y_min - y1) / (y2 - y1)
                    y = self.y_min
                elif codigo_fora & self.BAIXO:
                    # Ponto está abaixo da janela
                    x = x1 + (x2 - x1) * (self.y_max - y1) / (y2 - y1)
                    y = self.y_max
                elif codigo_fora & self.DIREITA:
                    # Ponto está à direita
                    y = y1 + (y2 - y1) * (self.x_max - x1) / (x2 - x1)
                    x = self.x_max
                elif codigo_fora & self.ESQUERDA:
                    # Ponto está à esquerda
                    y = y1 + (y2 - y1) * (self.x_min - x1) / (x2 - x1)
                    x = self.x_min

                # Substitui o ponto que estava fora pela interseção encontrada
                if codigo_fora == codigo1:
                    x1, y1 = x, y
                    codigo1 = self.obter_codigo(x1, y1)
                else:
                    x2, y2 = x, y
                    codigo2 = self.obter_codigo(x2, y2)

        if aceita:
            return (round(x1), round(y1), round(x2), round(y2))
        else:
            return None # A reta foi totalmente rejeitada e não deve ser desenhada
    
    def aplicar_recorte_na_tela(self, tela, array_estruturas):
        array_temporarias = []
        # Varre todos os objetos
        for objeto in array_estruturas:
            
            # Checa se o objeto é da classe Reta (algoritmo é exclusivo para retas)
            if isinstance(objeto, Reta):
                
                # Tenta recortar usando as coordenadas originais do objeto
                resultado = self.processar_reta(objeto.x1, objeto.y1, objeto.x2, objeto.y2)
                
                # Se o algoritmo retornou coordenadas (Aceitou ou Recortou)
                if resultado is not None:
                    # Atualiza os valores da reta temporariamente
                    nx1, ny1, nx2, ny2 = resultado
                    
                    # Desenha a linha recortada (assumindo que você tem acesso às funções de desenho aqui)
                    # Você pode criar um método temporário ou instanciar uma Reta nova aqui só para desenhar
                    ini = (nx1, ny1)
                    fi = nx2, ny2
                    reta_recortada = Reta(ini, fi)
                    reta_recortada.reta_bresenham(tela)
                    array_temporarias.append(reta_recortada)

