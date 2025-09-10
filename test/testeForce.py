import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ================================
# Parâmetros
# ================================

SPACE_SIZE = 100.0
K_COULOMB = 100.0    # Constante da força Coulombiana
DT = 0.05
STEPS = 500
N_PARTICLES = 60

np.random.seed(0)

# ================================
# Inicializar partículas
# ================================

# Metade azul, metade vermelha
positions = np.random.uniform(0, SPACE_SIZE, (N_PARTICLES, 2))
velocities = np.random.uniform(-1, 1, (N_PARTICLES, 2))
types = np.array(['blue'] * (N_PARTICLES//2) + ['red'] * (N_PARTICLES//2))

# Partícula fixa (preta) no meio
fixed_position = np.array([SPACE_SIZE/2, SPACE_SIZE/2])

# ================================
# Simulação
# ================================

history_positions = []
history_types = []

def compute_forces():
    forces = np.zeros_like(positions)

    # Interação entre partículas móveis
    for i in range(N_PARTICLES):
        for j in range(i+1, N_PARTICLES):
            r_vec = positions[j] - positions[i]
            r2 = np.sum(r_vec**2)
            if r2 < 1e-5:
                continue
            r = np.sqrt(r2)
            force_mag = K_COULOMB / r2

            if types[i] == types[j]:
                # Mesmo tipo: repulsão
                force_vec = force_mag * (r_vec / r)
            else:
                # Tipos diferentes: atração
                force_vec = -force_mag * (r_vec / r)

            forces[i] += force_vec
            forces[j] -= force_vec  # Ação e reação

    # Interação com a partícula preta (atração para o centro)
    for i in range(N_PARTICLES):
        r_vec = fixed_position - positions[i]
        r2 = np.sum(r_vec**2)
        if r2 < 1e-5:
            continue
        r = np.sqrt(r2)
        force_mag = K_COULOMB / r2
        force_vec = force_mag * (r_vec / r)

        forces[i] += force_vec

    return forces

for step in range(STEPS):
    forces = compute_forces()

    velocities += forces * DT
    positions += velocities * DT

    # Condição de contorno periódica
    positions = np.mod(positions, SPACE_SIZE)

    history_positions.append(positions.copy())
    history_types.append(types.copy())

history_positions = np.array(history_positions)

print("Simulação finalizada!")

# ================================
# Animação
# ================================

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, SPACE_SIZE)
ax.set_ylim(0, SPACE_SIZE)
ax.set_aspect('equal')
blue_scat = ax.plot([], [], 'bo')[0]
red_scat = ax.plot([], [], 'ro')[0]
fixed = ax.plot(fixed_position[0], fixed_position[1], 'ko', markersize=10)[0]

def init():
    blue_scat.set_data([], [])
    red_scat.set_data([], [])
    return blue_scat, red_scat, fixed

def update(frame):
    pos = history_positions[frame]
    blue_pos = pos[types == 'blue']
    red_pos = pos[types == 'red']

    blue_scat.set_data(blue_pos[:, 0], blue_pos[:, 1])
    red_scat.set_data(red_pos[:, 0], red_pos[:, 1])

    return blue_scat, red_scat, fixed

ani = animation.FuncAnimation(fig, update, frames=len(history_positions),
                               init_func=init, blit=True, interval=30)

plt.show()
