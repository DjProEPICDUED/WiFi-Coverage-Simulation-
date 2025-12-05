# 📶 Wi-Fi Signal Strength Simulator (dBm) w/ Wall Attenuation (Generates Heatmap)

A Python-based simulation tool that visualizes Wi-Fi signal propagation. It allows users to design custom floor plans, place routers, and generate signal heatmaps based on real-world physics, including wall attenuation and frequency bands.

## ✨ Features

  * **Interactive Floor Plan Editor:** Draw walls and place multiple routers using a simple GUI.
  * **Real-World Presets:** Choose from best-selling routers (TP-Link AX1800, Deco X55, GL-iNet Opal) or configure custom Tx power/Gain specs.
  * **Physics-Based Simulation:** Calculates signal loss based on:
      * Frequency (2.4GHz vs 5.0GHz).
      * Wall Materials (Drywall, Brick, Concrete).
      * Room Clutter (Empty, Medium, Heavy).
  * **Visual Heatmaps:** Generates a color-coded signal strength map (dBm) overlaying your floor plan.

## Requirements

You will need Python installed along with the following libraries:

```bash
pip install numpy matplotlib
```

## 🚀 How to Run

1.  Clone the repository or download the files.
2.  Run the main simulation script:

<!-- end list -->

```bash
python wifiSim.py
```

3.  **Configuration:** Follow the terminal prompts to select your router model, frequency band, and clutter level.
4.  **Map Editor:** A window will open.
      * **Left Click:** Draw Wall.
      * **Right Click:** Remove Wall.
      * **Middle Click:** Move existing router.
      * **Buttons:** Add or Remove routers dynamically.
      * **Enter:** Finish editing and run simulation.

## 📂 Project Structure

  * `wifiSim.py`: The main entry point. Orchestrates the inputs, editor, and simulation.
  * `gui.py`: Handles the interactive map editor (walls and router placement).
  * `simFuncs.py`: Contains the physics algorithms for path loss and wall attenuation.
  * `inAndOut.py`: Manages user inputs, router specifications, and heatmap plotting.

-----

**Note:** Ensure all `.py` files are in the same directory before running.
