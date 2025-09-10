import numpy as np
import matplotlib.pyplot as plt
import os as OS
import random
import platform
from classPredador import Predador 
from classPrey import Prey

#variaveis
Dimensions = 5.0

# Inicialização
preys = []
predadores = []


# Criando prey
def generate_prey(numberOfIndividuals):
    for i in range(numberOfIndividuals):
        x = np.random.uniform(-Dimensions,Dimensions)
        y = np.random.uniform(-Dimensions,Dimensions)
        preys.append(Prey([x,y]))

#criando Predador
def generate_Predador(numberOfIndividuals):
    for i in range(numberOfIndividuals):
        IdadePredador = 5
        x = np.random.uniform(-Dimensions,Dimensions)
        y = np.random.uniform(-Dimensions,Dimensions)
        gender = ["M","F"]
        predadores.append(Predador(random.choice(gender),IdadePredador,[x,y],False))

def generate_Spawn(coord):
    numberOfIndividuals = random.randint(0, 5)
    for i in range(numberOfIndividuals):
        IdadePredador = 1
        x = coord[0]
        y = coord[1]
        gender = ["M","F"]
        predadores.append(Predador(random.choice(gender),IdadePredador,[x,y], True))

def add_Wind_Shift(max_wind_force,min_wind_force):
    rlan = np.random.uniform(max_wind_force, min_wind_force)  #alcançe de movimento do individuo 
    theta = np.random.uniform(0, 2 * np.pi)
    return rlan * np.cos(theta), rlan * np.sin(theta) # Coordenada x e y a partir do centro

# Função decidir direção individuo 
def decide_direction(mov_max,mov_min):
    rlan = np.random.uniform(mov_min, mov_max)  #alcançe de movimento do individuo 
    theta = np.random.uniform(0, 2 * np.pi)
    return rlan * np.cos(theta), rlan * np.sin(theta) # Coordenada x e y a partir do centro

# Função mover individuo 
def move_individual(arrayIndividual,wind_shift,mov_max,mov_min):
    for individual in arrayIndividual:
        if individual.move == True:
            wsx, wsy = wind_shift
            dx, dy = decide_direction(mov_max,mov_min)
            individual.coordenada = [individual.coordenada[0] + dx + wsx, individual.coordenada[1] + dy +wsy]

# Ao percorrer a lista de trás para frente, 
# os índices dos elementos ainda não processados 
# não são afetados pelas remoções, garantindo que 
# todos os elementos sejam verificados.

def death_control(arrPredadores):
    # primeiro parametro define o ultmo index; 
    # o segundo define o limite, vai parar antes do -1; 
    # o terceiro define o passo
    for i in range(len(arrPredadores) - 1, -1, -1):
        #print("morte",arrPredadores[i].morte)
        if arrPredadores[i].morte == True:
            arrPredadores.pop(i)

# # Função para checar colisao
# def check_colision_prey(predador, preys, rp): 
#     for i in predador:
#         for j in preys:
#             if np.sqrt((i.coordenada[0] - j[0])**2 + (i.coordenada[1] - j[1])**2) <= rp:
#                 print("colide")
#     return False  

def check_colision_prey(predador, preys, rp):
        for i in range(len(preys)):
            for j in range(i + 1, len(predador)):
                # print(predador[j].is_copulating)
                if np.sqrt((preys[i].coordenates[0] - predador[j].coordenada[0])**2 + (preys[i].coordenates[1] - predador[j].coordenada[1])**2) <= rp:
                    predador[j].on_prey = True
                    preys[i].predators.append([predador[j]])

# Função para checar colisao entre predadores
def check_colision_Predador(predador,rp): #rp define a distancia de aproximação para o acasalamento
    for i in range(len(predador)):
        for j in range(i + 1, len(predador)): 
            valor_i = predador[i].coordenada
            valor_j = predador[j].coordenada
            sexo_i = predador[i].genero
            sexo_j = predador[j].genero
            idade_i = predador[i].procriar
            idade_j = predador[j].procriar
            can_copulete_i = predador[i].on_prey
            can_copulete_j = predador[j].on_prey
            if sexo_i != sexo_j and idade_j and idade_i and can_copulete_i and can_copulete_j:
                #generate_Spawn(valor_i)
                if sexo_i == "F":
                    generate_Spawn(valor_i)
                    #print(valor_i)
                else:
                    generate_Spawn(valor_j)
                    #print(valor_j)

def copule(preys):
    for i in preys:
        print(i.predators)
        for j in i.predators:
            print("ok")
    

#set the number of individuals
generate_Predador(30)
generate_prey(10)

count = 0
while count < 50:
    # Plotagem do resultado
    move_individual(predadores,add_Wind_Shift(1.0,1.5),0.5,2.0)
    check_colision_Predador(predadores,0.5)
    #death_control(predadores)
    check_colision_prey(predadores, preys, 1.0)
    copule(preys)
    for i in predadores:
        #print(i.idade)
        i.crescimento_predador()
        # i.apto_a_procriar()
        # i.idade_de_morte()
        i.can_move()
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(111)
    ax1.scatter([predador.coordenada[0] for predador in predadores], [predador.coordenada[1] for predador in predadores], s=50, c='b')
    ax1.scatter([prey.coordenates[0] for prey in preys], [prey.coordenates[1] for prey in preys], s=150, c='r')
    plt.xlim(-Dimensions*3, Dimensions*3)  # Define limite fixo para o eixo x
    plt.ylim(-Dimensions*3, Dimensions*3)  # Define limite fixo para o eixo y
    plt.gca().set_aspect('equal', adjustable='box')  # Garante a proporção igual dos eixos
    plt.grid(True)
    plt.title("Frame {}".format(count))
    if count > 9:
        plt.savefig("matrix_IBS_{}.png".format(count), bbox_inches='tight')
    else:
        plt.savefig("matrix_IBS_0{}.png".format(count), bbox_inches='tight')
    count += 1
    

    
if platform.system() == "Windows":
    OS.system("magick convert *.png ibs.gif && del /Q *.png")
else:
    OS.system("convert *.png ibs.gif && rm -rf *.png")
