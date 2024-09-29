import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.font_manager import FontProperties
import numpy as np
import sys
import code
from scipy.signal import lsim, TransferFunction

# Specify the path to your data file
file_path = 'GyeongJuMKL_NS_FLAC.ACC'

# Initialize lists to hold time and acceleration values
time_values = []
acceleration_values = []

# Read the data from the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Read the total number of lines to be read
total_lines = int(lines[1].split()[0])  # 1700 from the second line
time_interval = float(lines[1].split()[1])  # seconds interval

# Initialize the first time value
time_initial = 0.0

# The initial acceleration value is provided on the second line
initial_value = float(lines[2].strip())
acceleration_values.append(initial_value)
time_values.append(time_initial)

# Process the remaining lines for acceleration data
for i in range(3, total_lines + 2):  # Start from the fourth line and read up to the 1700th line
    acceleration_values.append(float(lines[i].strip()))
    time_values.append(time_initial + (i - 2) * time_interval)  # Calculate time based on the interval

dt = time_values[2]-time_values[1]
velocity_value = np.cumsum(acceleration_values) * dt
displacement_value = np.cumsum(velocity_value) * dt

acceleration_in_g = [value / 9.81 for value in acceleration_values]

###############################################################
# Calculate Response Spectrum using Frequency Response Spectrum
###############################################################
# Define constants
zeta = 0.05  # Damping ratio, typically 5% for structural systems

# Define the frequency range for analysis (in rad/s)
periods = np.array([0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, \
                    0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, \
                    0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, \
                    0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36, 0.38, 0.4, \
                    0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7, \
                    0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.94, 0.96, 0.98, \
                    1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, \
                    2.0, 3.0, 4.0, 5.0])
omega_n = (1/periods)*2*np.pi

# Initialize the response spectrum array
Sd = np.zeros(len(omega_n))
Sv = np.zeros(len(omega_n))
Sa = np.zeros(len(omega_n))

# Loop through each natural frequency
for i, omega in enumerate(omega_n):
    wn = omega  # Natural frequency for the current loop
    
    # Define the system transfer function H(s) = 1 / (s^2 + 2*zeta*wn*s + wn^2)
    num = [1]  # Numerator (for acceleration)
    den = [1, 2*zeta*wn, wn**2]  # Denominator
    system = TransferFunction(num, den)

    # Calculate the response of the system to the ground acceleration
    _, y, _ = lsim(system, U=acceleration_in_g, T=time_values)
    
    # Maximum acceleration response
    Sd[i] = np.max(np.abs(y)) # Displacement response spectrum
    Sv[i] = Sd[i]*omega # Displacement response spectrum
    Sa[i] = Sd[i]*omega*omega # Displacement response spectrum

###############################################################

lable_properties = FontProperties(family='Cambria', style='normal', size=18)

# Plot the data
fig = plt.figure(figsize=(12, 8))  # Set the figure size (width, height) in inches
# Define the GridSpec with specific height and width ratios
gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1], width_ratios=[2, 1])
# Adjust the spacing between subplots
gs.update(wspace=0.1, hspace=0.3)  # Adjust these values to increase/decrease spacing

# First subplot 
ax1 = plt.subplot(gs[0, 0])  # This subplot takes first column of the first row
ax1.plot(time_values, acceleration_in_g, label='N-S Motion')
ax1.set_xlim(0.0, 16.0)
ax1.set_ylim(-0.4, 0.4)
#ax1.set_xlabel('Time (s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax1.set_ylabel('Acceleration (g)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax1.grid(False)
ax1.legend(frameon=False, prop={'family': 'Verdana', 'size': 8, 'weight': 'bold'}, loc='upper right', shadow=True)
ax1.tick_params(axis='both', direction='inout', length=10)

# Second subplot (smaller)
ax2 = plt.subplot(gs[0, 1])  # This subplot takes the second column of the first row
ax2.plot(periods, Sa, label='Pseudo Acc. Spectrum')
ax2.set_xlim(0.0, 2.0)
ax2.set_ylim(0.0, 1.0)
#ax2.set_xlabel('Time (s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax2.set_ylabel(r'S $\mathregular{_{a}}$ (g)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=40, rotation=270)
ax2.grid(True)
ax2.legend(frameon=False, prop={'family': 'Verdana', 'size': 8, 'weight': 'bold'}, loc='upper right', shadow=True)
ax2.tick_params(axis='both', direction='inout', length=10)

