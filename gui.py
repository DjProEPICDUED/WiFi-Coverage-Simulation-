import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

GRID_SIZE = 50
wall_grid = np.zeros((GRID_SIZE, GRID_SIZE))
routers = [[25, 25]]
placing_router = False

# Global variables to hold the specific plot axis and button references
ax_main = None
btn_add = None
btn_remove = None

def draw_editor():
    global ax_main
    
    # CLEAR ONLY THE MAIN AXIS, NOT THE WHOLE FIGURE
    ax_main.clear()
    
    # Use the specific axis (ax_main) to draw, not plt
    ax_main.imshow(wall_grid, cmap="binary", origin="lower")

    # draw all routers
    for r in routers:
        ax_main.scatter(r[1], r[0], c='red', s=120)

    ax_main.set_title("Left=Add Wall | Right=Remove Wall | Middle=Move Router\nENTER=Finish")
    plt.draw()

def onclick(event):
    global wall_grid, routers, placing_router

    # Ignore clicks that happen outside the main plot area (like on buttons)
    if event.inaxes != ax_main:
        return

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
    global ax_main, btn_add, btn_remove 

    fig = plt.figure(figsize=(7, 7))
    
    # Adjust layout to make room at the bottom for buttons
    plt.subplots_adjust(bottom=0.2)

    # Create the main axis for the map
    ax_main = fig.add_subplot(111)

    # Draw the initial state
    draw_editor()

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Position buttons in the empty space at the bottom
    ax_add = plt.axes([0.15, 0.05, 0.3, 0.075])
    ax_remove = plt.axes([0.55, 0.05, 0.3, 0.075])

    # Assign to global variables to prevent garbage collection
    btn_add = Button(ax_add, "Add Router")
    btn_remove = Button(ax_remove, "Remove Router")

    btn_add.on_clicked(add_router_button)
    btn_remove.on_clicked(remove_router_button)

    plt.show()

    return wall_grid, routers

if __name__ == '__main__':
    start_editor()