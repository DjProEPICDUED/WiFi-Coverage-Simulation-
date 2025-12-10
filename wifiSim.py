import numpy as np
import matplotlib.pyplot as plt
from simFuncs import *
from inAndOut import *
from gui import *

while True:
    try:
        ui = input("Do you want to simulate a custom router or one of 3 best selling routers? (custom/best) -> ")
        if ui == "best":
            bandChoice, tx, gain, wallType, n = user_input()
            break
        elif ui == "custom":
            bandChoice, tx, gain, wallType, n = cust_user_input()
            break
        else:
            print("Enter a valid input.")
    except ValueError:
        print("Invalid input. Please enter a valid string.")

#For testing purposes
# routerType = 3
# bandChoice = 2.4
# tx = routers[routerType - 1][f'{bandChoice}GHz']['Pt']
# gain = routers[routerType - 1][f'{bandChoice}GHz']['G']

wallGrid, router = start_editor()
p0 = calc_p0(bandChoice, tx, gain)
grid = simuSignal(router, p0, n, wallGrid, wallType)

plotHeatmap(grid, router, wallGrid)