# Third subplot 
ax1 = plt.subplot(gs[1, 0])  # This subplot takes first column of the first row
ax1.plot(time_values, velocity_value, label='N-S Motion')
ax1.set_xlim(0.0, 16.0)
ax1.set_ylim(-0.1, 0.1)
#ax1.set_xlabel('Time (s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax1.set_ylabel('Velocity (m/s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax1.grid(False)
ax1.legend(frameon=False, prop={'family': 'Verdana', 'size': 8, 'weight': 'bold'}, loc='upper right', shadow=True)
ax1.tick_params(axis='both', direction='inout', length=10)

# 4th subplot (smaller)
ax2 = plt.subplot(gs[1, 1])  # This subplot takes the second column of the first row
ax2.plot(periods, Sv, label='Pseudo Vel. Spectrum')
ax2.set_xlim(0.0, 2.0)
ax2.set_ylim(0.0, 0.02)
#ax2.set_xlabel('Time (s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax2.set_ylabel(r'S $\mathregular{_{v}}$ (m/s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=40, rotation=270)
ax2.grid(True)
ax2.legend(frameon=False, prop={'family': 'Verdana', 'size': 8, 'weight': 'bold'}, loc='upper right', shadow=True)
ax2.tick_params(axis='both', direction='inout', length=10)

# 5th subplot 
ax1 = plt.subplot(gs[2, 0])  # This subplot takes first column of the first row
ax1.plot(time_values, displacement_value, label='N-S Motion')
ax1.set_xlim(0.0, 16.0)
ax1.set_ylim(-0.01, 0.01)
ax1.set_xlabel('Time (s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax1.set_ylabel('Displacement (m)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax1.grid(False)
ax1.legend(frameon=False, prop={'family': 'Verdana', 'size': 8, 'weight': 'bold'}, loc='upper right', shadow=True)
ax1.tick_params(axis='both', direction='inout', length=10)

# 6th subplot (smaller)
ax2 = plt.subplot(gs[2, 1])  # This subplot takes the second column of the first row
ax2.plot(periods, Sd, label='Pseudo Disp. Spectrum')
ax2.set_xlim(0.0, 2.0)
ax2.set_ylim(0.0, 0.002)
ax2.set_xlabel('Period (s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=20)
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax2.set_ylabel(r'S $\mathregular{_{d}}$ (m)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad=40, rotation=270)
ax2.grid(True)
ax2.legend(frameon=False, prop={'family': 'Verdana', 'size': 8, 'weight': 'bold'}, loc='upper right', shadow=True)
ax2.tick_params(axis='both', direction='inout', length=10)

# Display the figure
#plt.tight_layout()
plt.show()


#plt.figure(figsize=(15, 6))
#plt.subplot(3, 2, 1)
#plt.plot(time_values, acceleration_in_g, label='N-S Motion')
#plt.xlim(0.0, 16.0)
#plt.ylim(-0.4, 0.4)
##plt.title('Gyeong-ju EQ Station MKL N-S Motion')
#plt.xlabel('Time (s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad = 20)
#plt.ylabel('Acceleration (g)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad = 20)
#plt.grid(True)
#plt.legend(frameon=False, prop={'family': 'Verdana', 'size': 16, 'weight': 'bold'}, loc='upper right', shadow=True)
#plt.xticks(fontproperties=lable_properties)
#plt.yticks(fontproperties=lable_properties)
#plt.tick_params(axis='both', direction='inout', length=10)
## Display the plot
#plt.grid(axis='x', visible=False)
#plt.grid(axis='y', visible=False)
#
#plt.figure(figsize=(12, 8))
#plt.subplot(3, 2, 2)
#plt.plot(periods, Sa, label='Pseudo Acc. Spectrum')
#plt.xlim(0.0, 2.0)
#plt.ylim(0.0, 1.0)
#plt.xlabel('Time (s)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad = 20)
#plt.ylabel('Acceleration (g)', fontsize=20, fontweight='bold', family='Cambria', color='black', labelpad = 20)
#plt.grid(True)
#plt.legend(frameon=False, prop={'family': 'Verdana', 'size': 16, 'weight': 'bold'}, loc='upper right', shadow=True)
#plt.xticks(fontproperties=lable_properties)
#plt.yticks(fontproperties=lable_properties)
#plt.tick_params(axis='both', direction='inout', length=10)



#plt.subplot(3, 2, 3)
#plt.plot(time_values, a, label='Pseudo Acc. Spectrum')



