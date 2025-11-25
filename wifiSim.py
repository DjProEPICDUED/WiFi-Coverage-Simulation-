import numpy as np
import matplotlib.pyplot as plt
from simFuncs import *
from userInput import *

# grid = np.zeros((50, 50))
# router = [25, 25]
wallGrid, router = start_editor()
grid = np.zeros((50, 50))

nEmpty = 1.6
nMedium = 2.5
nClutter = 3.5

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

# print("Choose one of the following best selling routers to run the simulation on:")
# print("1) TP-Link AX1800: 20dBm Tx Power, 4dBi Gain (2.4GHz); 20dBm Tx Power, 5dBi Gain (5GHz)")
# print("2) TP-Link Deco X55: 20dBm Tx Power, 3dBi Gain (2.4GHz); 20dBm Tx Power, 4dBi Gain (5GHz)")
# print("3) GL-iNet Opal: 19.4dBm Tx Power, 2dBi Gain (2.4GHz); 22.47dBm Tx Power, 2dBi Gain (5GHz)")

# while True:
#     routerType = int(input("Enter 1, 2, or 3 -> "))
#     if routerType == 1 or routerType == 2 or routerType == 3:
#         break
#     else:
#         print("Invalid input, please enter 1, 2, or 3")

# print("These routers are dual-band, meaning they opreate on both 2.4GHz and 5GHz frequencies.")
# print("Would you like to simulate the 2.4GHz or 5GHz band?")

# while True:
#     bandChoice = float(input("Enter 2.4 or 5 -> "))
#     if bandChoice == 2.4 or bandChoice == 5:
#         break
#     else:
#         print("Invalid input, please enter 2.4 or 5")

# tx = routers[routerType - 1][f'{bandChoice}GHz']['Pt']
# gain = routers[routerType - 1][f'{bandChoice}GHz']['G']

# while True:
#     print("Where do you want to place the router on the grid (it goes from 0 meters to 50 meters in the x and y directions)?")
#     router[0], router[1] = int(input("Enter a row (1-50) -> ")) - 1, int(input("Enter a column (1-50) - > ")) - 1
#     if 0 <= router[0] < 50 and 0 <= router[1] < 50:
#         break
#     else:
#         print("Invalid input, please enter row and column values between 1 and 50")

# print(
#     f"Running simulation on {routers[routerType - 1]["name"]} at {bandChoice}GHz using transmit power of {tx}dBm" 
#     f" and gain of {gain}dBi.")


#TEMP
routerType = 3
bandChoice = 2.4
tx = routers[routerType - 1][f'{bandChoice}GHz']['Pt']
gain = routers[routerType - 1][f'{bandChoice}GHz']['G']
# router[0], router[1] = 25, 25

p0 = calc_p0(bandChoice, tx, gain)
newGrid = simuSignal(grid, router, p0, nEmpty, wallGrid)

plotHeatmap(newGrid, router, wallGrid)