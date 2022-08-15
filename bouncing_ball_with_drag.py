"""

author: Angelica Uzo
course: Chemical Engineering
school: University of Birmingham

"""

# This code will model the trajectory of a hard spherical steel ball with and without drag forces acting 
# travelling through air provided the initial position, initial speed and angle of inclination 
# to the horizontal in degrees at an initial time, t0 in steps dt until final time, tf is reached
import numpy as np
import matplotlib.pyplot as plt
import seaborn; seaborn.set_style("whitegrid")

# Pre-defined parameters
# Initial position
rx0 = 0 #m
ry0 = 10 #m

# Initial speed and angle of inclination to the horizontal
v0 = 10 #m s^-1
theta = 0 #in degrees

# Gravitational acceleration
g = 9.81 #m s^-2

# Initial time
t0 = 0 #s

# Coefficient of restitution
cor = 0.7 #dimensionless 

# Density
rho_air = 1.2 #kg m^-3 for the fluid
rho_steel = 7850 #kg m^-3 for the ball

# Steel ball dimensions
diameter = 1e-2 #m
radius = diameter/2 #m
cd = 0.47 #drag coefficient (dimensionless)
# The projected area of a sphere is a circle
projected_area = np.pi * radius ** 2 #m^2
volume = np.pi * 4 / 3 * radius ** 3 #m^3
mass = volume * rho_steel #kg

# User-defined parameters
# Time step                          
dt = 0.01 #s

# Final time
tf = 10 #s 

# This fuction returns the drag force at the velocity stated
def drag_force(velocity):
    drag = cd * projected_area * rho_air * velocity ** 2 / 2
    return drag

# t_current represents the time at the current position of the projectile
t_current = t0

# r_current is an array containing the current horizontal and vertical displacements of the projectile respectively 
r_current_drag = np.array([rx0 , ry0]) 
r_current_nodrag = np.array([rx0 , ry0])

# v_current is an array containing the current horizontal and vertical velocities of the projectile respectively
v_current_drag = np.array([v0 * np.cos(np.radians(theta)) , v0 * np.sin(np.radians(theta))])
v_current_nodrag = np.array([v0 * np.cos(np.radians(theta)) , v0 * np.sin(np.radians(theta))])

# position, time and speed represent empty lists into which the r_current, t_current and v_current
# values will be appended respectively
position_drag = []
position_nodrag = []
speed_drag = []
speed_nodrag = []
time = []

# Euler's Method
# This loop calculates r_current and v_current at t_current and appends it to the list 'position' and 'speed' 
# respectively for both drag and no drag until t_current is equal to tf after which the loop is terminated.  
while t_current <= tf:
    # Calculating acceleration
    # a[0] is the acceleration along the horizontal whereas a[1] is the acceleration along the vertical
    # drag acts in a direction opposite to motion
    v0_magitude = np.sqrt(v_current_drag[0]**2 + v_current_drag[1]**2)
    # (-v_current_drag[0]/v0_magitude) represents the unit vector in the x-direction
    # (-v_current_drag[1]/v0_magitude) represents the unit vector in the y-direction
    a_drag = np.array([0 + 1 / mass * drag_force(v_current_drag[0]) * (-v_current_drag[0]/v0_magitude), - g + 1 / mass * drag_force(v_current_drag[1]) * (-v_current_drag[1]/v0_magitude)])
    a_nodrag = np.array([0, - g])
    # r_current[0] represents the vertical displacement, r_current[1] represents the horizontal displacement
    # v_current[0] represents the vertical velocity, v_current[1] represents the horizontal velocity
    v_new_drag = np.array([v_current_drag[0] + dt * a_drag[0] , v_current_drag[1] + dt * a_drag[1]])
    r_new_drag = np.array([r_current_drag[0] + v_current_drag[0] * dt , r_current_drag[1] + v_current_drag[1] * dt])
    v_new_nodrag = np.array([v_current_nodrag[0] + dt * a_nodrag[0] , v_current_nodrag[1] + dt * a_nodrag[1]])
    r_new_nodrag = np.array([r_current_nodrag[0] + v_current_nodrag[0] * dt , r_current_nodrag[1] + v_current_nodrag[1] * dt])
    # 'position.append(r_current)' modifies the list 'position' by adding r_current to the end of the list 
    # rx_and_ry represents an array of the entries within 'position'
    position_drag.append(r_current_drag)
    rx_and_ry_drag = np.array(position_drag)
    position_nodrag.append(r_current_nodrag)
    rx_and_ry_nodrag = np.array(position_nodrag)
    # This modifies the list 'speed' by adding v_current to the end of the list 
    # v represents an array of the entries within 'speed'
    speed_drag.append(v_current_drag)
    v_drag = np.array(speed_drag)
    speed_nodrag.append(v_current_nodrag)
    v_nodrag = np.array(speed_nodrag)
    # The 'if' conditional statement below accounts for the bounce
    if r_new_drag[1] < 0 and r_current_drag[1] >= 0 :
        v_new_drag[1] = -cor * v_new_drag[1]
    if r_new_nodrag[1] < 0 and r_current_nodrag[1] >= 0 :
        v_new_nodrag[1] = -cor * v_new_nodrag[1]
    # r_new and v_new become the next timestep's r_current and v_current values
    v_current_drag = v_new_drag
    v_current_nodrag = v_new_nodrag
    r_current_drag = r_new_drag
    r_current_nodrag = r_new_nodrag
    # 'time.append(t_current)' modifies the list 'time' by adding t_current to the end of the list 
    # t represents an array of the entries within 'time'
    time.append(t_current)
    t = np.array(time)
    # This defines t_current at the new timestep and the loop repeats
    t_current = t_current + dt

# Plotting the Graphs
fig, axes = plt.subplots(1, 3)
fig.set_size_inches(18, 6)
axes[0].plot(rx_and_ry_drag[:,0], rx_and_ry_drag[:,1], 'k--', label = "Euler Projectile Position with Drag")
axes[0].plot(rx_and_ry_nodrag[:,0], rx_and_ry_nodrag[:,1], 'r-', label = "Euler Projectile Position without Drag")
axes[0].set_xlabel("Horizontal Displacement ($m$)")
axes[0].set_ylabel("Vertical Displacement ($m$)")
axes[0].set_title("Trajectory of Projectile")
axes[1].plot(t, rx_and_ry_drag[:,0], 'k--', label = "rx(t) vs. t with drag")
axes[1].plot(t, rx_and_ry_nodrag[:,0], 'r-',label = "rx(t) vs. t without drag")
axes[1].plot(t, rx_and_ry_drag[:,1], 'y--', label = "ry(t) vs. t with drag")
axes[1].plot(t, rx_and_ry_nodrag[:,1], 'g-', label = "ry(t) vs. t without drag")
axes[1].set_xlabel("Time ($s$)")
axes[1].set_ylabel("Displacement ($m$)")
axes[1].set_title("Displacement vs. Time")
axes[2].plot(t, v_drag[:,0], 'k--', label = "vx(t) vs. t with drag")
axes[2].plot(t, v_nodrag[:,0], 'r-',label = "vx(t) vs. t without drag")
axes[2].plot(t, v_drag[:,1], 'y--', label = "vy(t) vs. t with drag")
axes[2].plot(t, v_nodrag[:,1], 'g-', label = "vy(t) vs. t without drag")
axes[2].set_xlabel("Time ($s$)")
axes[2].set_ylabel("Velocity ($m$)")
axes[2].set_title("Velocity vs. Time")

# Adding the legend
for ax in axes:
    ax.legend()
    