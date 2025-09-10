import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# ==== PARÂMETROS GERAIS ====
num_A = 10
num_B = 10
num_C = 4
raio_influencia = 1.5
limite_espaco = 25
total_frames = 100

# Parâmetros de deslocamento polar aleatório
min_valor = 0.2
max_valor = 1.0

# ==== CLASSE PARTICULA ====
class Particula:
    def __init__(self, tipo, pos=None):
        self.tipo = tipo
        if pos is None:
            self.pos = np.random.rand(2) * limite_espaco
        else:
            self.pos = np.array(pos)
    
    def mover(self):
        if self.tipo in ['A', 'B']:
            rlan = np.random.uniform(min_valor, max_valor)
            theta = np.random.uniform(0, 2 * np.pi)
            dx = rlan * np.cos(theta)
            dy = rlan * np.sin(theta)
            self.pos += np.array([dx, dy])
            self.pos = np.clip(self.pos, 0, limite_espaco)

# ==== INICIALIZAÇÃO DAS PARTÍCULAS ====
def criar_particulas(n, tipo):
    return [Particula(tipo) for _ in range(n)]

particulas_A = criar_particulas(num_A, 'A')
particulas_B = criar_particulas(num_B, 'B')
particulas_C = criar_particulas(num_C, 'C')

todas_particulas = particulas_A + particulas_B + particulas_C

# ==== VERIFICAÇÃO DE INFLUÊNCIA E CRIAÇÃO ====
def verificar_influencia(particulas):
    novas = []
    particulas_C = [p for p in particulas if p.tipo == 'C']
    particulas_AB = [p for p in particulas if p.tipo in ['A', 'B']]
    
    for c in particulas_C:
        A_dentro = []
        B_dentro = []
        for p in particulas_AB:
            dist = np.linalg.norm(p.pos - c.pos)
            if dist <= raio_influencia:
                if p.tipo == 'A':
                    A_dentro.append(p)
                else:
                    B_dentro.append(p)
        if A_dentro and B_dentro:
            novo_tipo = random.choice(['A', 'B'])
            angulo = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0, raio_influencia)
            deslocamento = r * np.array([np.cos(angulo), np.sin(angulo)])
            nova_pos = c.pos + deslocamento
            nova_pos = np.clip(nova_pos, 0, limite_espaco)
            novas.append(Particula(novo_tipo, nova_pos))
    
    return novas

# ==== PLOTAGEM ====
fig, ax = plt.subplots()
sc_A = ax.scatter([], [], color='blue', label='A')
sc_B = ax.scatter([], [], color='green', label='B')
sc_C = ax.scatter([], [], color='red', label='C')

# Círculos de influência
circulos = []
for c in particulas_C:
    circulo = plt.Circle(c.pos, raio_influencia, color='r', fill=False, linestyle='--')
    ax.add_patch(circulo)
    circulos.append(circulo)

ax.set_xlim(0, limite_espaco)
ax.set_ylim(0, limite_espaco)
ax.set_title('Simulação de Partículas com Classe e Movimento Polar')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_aspect('equal')
ax.grid(True)

# ==== ATUALIZAÇÃO POR FRAME ====
def atualizar(frame):
    global todas_particulas

    for p in todas_particulas:
        p.mover()

    novas = verificar_influencia(todas_particulas)
    todas_particulas.extend(novas)

    pos_A = np.array([p.pos for p in todas_particulas if p.tipo == 'A'])
    pos_B = np.array([p.pos for p in todas_particulas if p.tipo == 'B'])
    pos_C = np.array([p.pos for p in todas_particulas if p.tipo == 'C'])

    sc_A.set_offsets(pos_A)
    sc_B.set_offsets(pos_B)
    sc_C.set_offsets(pos_C)

    return sc_A, sc_B, sc_C

# ==== EXECUTA A ANIMAÇÃO ====
anim = FuncAnimation(fig, atualizar, frames=total_frames, interval=200, blit=False)
plt.show()
