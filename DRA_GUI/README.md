# GUI for Laser Heating Simulation

## Overview
This GUI interface allows users to set parameters for the laser heating simulation, including laser properties, material selection, and simulation duration. The GUI gathers input and passes it to the simulation script, making it easy to customize and run simulations without modifying code directly.

## Features
- **Interactive Parameter Input**: Allows users to select laser wavelength, power, material type, and more through an intuitive interface.
- **File Selection**: Enables users to select a video file for comparison with the simulation output.
- **Dark Mode Option**: Customizable appearance with a toggle for light and dark modes.
- **Simulation Control**: Submits the input parameters to the simulation, starting the process with a single click.

## File Structure
- **`GUI_DRA.py`**: The main GUI file that creates the user interface and handles input for the simulation.

## Usage
1. **Launch the GUI**: Run `GUI_DRA.py` to open the interface.
   ```bash
   python GUI_DRA.py
   ```
2. **Set Parameters**: Enter the laser and material properties in the designated fields.
3. **Select Video for Comparison**: Use the file selection option to choose a video file.
4. **Run Simulation**: Click **Submit** to start the simulation with the configured parameters.

## Code Structure
- **Input Sections**: Divided into laser properties, material properties, and simulation time.
- **File Selection**: Allows the user to choose a comparison video file.
- **Submit Button**: Triggers the simulation process.

## Dependencies
- **CustomTkinter**: Used for a modern, interactive interface.
- **Tkinter**: Standard Python library for GUI applications.

## Example Run
Launching the GUI allows users to configure all simulation parameters, ensuring flexibility and ease of use.
