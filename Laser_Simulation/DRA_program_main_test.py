from dataclasses import dataclass       # using class as creating containers
from functools import cached_property   # turns method value into an attribute

import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib.animation import FuncAnimation

#Stuff from GUI jugs 
from GUI_DRA import App
import threading
import os

@dataclass
class Material:
    """class for properties of a single copper with methods to assist"""
    name:                str = ""      # e.g. Copper
    molarMass:           tuple = (0.0,"")
    density:             tuple = (0.0,"")
    heatCapacity:        tuple = (0.0,"") 
    thermalConductivity: tuple = (0.0,"")
    blueAbsorption:      float = (0.0)
    emissivity:          float = (0.0) 

    @cached_property
    def specific_heat_capacity(self) :
        molsPerGram = 1.0/self.molarMass[0]
        val = molsPerGram*self.heatCapacity[0]
        return (val*1.e3,"J/kg/K")   # J/Kg/K

@dataclass
class Laser:
    """class for properties of a laser with methods to assist"""
    name:                str = ""      # e.g. Copper
    wavelength:          tuple = (0.0,"")
    power:               tuple = (0.0,"")
    M2:                  float = (0.0)

@dataclass
class LaserPosition:
    cx:                  float = (0.0) #mm
    cy:                  float = (0.0) #mm
    r:                   float = (0.0) #mm
    cx_speed:        float = (0.0) 
    cy_speed:        float = (0.0)
    r_speed:         float = (0.0)

@dataclass
class Surface:
    """class for properties of the surface, independent of material, with methods to assist """
    width:               float = (0.0) #mm
    height:              float = (0.0) #mm
    depth:               float = (0.0) #mm
    dx:                  float = (0.0) # intervals in x, mm  
    dy:                  float = (0.0) # intervals in y, mm
    Tcool:               float = (0.0) #K



               
# take user input to assign surface instance
def input_material_choice():

    """JUGS CHANGES TO INPUT"""
    file_path = "simulation_data.txt" 
    simulation_data = parse_simulation_data(file_path)
    """END OF JUGS CHANGES TO INPUT"""
    
    material_choice = simulation_data.get("Material selected", "Default Material") #I changed this too
    print("this was run")

    if material_choice == 'copper':
        material = copper
    elif material_choice == 'titanium':
        material = titanium
    elif material_choice == 'test':
        material = test_material
    else:
        print("Ivalid material. Add instance of any new material.")
        exit()
    return material

# take user input to allow a varying time frame for the simulation
def input_simulation_time():
    """JUGS CHANGES TO INPUT"""
    file_path = "simulation_data.txt" 
    simulation_data = parse_simulation_data(file_path)
    """END OF JUGS CHANGES TO INPUT"""
    length = float(simulation_data.get("Simulation Time", "0")) #I changed this too
    frames = int(length/dt)
    return frames

# makes a grid of uniform temperature 'Tcool'/300K. Used for heating simulation
def initialize_Tcool(nx, ny, dx, dy, Tcool, cx, cy):
    x = np.arange(0, nx * dx, dx)
    y = np.arange(0, ny * dy, dy)
    X, Y = np.meshgrid(x, y)
    u0 = Tcool * np.ones_like(X)
    return u0, X, Y

# calculates sigma, which changes with r
def calculate_sigma(r):
    #sigma = (blueLaser.M2 / (2 * np.sqrt(2 * np.log(2))))  #mm Standard deviation of the Gaussian
    sigma = r/(np.sqrt(2))
    return sigma

# calculates power/unit area, which also changes with r
def power_area(sigma):
    power_distribution_mode = 1 #1 is gaussian, 2 is flat top power distributioj
    if power_distribution_mode == 1:
        power_area = blueLaser.power[0]/(2 * np.pi * (sigma**2))
        
    if power_distribution_mode == 2:
        power_area = blueLaser.power[0]/(np.pi * (r**2))
    return power_area

