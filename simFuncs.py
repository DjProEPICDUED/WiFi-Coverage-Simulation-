import numpy as np
import matplotlib.pyplot as plt

# Attenuation per wall type (dB)
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


def get_wall_loss_along_ray(router, cell, wallGrid):
    """
    Computes TOTAL attenuation (dB) along the straight line
    from router → cell.
    Properly counts unique wall cells and applies correct material attenuation.
    """
    r0, c0 = router
    r1, c1 = cell

    samples = 300  # smooth ray tracing
    visited = set()
    total_loss = 0

    for t in np.linspace(0, 1, samples):
        r = int(r0 + (r1 - r0) * t)
        c = int(c0 + (c1 - c0) * t)

        # If out of bounds, skip
        if r < 0 or c < 0 or r >= wallGrid.shape[0] or c >= wallGrid.shape[1]:
            continue

        if (r, c) not in visited:
            visited.add((r, c))
            wall_type = int(wallGrid[r, c])
            total_loss += WALL_ATTENUATION[wall_type]

    return total_loss


def simuSignal(grid, router, p0, nEmpty, wallGrid=None):
    """
    Simulates Wi-Fi signal strength across the grid.
    Includes:
        - free space path loss
        - attenuation through walls (ray marching)
    """
    rows, cols = grid.shape
    newGrid = np.zeros_like(grid)

    for r in range(rows):
        for c in range(cols):

            d = np.sqrt((r - router[0])**2 + (c - router[1])**2)

            if d == 0:
                newGrid[r, c] = p0
                continue

            # Free space loss
            Pr = p0 - 10 * nEmpty * np.log10(d)

            # Add wall attenuation
            if wallGrid is not None:
                wall_loss = get_wall_loss_along_ray(router, (r, c), wallGrid)
                Pr -= wall_loss

            newGrid[r, c] = Pr

    return newGrid


def plotHeatmap(grid, router, wallGrid=None):
    """
    Draws heatmap with walls underneath.
    """
    plt.figure(figsize=(8, 8))

    # Dynamic color scaling
    im = plt.imshow(grid, origin="lower",
                    cmap="inferno", alpha=0.85,
                    vmin=np.max(grid),
                    vmax=np.min(grid))

    # Overlay walls
    if wallGrid is not None:
        wall_overlay = np.ma.masked_where(wallGrid == 0, wallGrid)
        plt.imshow(wall_overlay, cmap="gray", origin="lower", alpha=0.35)

    # Router marker
    plt.scatter(router[1], router[0],
                c='cyan', s=150, edgecolors='black', label="Router")

    plt.colorbar(im, label="Signal Strength (dBm)")
    plt.title("Wi-Fi Signal Strength Heatmap")
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.legend(loc="upper right")
    plt.show()
