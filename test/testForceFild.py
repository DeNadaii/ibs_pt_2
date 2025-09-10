import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configurações iniciais
NUM_PARTICULAS = 20
LIMITE = 10  # Limites do espaço (toroidal)
K = 1.0
PASSO_MIN, PASSO_MAX = 0.1, 0.5

# Inicialização das partículas
class Particula:
    def __init__(self):
        self.x = np.random.uniform(-LIMITE, LIMITE)
        self.y = np.random.uniform(-LIMITE, LIMITE)
        self.carga = np.random.choice([-1, 1])
    
    def move(self, forca_x, forca_y):
        theta = np.random.uniform(0, 2 * np.pi)
        r = np.random.uniform(PASSO_MIN, PASSO_MAX)
        desloc_x = r * np.cos(theta) + forca_x
        desloc_y = r * np.sin(theta) + forca_y
        self.x = (self.x + desloc_x + LIMITE) % (2 * LIMITE) - LIMITE
        self.y = (self.y + desloc_y + LIMITE) % (2 * LIMITE) - LIMITE

particulas = [Particula() for _ in range(NUM_PARTICULAS)]

# Cálculo da menor distância considerando malha infinita (toróide)
def menor_distancia(dx):
    if dx > LIMITE:
        dx -= 2 * LIMITE
    elif dx < -LIMITE:
        dx += 2 * LIMITE
    return dx

# Campo de força com malha infinita
def calcular_forca(p1, p2):
    dx = menor_distancia(p2.x - p1.x)
    dy = menor_distancia(p2.y - p1.y)
    dist_sq = dx**2 + dy**2 + 0.1
    forca = K * p1.carga * p2.carga / dist_sq
    return forca * dx / np.sqrt(dist_sq), forca * dy / np.sqrt(dist_sq)

# Setup da figura
fig, ax = plt.subplots()
sc = ax.scatter([], [], s=50)
ax.set_xlim(-LIMITE, LIMITE)
ax.set_ylim(-LIMITE, LIMITE)
ax.set_title("Malha Infinita com Cargas")

# Função de atualização da animação
def update(frame):
    xs, ys, cs = [], [], []
    for i, p in enumerate(particulas):
        fx, fy = 0, 0
        for j, outro in enumerate(particulas):
            if i != j:
                dfx, dfy = calcular_forca(p, outro)
                fx += dfx
                fy += dfy
        p.move(fx, fy)
        xs.append(p.x)
        ys.append(p.y)
        cs.append('red' if p.carga > 0 else 'blue')
    sc.set_offsets(np.c_[xs, ys])
    sc.set_color(cs)
    return sc,

# Criar e salvar a animação
ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=True)
ani.save("particulas_toroidal.gif", writer='pillow', fps=10)

plt.show()
