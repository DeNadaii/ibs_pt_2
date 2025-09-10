class Predador:
    def __init__(self, genero, idade, coordenada, on_prey):
        self.genero = genero
        self.idade = idade
        self.coordenada = coordenada
        self.procriar = False
        self.morte = False
        self.move = True
        self.is_copulating = False 
        self.on_prey = on_prey
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
    def can_move(self):
        if self.idade < 5 and self.on_prey:
            self.move = False
    def copulating(self):
        if self.procriar and self.on_prey:
            self.move = False
            self.is_copulating = True
            self.days_of_copule += 1
    def test():
        print("print test")
                
        
    
        