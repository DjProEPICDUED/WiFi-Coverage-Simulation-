import numpy as np
import matplotlib.pyplot as plt

def calc_p0(bandChoice, tx, gain):
    freq = bandChoice * 1e9
    p0 = tx + gain - (20 * np.log10(freq) - 147.55)
    return p0

def simuSignal(grid, router, p0, n):
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - router[0])**2 + (j - router[1])**2)
            if d < 1:
                d = 1
            
            grid[i, j] = p0 - 10 * n * np.log10(d)
    return grid

def plotHeatmap(grid, router, wallGrid=None):
    plt.figure(figsize=(8, 8))

    plt.imshow(grid, origin="lower", cmap="inferno", alpha=0.85)

    if wallGrid is not None:
        wall_overlay = np.ma.masked_where(wallGrid == 0, wallGrid)
        plt.imshow(wall_overlay, cmap="gray", origin="lower", alpha=0.4)

    plt.scatter(router[1], router[0], c='cyan', s=120, edgecolors='black', label="Router")

    plt.colorbar(label="Signal Strength (dBm)")
    plt.title("Wi-Fi Signal Strength Heatmap")
    plt.xlabel("X position (meters)")
    plt.ylabel("Y position (meters)")
    plt.legend(loc="upper right")
    plt.show()