# create function that allows laser position/size to change over time
# NOTE: I plan on changing the implementation of this function to allow for a greater variety of functions
def change_laser_position(cx, cy, r, x_increment, y_increment, r_increment, nsteps, step_count, dt):
    animation_mode = 0 #1 is grid lines. 0 is static
    global line_count
    t = step_count*dt 
    if animation_mode == 0:
        return cx, cy, r
    if animation_mode == 1:
        if line_count%2 != 0 and line_count != 0:
            x_increment = -x_increment

        cx = cx + x_increment
        if cx < 0 or cx> 100:
            print(cx)
            cx = max(0, min(cx, 100))
            cy = cy +  20 #jump down 2 cm/ 20mm
            line_count += 1

    if animation_mode == 2:
        t = step_count*dt 
        cx = 0.5*(cx + np.cos(t))
        cy = 0.5*(cy + np.sin(t))

    return cx, cy, r

#calculates the radiative loss iteratively each time do_timestep is called
def calculate_radiative_loss(T_surface, Tcool):

    boltzman_constant = (5.67036e-8)/(1000)**2 #Wmm^-2K^-4

    mu = (boltzman_constant * material.emissivity)/(surface.depth * rho_kgmm * Cp) #Not too sure about the validity          
    return  mu * (T_surface**4 - Tcool**4)  

