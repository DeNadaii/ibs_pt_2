class Predador:
    def __init__(self, genero, idade, coordenada, can_move):
        self.genero = genero
        self.idade = idade
        self.coordenada = coordenada
        self.procriar = False
        self.morte = False
        self.can_move = can_move
        self.is_copulating = False 
        self.days_of_copule = 0
    def crescimento_predador(self):
        if self.idade <= 20:
            self.idade += 1
    def apto_a_procriar(self):
        if 10 <= self.idade <= 12:
            self.procriar = True
    def idade_de_morte(self):
        if self.idade > 20:
            self.morte = True
    def test():
        print("print test")
                
        
    
        