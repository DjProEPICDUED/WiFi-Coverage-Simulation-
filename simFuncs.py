import numpy as np
import matplotlib.pyplot as plt

WALL_ATTENUATION = {
    0: 0,      # empty
    1: 5,      # drywall
    2: 12,     # brick
    3: 20      # concrete
}

def calc_p0(bandChoice, tx, gain):
    freq = bandChoice * 1e9
    p0 = tx + gain - (20 * np.log10(freq) - 147.55)
    return p0

def get_wall_loss_along_ray(router, cell, wallGrid, wallType):

    r0, c0 = router
    r1, c1 = cell

    samples = 300
    visited = set()
    total_loss = 0

    for t in np.linspace(0, 1, samples):
        r = int(r0 + (r1 - r0) * t)
        c = int(c0 + (c1 - c0) * t)

        if r < 0 or c < 0 or r >= wallGrid.shape[0] or c >= wallGrid.shape[1]:
            continue

        if (r, c) not in visited:
            visited.add((r, c))
            if wallGrid[r, c] != 0:
                total_loss += wallType

    return total_loss

def simuSignal(routers, p0, nEmpty, wallGrid, wallType):
    GRID_SIZE = wallGrid.shape[0]
    full_grid = np.full((GRID_SIZE, GRID_SIZE), -9999.0)

    for router in routers:

        temp_grid = np.zeros((GRID_SIZE, GRID_SIZE))

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):

                d = np.sqrt((r - router[0])**2 + (c - router[1])**2)

                if d == 0:
                    Pr = p0
                else:
                    wall_loss = get_wall_loss_along_ray(router, (r, c), wallGrid, wallType)
                    Pr = p0 - 10 * nEmpty * np.log10(d) - wall_loss

                temp_grid[r, c] = Pr

        full_grid = np.maximum(full_grid, temp_grid)

    return full_grid
