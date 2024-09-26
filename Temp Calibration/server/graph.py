import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from scipy.interpolate import make_interp_spline
from scipy.stats import linregress

from post_process_serial import get_dataframe, get_file

# Function to plot best-fit line
def plot_best_fit(ax, x, y, label):
    slope, intercept, rvalue, _, _ = linregress(x, y)
    ax.plot(x, slope * x + intercept, label=f'{label} Best Fit: Slope:{slope}  R2:{rvalue**2: .2f}', linestyle='--')

if __name__ == "__main__":
    file_name = "0.1-0.8accelV1"
    directory = r"data\bmi270\bed_accel"
    
    # Handle file conversion and get data read from file
    dataframe = get_dataframe(directory=directory, file_name=file_name)
    
    #zero milllis
    dataframe["TIME"] = dataframe["TIME"]-dataframe['TIME'][0]
    
    # Convert TIME to seconds
    dataframe['Seconds'] = dataframe['TIME'] / 1000.0
    
    # Integrate Gyroscope data to get angular position
    gyro_columns = ['GYROX', 'GYROY', 'GYROZ']
    for col in gyro_columns:
        dataframe[f'Position_{col}'] = np.cumsum(dataframe[col] * np.gradient(dataframe['Seconds']))
    
    # Define marker style and size
    marker_style = {'marker': '+', 's': 2}
    
    # trim to desired temperature
    min_value = 0
    max_value = 48
    first_index = dataframe[(dataframe['TEMP'] >= min_value) & (dataframe['TEMP'] <= max_value)].index[0]
    dataframe = dataframe.loc[first_index:]
    
    
    
    # Create subplots
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    fig1, axs1 = plt.subplots(2, 1, figsize=(10, 12))
    
    # Subplot for Acceleration X, Y, Z vs Time
    axs[0].scatter(dataframe['Seconds'], dataframe['ACCX'], label='ACCX', **marker_style)
    axs[0].scatter(dataframe['Seconds'], dataframe['ACCY'], label='ACCY', **marker_style)
    axs[0].scatter(dataframe['Seconds'], dataframe['ACCZ'], label='ACCZ', **marker_style)
    axs[0].set_title('Linear Accel vs Time')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel("Acceleration [G]")
    axs[0].legend()
    
    # Subplot for GYROscope X, Y, Z vs Time
    axs[1].scatter(dataframe['Seconds'], dataframe['GYROX'], label='GYROX', **marker_style)
    axs[1].scatter(dataframe['Seconds'], dataframe['GYROY'], label='GYROY', **marker_style)
    axs[1].scatter(dataframe['Seconds'], dataframe['GYROZ'], label='GYROZ', **marker_style)
    axs[1].set_title('Rotational Vel vs Time')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Velocity [Deg/s]')
    axs[1].legend()
    
    # Subplot for Temperature vs Time
    axs[2].scatter(dataframe['Seconds'], dataframe['TEMP'], label='Temp', color='r', **marker_style)
    axs[2].set_title('Temperature vs Time')
    axs[2].set_xlabel('Time [s]')
    axs[2].set_ylabel('Temperature [C]')
    axs[2].legend()
    
    # Define marker style and size
    marker_style = {}
    
    # Subplot for Integrated GYROscope (Position) vs Time
    axs1[0].scatter(dataframe['Seconds'], dataframe['Position_GYROX'], label='Position GYROX', **marker_style)
    axs1[0].scatter(dataframe['Seconds'], dataframe['Position_GYROY'], label='Position GYROY', **marker_style)
    axs1[0].scatter(dataframe['Seconds'], dataframe['Position_GYROZ'], label='Position GYROZ', **marker_style)
    # Best-fit lines
    plot_best_fit(axs1[0], dataframe['Seconds'], dataframe['Position_GYROX'], 'GYROX')
    plot_best_fit(axs1[0], dataframe['Seconds'], dataframe['Position_GYROY'], 'GYROY')
    plot_best_fit(axs1[0], dataframe['Seconds'], dataframe['Position_GYROZ'], 'GYROZ')
    axs1[0].set_title('Integrated Gyroscope (Position) vs Time')
    axs1[0].set_xlabel('Time [s]')
    axs1[0].set_ylabel('Position (degrees)')
    axs1[0].legend()
    
    # Group by 'TEMP' and calculate the mean for duplicates
    df_unique = dataframe.groupby('TEMP').mean().reset_index()

    # Create smooth curves
    temp_smooth = np.linspace(df_unique['TEMP'].min(), df_unique['TEMP'].max(), 300)

    spl_x = make_interp_spline(df_unique['TEMP'], df_unique['GYROX'], k=3)
    gyro_x_smooth = spl_x(temp_smooth)

    spl_y = make_interp_spline(df_unique['TEMP'], df_unique['GYROY'], k=3)
    gyro_y_smooth = spl_y(temp_smooth)

    spl_z = make_interp_spline(df_unique['TEMP'], df_unique['GYROZ'], k=3)
    gyro_z_smooth = spl_z(temp_smooth)

    # Plot
    axs1[1].plot(temp_smooth, gyro_x_smooth, label='Temp vs. GYROX')
    axs1[1].plot(temp_smooth, gyro_y_smooth, label='Temp vs. GYROY')
    axs1[1].plot(temp_smooth, gyro_z_smooth, label='Temp vs. GYROZ')
    # Best-fit lines
    plot_best_fit(axs1[1], df_unique['TEMP'], df_unique['GYROX'], 'GYROX')
    plot_best_fit(axs1[1], df_unique['TEMP'], df_unique['GYROY'], 'GYROY')
    plot_best_fit(axs1[1], df_unique['TEMP'], df_unique['GYROZ'], 'GYROZ')

    axs1[1].set_title('Gyro Accel vs Temp')
    axs1[1].set_xlabel('Temp [C]')
    axs1[1].set_ylabel('Accel G')
    axs1[1].legend()
    
    plt.tight_layout()
    plt.show()

    
    
    