import numpy as np
import matplotlib.pyplot as plt

WALL_ATTENUATION = {
    0: 0,      # empty
    1: 5,      # drywall
    2: 12,     # brick
    3: 20      # concrete
}

def calc_p0(bandChoice, tx, gain):
    """
    Compute reference received power P0 at 1 meter.
    """
    freq = bandChoice * 1e9
    p0 = tx + gain - (20 * np.log10(freq) - 147.55)
    return p0

def count_walls_between(router, cell, wallGrid):
    r0, c0 = router
    r1, c1 = cell

    # Bresenham’s Line Algorithm
    walls = 0
    dr = abs(r1 - r0)
    dc = abs(c1 - c0)
    sr = 1 if r0 < r1 else -1
    sc = 1 if c0 < c1 else -1
    err = dr - dc

    r, c = r0, c0

    while True:
        # Skip the starting cell (router)
        if not (r == r0 and c == c0):
            if wallGrid[r, c] != 0:
                walls += 1

        if r == r1 and c == c1:
            break

        e2 = 2 * err
        if e2 > -dc:
            err -= dc
            r += sr
        if e2 < dr:
            err += dr
            c += sc

    return walls

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

def simuSignal(router, p0, nEmpty, wallGrid, wallType):
    grid = np.zeros((50, 50))

    for r in range(50):
        for c in range(50):

            d = np.sqrt((r - router[0])**2 + (c - router[1])**2)

            if d == 0:
                grid[r, c] = p0

            wall_loss = get_wall_loss_along_ray(router, (r, c), wallGrid, wallType)
            Pr = p0 - 10 * nEmpty * np.log10(d) - wall_loss

            grid[r, c] = Pr

    return grid