import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np

from post_process_serial import get_dataframe



if __name__ == "__main__":
    file_name = "v1_tempchange"
    directory = r"data\bmi270\static"
    
    # Handle file conversion and get data read from file
    dataframe = get_dataframe(directory=directory, file_name=file_name)
    
    #zero milllis
    dataframe["Millis"] = dataframe["Millis"]-dataframe['Millis'][0]
    
    # Convert Millis to seconds
    dataframe['Seconds'] = dataframe['Millis'] / 1000.0
    
    # Integrate Gyroscope data to get angular position
    gyro_columns = ['GyroX', 'GyroY', 'GyroZ']
    for col in gyro_columns:
        dataframe[f'Position_{col}'] = np.cumsum(dataframe[col] * np.gradient(dataframe['Seconds']))
    
    # Define marker style and size
    marker_style = {'marker': '+', 's': 2}
    
    # Create subplots
    fig, axs = plt.subplots(4, 1, figsize=(10, 12))
    
    # Subplot for Acceleration X, Y, Z vs Time
    axs[0].scatter(dataframe['Seconds'], dataframe['AccelX'], label='AccelX', **marker_style)
    axs[0].scatter(dataframe['Seconds'], dataframe['AccelY'], label='AccelY', **marker_style)
    axs[0].scatter(dataframe['Seconds'], dataframe['AccelZ'], label='AccelZ', **marker_style)
    axs[0].set_title('Linear Accel vs Time')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel("Acceleration [G]")
    axs[0].legend()
    
    # Subplot for Gyroscope X, Y, Z vs Time
    axs[1].scatter(dataframe['Seconds'], dataframe['GyroX'], label='GyroX', **marker_style)
    axs[1].scatter(dataframe['Seconds'], dataframe['GyroY'], label='GyroY', **marker_style)
    axs[1].scatter(dataframe['Seconds'], dataframe['GyroZ'], label='GyroZ', **marker_style)
    axs[1].set_title('Rotational Vel vs Time')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Velocity [Deg/s]')
    axs[1].legend()
    
    # Subplot for Integrated Gyroscope (Position) vs Time
    axs[2].scatter(dataframe['Seconds'], dataframe['Position_GyroX'], label='Position GyroX', **marker_style)
    axs[2].scatter(dataframe['Seconds'], dataframe['Position_GyroY'], label='Position GyroY', **marker_style)
    axs[2].scatter(dataframe['Seconds'], dataframe['Position_GyroZ'], label='Position GyroZ', **marker_style)
    axs[2].set_title('Integrated Gyroscope (Position) vs Time')
    axs[2].set_xlabel('Time [s]')
    axs[2].set_ylabel('Position (degrees)')
    axs[2].legend()
    
    # Subplot for Temperature vs Time
    axs[3].scatter(dataframe['Seconds'], dataframe['Temp'], label='Temp', color='r', **marker_style)
    axs[3].set_title('Temperature vs Time')
    axs[3].set_xlabel('Time [s]')
    axs[3].set_ylabel('Temperature [C]')
    axs[3].legend()
    
    plt.tight_layout()
    plt.show()

    
    
    