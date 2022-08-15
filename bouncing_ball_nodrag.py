"""

author: Angelica Uzo
course: Chemical Engineering
school: University of Birmingham

"""

# This code will model the trajectory of a hard spherical steel ball without drag forces 
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
rho_steel = 7480 #kg m^-3 for the ball

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

# t_current represents the time at the current position of the projectile
t_current = t0

# r_current is an array containing the current horizontal and vertical displacements of the projectile respectively 
r_current = np.array([rx0 , ry0]) 

# v_current is an array containing the current horizontal and vertical velocities of the projectile respectively
v_current = np.array([v0 * np.cos(np.radians(theta)) , v0 * np.sin(np.radians(theta))])

# position, time and speed represent empty lists into which the r_current, t_current and v_current
# values will be appended respectively
position = []
time = []
speed = []

# Euler's Method
# This loop calculates r_current and v_current at t_current and appends it to the list 'position' and 'speed' 
# respectively until t_current is equal to tf after which the loop is terminated. 
while t_current <= tf:
    # Calculating acceleration
    # a[0] is the acceleration along the horizontal whereas a[1] is the acceleration along the vertical
    a = np.array([0, - g])
    # r_current[0] represents the horizontal displacement, r_current[1] represents the vertical displacement
    # v_current[0] represents the horizontal velocity, v_current[1] represents the vertical velocity
    v_new = np.array([v_current[0] + dt * a[0] , v_current[1] + dt * a[1]])
    r_new = np.array([r_current[0] + v_current[0] * dt , r_current[1] + v_current[1] * dt])
    # 'position.append(r_current)' modifies the list 'position' by adding r_current to the end of the list 
    # rx_and_ry represents an array of the entries within 'position'
    position.append(r_current)
    rx_and_ry = np.array(position)
    # This modifies the list 'speed' by adding v_current to the end of the list 
    # v represents an array of the entries within 'speed'
    speed.append(v_current)
    v = np.array(speed)
    # The 'if' conditional statement below accounts for the bounce
    if r_new[1] < 0 and r_current[1] >= 0 :
        v_new[1] = -cor * v_new[1]
    # r_new and v_new become the next timestep's r_current and v_current values
    v_current = v_new
    r_current = r_new
    # 'time.append(t_current)' modifies the list 'time' by adding t_current to the end of the list 
    # t represents an array of the entries within 'time'
    time.append(t_current)
    t = np.array(time)
    # This defines t_current at the new timestep and the loop repeats
    t_current = t_current + dt
# Plotting the graphs
fig, axes = plt.subplots(1, 3)
fig.set_size_inches(18, 6)
# rx_and_ry[:,0] represents the horizontal displacement
# rx_and_ry[:,1] represents the vertical displacement
axes[0].scatter(rx_and_ry[:,0], rx_and_ry[:,1], c=t, label = "Euler Projectile Position")
axes[0].set_xlabel("Horizontal Displacement ($m$)")
axes[0].set_ylabel("Vertical Displacement ($m$)")
axes[0].set_title("Trajectory of Projectile")
axes[1].plot(t, rx_and_ry[:,0], label = "rx(t) vs. t")
axes[1].plot(t, rx_and_ry[:,1], label = "ry(t) vs. t")
axes[1].set_xlabel("Time ($s$)")
axes[1].set_ylabel("Displacement ($m$)")
axes[1].set_title("Displacement vs. Time")
# v[:,0] represents the horizontal component of velocity
# v[:,1] represents the vertical component of velocity
axes[2].plot(t, v[:,0], label = "vx(t) vs. t")
axes[2].plot(t, v[:,1], label = "vy(t) vs. t")
axes[2].set_xlabel("Time ($s$)")
axes[2].set_ylabel("Velocity ($m$)")
axes[2].set_title("Velocity vs. Time")

# Adding the legend
for ax in axes:
    ax.legend()