def do_timestep(u0, u, X, Y, cx, cy, r):
    sigma = calculate_sigma(r)
    power_volume = power_area(sigma) / surface.depth
    
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * (
        (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
        + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 ) 

    radiation_cooling = calculate_radiative_loss(u[1:-1, 1:-1], surface.Tcool)


    laser_heating = (((material.blueAbsorption)*(power_volume))/(rho_kgmm*Cp))* np.exp(-(((X - cx) ** 2 + (Y - cy) ** 2) / (sigma ** 2))/2)



    laser_heating_flattop = np.zeros_like(u)  # Initialize flat top laser heating array
    within_radius = np.sqrt((X - cx)**2 + (Y - cy)**2) <=r
    laser_heating_flattop[within_radius] = power_volume / (rho_kgmm * Cp)
    


    u[1:-1, 1:-1] += (laser_heating_flattop[1:-1, 1:-1] - radiation_cooling) * dt        
    u0 = u.copy()
    return u0, u


# Animation update function
def update(frame):


    global u, u0, X, Y, cx_i, cy_i, r_i, dt
    cx_i, cy_i, r_i = change_laser_position(cx_i, cy_i, r_i, x_increment, y_increment, r_increment, nsteps, step_count,dt)
    cx, cy, r = cx_i, cy_i, r_i
    u0, u = do_timestep(u0, u, X, Y, cx , cy, r)
    im.set_array(u.copy())
    ax.set_title('{:.1f} ms'.format(frame * dt * 1000))
    return im

    
"""JUGS GUI STUFF"""
def parse_simulation_data(file_path):
    data = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split(":", 1)
                data[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while parsing the file: {e}")
    return data

def clean(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")
    else:
        print(f"The file {file_path} does not exist.")
"""END OF JUGS GUI STUFF"""
    
if __name__ == "__main__":

    """Instantiaiting class objects"""

    titanium = Material(name="titanium", \
                molarMass=(47.87,"g/mol"),\
                density=(4.506,"g/cm3"),\
                heatCapacity=(25.060,"J/mol/K"),
                thermalConductivity=(19.4, "W/m/k"),
                blueAbsorption=0.85,
                emissivity = 0.2)
    copper = Material(name="copper", \
                molarMass=(63.546,"g/mol"),\
                density=(8.96,"g/cm3"),\
                heatCapacity=(24.440,"J/mol/K"),
                thermalConductivity=(401,"W/m/k"),
                blueAbsorption=0.65,
                emissivity = 0.07)
    test_material = Material(name = 'test_material',
                molarMass=(120,"g/mol"),\
                density=(2,"g/cm3"),\
                heatCapacity=((600),"J/mol/K"),
                thermalConductivity=(3.0,"W/m/k"),
                blueAbsorption=0.75,
                emissivity = 0.2)            
    blueLaser = Laser(name="blue", \
                wavelength=(405.0,"nm"),\
                power=(10.0,"W"),\
                M2=(10.0) )
    laser_position = LaserPosition(cx = (50.0),\
                cy = (50.0),\
                r = (7),\
                cx_speed = (4000.0),#mm/s\ 
                cy_speed = (0.0),#mm/s\
                r_speed = (0.0))
    surface = Surface(width = (100.0),\
                height = (100.0),\
                depth = (0.5),\
                dx = (0.4),\
                dy = (0.4),\
                Tcool = (300))

    """Define global variables"""

    save_mode = 0 #save mode 1 will save the animation as a mp4, 0 (default) simply displays the animation
                  #NOTE saving the mp4 requires downloading ffmpeg and setting it as an environment path
    
    material = input_material_choice()  

    k = material.thermalConductivity[0] #W/m/k

    rho = material.density[0] #g/m^3
    print("%f rho:", rho)
    rho_mm = rho/(10)**3 #g/mm-3
    rho_kgmm = rho_mm/1000 #kg/mm-3

    Cp = material.specific_heat_capacity[0] #J/kgK
    print("%f Cp:", Cp)
    alpha = k/(rho*1000.)/Cp    # Thermal Diffusivity, m^2/s
    D = alpha * 1.e6 # Thermal diffusivity of copper, mm^2/s
 
    nx, ny = int(surface.width/surface.dx), int(surface.height/surface.dy) # Number of grid points in each direction (x,y) on the 2-D target surface
    dx2, dy2 = surface.dx**2, surface.dy**2 
    dt = dx2 * dy2/(2*D*(dx2 + dy2)) # The time step dt is chosen for stability of the explicit algorithm
    print("dt:", dt)
    u0 = surface.Tcool * np.ones((nx, ny)) #dreate 
    u = u0.copy()
    assert u0.all() == u.all() 


    """Define laser position and beam size"""
    cx_i = laser_position.cx
    cy_i = laser_position.cy
    r_i = laser_position.r  

    cx = laser_position.cx
    cy = laser_position.cy
    r = laser_position.r
    
    line_count = 0 
    x_speed = laser_position.cx_speed
    y_speed = laser_position.cy_speed
    r_speed = laser_position.r_speed
    
    x_increment = x_speed*dt 
    y_increment = y_speed*dt
    r_increment = r 


    nsteps = input_simulation_time()  # Number of timesteps    
    step_count = 0 #counter for each frame, used to calculate time
    print('Total time: ', nsteps*dt)

    u0, X, Y = initialize_Tcool(nx,ny,surface.dx, surface.dy, surface.Tcool, cx, cy)

    #Main loop to run the simulation over time
    for m in range(nsteps):
        step_count = step_count + 1
        cx, cy, r = change_laser_position(cx, cy, r, x_increment, y_increment, r_increment, nsteps, step_count, dt)

        u0, u = do_timestep(u0, u, X, Y, cx, cy, r)
        if m%100 == 0:
            print(f"After timestep - cx: {cx}, cy: {cy}, r: {r}, t:{m*dt*1000}", 'ms')



    # animation
    fig, ax = plt.subplots()
    im = ax.imshow(u0.copy(), cmap=plt.get_cmap('hot'))
    ax.set_axis_off()
    ax.set_title('Initial State')
    fig.colorbar(im, ax=ax)

    
    u0, X, Y = initialize_Tcool(nx, ny, surface.dx, surface.dy, surface.Tcool, cx, cy)
    if save_mode == 1:
        # Define the file name for the output video
        animation = FuncAnimation(fig, update, frames= nsteps, interval=0.1, repeat=False)
        output_file = "simulation_video_1.mp4"
        # Save the animation as a video file, extra_args assures that the encoding is supported by most video players
        animation.save(output_file, writer='ffmpeg', fps=120, codec='libx264', bitrate=5000, extra_args=['-pix_fmt', 'yuv420p'])
    else:
        # Create the animation, display
        animation = FuncAnimation(fig, update, frames= nsteps, interval=0.1, repeat=False)
        plt.show()
    