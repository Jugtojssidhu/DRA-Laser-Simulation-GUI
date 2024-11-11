# Laser Heating Simulation

## Overview
This simulation models the heating of metallic surfaces when exposed to a laser, specifically for research applications involving infrared technology. The simulation takes in user-defined laser properties and material characteristics to simulate the temperature changes over time on a metallic sheet. This component is integrated with a GUI interface, which gathers input from users and initiates the simulation process.

## Features
- **Material and Laser Properties**: Simulates heat dispersion based on parameters like laser wavelength, power, and material type (e.g., copper, titanium).
- **Customizable Simulation Time**: The simulation time can be adjusted according to user requirements.
- **Grid-Based Temperature Calculations**: Utilizes a grid to compute temperature changes and simulate radiative losses and laser-induced heating.
- **Outputs Video**: Generates a video visualizing the temperature distribution over time on the surface.

## File Structure
- **`DRA_program_main_test.py`**: Main simulation script that defines materials, laser properties, surface characteristics, and calculates the temperature changes over time.

## Usage
1. **Set Parameters**: Modify parameters in the GUI to select the material type, laser power, wavelength, and other characteristics.
2. **Run Simulation**: Upon submission in the GUI, the simulation will execute and calculate the temperature distribution based on the user-defined parameters.
3. **Output Video**: The simulation generates a video output (e.g., `simulation_video.mp4`) that visualizes the heat dispersion over time.

## Code Structure
- **Materials**: Defines properties for various materials, such as molar mass, density, and heat capacity.
- **Laser Properties**: Manages laser parameters like wavelength and power.
- **Surface and Temperature Calculation**: Computes heat dispersion across a grid on the surface, accounting for radiative losses and laser-induced heating.

## Dependencies
- **Python Libraries**: Ensure that `numpy`, `matplotlib`, and any other required libraries (specified in the project’s main requirements) are installed.

## Example Run
An example output video illustrates the temperature distribution across the metallic surface, with color gradations indicating varying temperature levels.

