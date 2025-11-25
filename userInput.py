import numpy as np
import matplotlib.pyplot as plt

GRID_SIZE = 50

wall_grid = np.zeros((GRID_SIZE, GRID_SIZE))
router_pos = [25, 25]   

def draw_editor():
    plt.clf()
    plt.imshow(wall_grid, cmap="binary", origin="lower")  # walls = black squares
    plt.scatter(router_pos[1], router_pos[0], c='red', s=120)  # router = red dot
    plt.title("Click to Edit Floor Plan\nLeft=Add Wall, Right=Remove Wall, Middle=Router, ENTER=Finish")
    plt.draw()

def onclick(event):
    global router_pos, wall_grid
    
    # check bounds
    if event.xdata is None or event.ydata is None:
        return
    
    col = int(event.xdata)
    row = int(event.ydata)

    if event.button == 1:       # left-click = add wall
        wall_grid[row, col] = 1

    elif event.button == 3:     # right-click = remove wall
        wall_grid[row, col] = 0

    elif event.button == 2:     # middle-click = place router
        router_pos = [row, col]

    draw_editor()


def on_key(event):
    if event.key == 'enter':
        plt.close()    # user is done editing


def start_editor():
    fig = plt.figure(figsize=(7,7))
    draw_editor()

    cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
    cid_key   = fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()

    return wall_grid, tuple(router_pos)