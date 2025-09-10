import numpy as np
import matplotlib.pyplot as plt
import os as OS
import random
import platform
import matplotlib.animation as animation
from classPredador import Predador 
from classPrey import Prey
import json

from pathlib import Path
import json

# Pega a pasta do script atual
base_dir = Path(__file__).resolve().parent
config_path = base_dir / "config.json"

with open(config_path, "r") as f:
    parametros = json.load(f)

#variaveis
Dimensions = parametros["Dimencoes"]

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
        predadores.append(Predador(random.choice(gender),IdadePredador,[x,y],True))

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
        if individual.can_move == True:
            wsx, wsy = wind_shift
            dx, dy = decide_direction(mov_max,mov_min)
            individual.coordenada = [individual.coordenada[0] + dx + wsx, individual.coordenada[1] + dy + wsy]

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
                if np.sqrt((preys[i].coordenates[0] - predador[j].coordenada[0])**2 + (preys[i].coordenates[1] - predador[j].coordenada[1])**2) <= rp:
                    predador[j].on_prey = True

# Função para checar colisao entre predadores
def check_colision_Predador(predador,rp): #rp define a distancia de aproximação para o acasalamento
    for i in range(len(predador)):
        for j in range(i + 1, len(predador)): 
            if predador[j].can_move and predador[i].can_move:
                if np.sqrt((predador[i].coordenada[0] - predador[j].coordenada[0])**2 + (predador[i].coordenada[1] - predador[j].coordenada[1])**2) <= rp:
                    print(predador[j].coordenada)
                    #generate_Spawn(predador[j].coordenada)
        

#set the number of individuals
generate_Predador(10)
generate_prey(5)

count = 0
while count < 50:
    # Plotagem do resultado
    move_individual(predadores,add_Wind_Shift(1.0,1.5),0.5,2.0)
    check_colision_Predador(predadores,0.5)
    #death_control(predadores)
    check_colision_prey(predadores, preys, 1.0)
    for i in predadores:
        #print(i.idade)
        i.crescimento_predador()
        # i.apto_a_procriar()
        # i.idade_de_morte()
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
    

'''# Função de atualização da animação
def update(frame):
    plt.clf()
    
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
    
    # Mover indivíduos
    for p in predadores:
        p.move()

    # Plotar os pontos atualizados
    plt.scatter([p.coordenada[0] for p in predadores], [p.coordenada[1] for p in predadores], s=50, c='b', label="Predadores")
    plt.scatter([p.coordenada[0] for p in preys], [p.coordenada[1] for p in preys], s=100, c='r', label="Presas")
    
    plt.xlim(-Dimensions, Dimensions)
    plt.ylim(-Dimensions, Dimensions)
    plt.legend()
    plt.title(f"Passo {frame}")

# Criando a animação
fig = plt.figure(figsize=(8, 8))
ani = animation.FuncAnimation(fig, update, frames=50, interval=200)
plt.show()'''

    

    
if platform.system() == "Windows":
    OS.system("magick convert *.png ibs.gif && del /Q *.png")
else:
    OS.system("convert *.png ibs.gif && rm -rf *.png")
