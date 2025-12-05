import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

GRID_SIZE = 50
wall_grid = np.zeros((GRID_SIZE, GRID_SIZE))
routers = [[25, 25]]
placing_router = False


def draw_editor():
    plt.clf()
    plt.imshow(wall_grid, cmap="binary", origin="lower")

    # draw all routers
    for r in routers:
        plt.scatter(r[1], r[0], c='red', s=120)

    plt.title("Left=Add Wall | Right=Remove Wall | Middle=Move Router\nENTER=Finish")
    plt.draw()

def onclick(event):
    global wall_grid, routers, placing_router

    if event.xdata is None or event.ydata is None:
        return

    col = int(event.xdata)
    row = int(event.ydata)

    # --- placing a new router ---
    if placing_router:
        routers.append([row, col])
        placing_router = False
        draw_editor()
        return

    # ----- Regular Editor Behavior -----

    if event.button == 1:
        wall_grid[row, col] = 1

    elif event.button == 3:
        wall_grid[row, col] = 0

    elif event.button == 2:  # move closest router
        # move only the nearest router
        dists = [np.hypot(r[0]-row, r[1]-col) for r in routers]
        idx = np.argmin(dists)
        routers[idx] = [row, col]

    draw_editor()

def on_key(event):
    if event.key == 'enter':
        plt.close()

def add_router_button(event):
    global placing_router
    placing_router = True
    print("Click anywhere to place a new router...")

def remove_router_button(event):
    if len(routers) > 1:
        routers.pop()
    print("Removed last router")
    draw_editor()

def start_editor():
    fig = plt.figure(figsize=(7, 7))
    draw_editor()

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('key_press_event', on_key)

    ax_add = plt.axes([0.1, 0.01, 0.25, 0.05])
    ax_remove = plt.axes([0.65, 0.01, 0.25, 0.05])

    btn_add = Button(ax_add, "Add Router")
    btn_remove = Button(ax_remove, "Remove Router")

    btn_add.on_clicked(add_router_button)
    btn_remove.on_clicked(remove_router_button)

    plt.show()

    return wall_grid, routers


if __name__ == '__main__':
    start_editor()