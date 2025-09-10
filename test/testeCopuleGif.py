import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Classe das partículas
class Particula:
    def __init__(self, x, y, tipo, fixa=False):
        self.x = x
        self.y = y
        self.tipo = tipo  # 'a', 'b' ou 'c'
        self.fixa = fixa

    def mover(self, min_wind_force, max_wind_force):
        if self.fixa:
            return
        rlan = np.random.uniform(min_wind_force, max_wind_force)
        theta = np.random.uniform(0, 2 * np.pi)
        dx = rlan * np.cos(theta)
        dy = rlan * np.sin(theta)
        self.x += dx
        self.y += dy

    def distancia_para(self, outra):
        return math.hypot(self.x - outra.x, self.y - outra.y)

# Geração inicial das partículas
def gerar_particulas_iniciais(n_a=5, n_b=5, n_c=10):
    particulas = []
    for i in range(n_a):
        particulas.append(Particula(random.uniform(-10, 10), random.uniform(-10, 10), 'a'))
    for i in range(n_b):
        particulas.append(Particula(random.uniform(-10, 10), random.uniform(-10, 10), 'b'))
    for i in range(n_c):
        particulas.append(Particula(random.uniform(-10, 10), random.uniform(-10, 10), 'c', fixa=True))
    return particulas

# Verifica se uma nova partícula deve surgir
def verificar_reacoes(particulas, raio=3):
    novas_particulas = []
    particulas_c = [p for p in particulas if p.tipo == 'c']
    for p_c in particulas_c:
        proximas_a = []
        proximas_b = []
        for p in particulas:
            if p == p_c:
                continue
            if p.distancia_para(p_c) <= raio:
                if p.tipo == 'a':
                    proximas_a.append(p)
                elif p.tipo == 'b':
                    proximas_b.append(p)
        if proximas_a and proximas_b:
            novo_tipo = random.choice(['a', 'b'])
            angulo = random.uniform(0, 2 * math.pi)
            r = random.uniform(0, raio)
            x_novo = p_c.x + r * math.cos(angulo)
            y_novo = p_c.y + r * math.sin(angulo)
            novas_particulas.append(Particula(x_novo, y_novo, novo_tipo))
    return novas_particulas

# Parâmetros da simulação
min_wind_force = 0.1
max_wind_force = 0.5
raio_interacao = 3
particulas = gerar_particulas_iniciais()
cores = {'a': 'blue', 'b': 'red', 'c': 'green'}

# Setup do gráfico
fig, ax = plt.subplots()
sc = ax.scatter([], [], c=[], s=50)
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_title("Simulação com deslocamento polar")
ax.grid(True)

# Função de atualização da animação
def update(frame):
    global particulas
    for p in particulas:
        p.mover(min_wind_force, max_wind_force)
    novas = verificar_reacoes(particulas, raio=raio_interacao)
    particulas.extend(novas)
    xs = [p.x for p in particulas]
    ys = [p.y for p in particulas]
    cs = [cores[p.tipo] for p in particulas]
    sc.set_offsets(np.c_[xs, ys])
    sc.set_color(cs)
    return sc,

# Animação
ani = FuncAnimation(fig, update, frames=100, interval=200, blit=True)

# Salva como GIF
ani.save("simulacao_particulas.gif", writer='pillow', fps=5)

# Exibe o gráfico (opcional, pode comentar se for rodar apenas no terminal/headless)
plt.show()
