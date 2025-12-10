import numpy as np
import matplotlib.pyplot as plt

#wall_grid = np.zeros((GRID_SIZE, GRID_SIZE))
WALL_ATTENUATION = {
    0: 0,      # empty
    1: 5,      # drywall
    2: 12,     # brick
    3: 20      # concrete
}
wallTypeList = [["too lazy", 67], ['drywall', 5], ['brick', 12], ['concrete', 20]]
clutter = [["is empty", 1.6], ["has medium clutter", 2.5], ["has heavy clutter", 3.5]]

def user_input():
    routers = [
        {
            "name": "TP-Link AX1800",
            "2.4GHz": {"Pt": 20, "G": 4},
            "5.0GHz": {"Pt": 20, "G": 5}
        },
        {
            "name": "TP-Link Deco X55",
            "2.4GHz": {"Pt": 20, "G": 3},
            "5.0GHz": {"Pt": 20, "G": 4}
        },
        {
            "name": "GL-iNet Opal",
            "2.4GHz": {"Pt": 19.14, "G": 2},
            "5.0GHz": {"Pt": 22.47, "G": 2}
        }
    ]
    routerInfo = ["TP-Link AX1800", "TP-Link Deco X55", "GL-iNet Opal"]

    print("Choose one of the following best selling routers to run the simulation on:")
    print("1) TP-Link AX1800: 20dBm Tx Power, 4dBi Gain (2.4GHz); 20dBm Tx Power, 5dBi Gain (5GHz)")
    print("2) TP-Link Deco X55: 20dBm Tx Power, 3dBi Gain (2.4GHz); 20dBm Tx Power, 4dBi Gain (5GHz)")
    print("3) GL-iNet Opal: 19.4dBm Tx Power, 2dBi Gain (2.4GHz); 22.47dBm Tx Power, 2dBi Gain (5GHz)")

    while True:
        try:
            routerType = int(input("Enter 1, 2, or 3 -> "))
            if routerType == 1 or routerType == 2 or routerType == 3:
                break
            else:
                print("Invalid input, please enter 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter an integer (1, 2, or 3).")

    print("These routers are dual-band, meaning they opreate on both 2.4GHz and 5GHz frequencies.")
    print("Would you like to simulate the 2.4GHz or 5GHz band?")

    while True:
        try:
            bandChoice = float(input("Enter 2.4 or 5 -> "))
            if bandChoice == 2.4 or bandChoice == 5:
                break
            else:
                print("Invalid input, please enter 2.4 or 5")
        except ValueError:
            print("Invalid input. Please enter a number (2.4 or 5).")

    tx = routers[routerType - 1][f'{bandChoice}GHz']['Pt']
    gain = routers[routerType - 1][f'{bandChoice}GHz']['G']

    while True:
        try:
            wallName = int(input("Enter the wall type to use for this simulation (1=drywall, 2=brick, 3=concrete) -> "))
            if wallName in [1, 2, 3]:
                break
            else:
                print("Invalid input, please enter 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter an integer (1, 2, or 3).")

    while True:
        try:
            choice = int(input("Do you want to simulate an empty room, a room with medium clutter, or a room with heavy clutter? (1=empty, 2=medium, 3=heavy)-> "))
            if choice in [1, 2, 3]:
                break
            else:
                print("Invalid input, please enter 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter an integer (1, 2, or 3).")

    print(
        f"Running simulation on {routers[routerType - 1]["name"]} at {bandChoice}GHz using transmit power of {tx}dBm" 
        f" and gain of {gain}dBi. The wall type selected is {wallTypeList[wallName][0]}. And the room {clutter[choice - 1][0]}.")
    
    wallType = wallTypeList[wallName][1]

    return bandChoice, tx, gain, wallType, clutter[choice - 1][1]

def cust_user_input():
    bandChoice = float(input("Enter you router's frequency band in GHz (usually 2.4 or 5) -> "))
    tx = float(input("Enter its transmit power in dBm (usually between 8-30 dBm) -> "))
    gain = float(input("Enter its antenna gain in dBi (usually between 0-10 dBi) -> "))

    while True:
        try:
            wallType = int(input("Enter the wall type to use for this simulation (1=drywall, 2=brick, 3=concrete) -> "))
            if wallType in [1, 2, 3]:
                break
            else:
                print("Invalid input, please enter 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter an integer (1, 2, or 3).")

    while True:
        try:
            choice = int(input("Do you want to simulate an empty room, a room with medium clutter, or a room with heavy clutter? (1=empty, 2=medium, 3=heavy)-> "))
            if choice in [1, 2, 3]:
                break
            else:
                print("Invalid input, please enter 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter an integer (1, 2, or 3).")

    wallType = wallTypeList[wallType][1]
    return bandChoice, tx, gain, wallType, clutter[choice - 1][1]

def plotHeatmap(grid, router, wallGrid=None):
    plt.figure(figsize=(8, 8))

    numMin = -15
    numMax = -50

    im = plt.imshow(grid, origin="lower", cmap="inferno", alpha=0.85,
                    vmin=numMax, vmax=numMin)

    if wallGrid is not None:
        wall_overlay = np.ma.masked_where(wallGrid == 0, wallGrid)
        plt.imshow(wall_overlay, cmap="gray", origin="lower", alpha=0.35)

    i = 0
    for r in router:  
        if i == 0:
            plt.scatter(r[1], r[0], c='cyan', s=150, edgecolors='black', label="Router")
        else:
            plt.scatter(r[1], r[0], c='cyan', s=150, edgecolors='black')
        i += 1

    plt.colorbar(im, label="Signal Strength (dBm)")
    plt.title("Wi-Fi Signal Strength Heatmap")
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.legend(loc="upper right")

    plt.show()
