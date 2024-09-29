import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import os
from utils import get_dataframe, plot_best_fit

mpl.style.use('fast')  # Use the fast style for performance
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 0.1
mpl.rcParams['agg.path.chunksize'] = 10000


class graphGyro:
    def __init__(self, file_names: list[(str, str)], directory: os.PathLike, trim_temp: None|tuple[int, int]) -> None:
        self.file_names = file_names # file name, reference name
        self.directory = directory
        self.trim_temp = trim_temp
        self.dataframes = []

        # Define marker style and size
        self.scatter_style = {'marker': '+', 's': 2}
        
    def loadFiles(self):
        for file in self.file_names:
            dataframe = get_dataframe(self.directory, file[0])
            
            first_index = dataframe[(dataframe['TEMP'] >= self.trim_temp[0]) & (dataframe['TEMP'] <= self.trim_temp[1])].index[0]
            dataframe = dataframe.loc[first_index:]
            
            self.dataframes.append(dataframe)
        return self.dataframes
            
    def plotVsTemp(self, dataframes: list[pd.DataFrame]):
        fig, axs = plt.subplots(len(dataframes)+1, 1, figsize=(10, 12))
        
        for index, df in enumerate(dataframes):
            # Subplot for GYROscope X, Y, Z vs Time
            axs[index].scatter(df['TEMP'], df['GYROX'], label=f'{self.file_names[index][0]} GYROX', **self.scatter_style)
            axs[index].scatter(df['TEMP'], df['GYROY'], label=f'{self.file_names[index][0]} GYROY', **self.scatter_style)
            axs[index].scatter(df['TEMP'], df['GYROZ'], label=f'{self.file_names[index][0]} GYROZ', **self.scatter_style)
            axs[index].set_title('Rotational Vel vs Temp')
            axs[index].set_xlabel('Temp [C]]')
            axs[index].set_ylabel('Velocity [Deg/s]')
            axs[index].legend(loc = "upper right")
           
        #print best fit of each axis on seperate figure
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
        axes = ["GYROX", 'GYROY', 'GYROZ']
        for index, axis in enumerate(axes):
            for df_index, df in enumerate(dataframes):
                plot_best_fit(axs[index], df['TEMP'], df[axis], f'{self.file_names[df_index][0][-6:]} {axis}')
            axs[index].set_title(f"Best Fit: Temp Vs. Vel. {axis}")
            axs[index].set_xlabel('Temp [C]]')
            axs[index].set_ylabel('Velocity [Deg/s]')
            axs[index].legend(loc = "upper right")
            
    def plot(self):
        plt.tight_layout()
        plt.show()
        
            

if __name__ == "__main__":
    directory = os.path.join("data", "bmi270", "static", "Const")
    directory1 = os.path.join("data", "bmi270", "static", "Tcal")
    file_names = [
        (os.path.join(directory1, "T1001_IMU1"), "IMU1"), 
        (os.path.join(directory1, "T1000_IMU1"), "IMU1"),
        (os.path.join(directory1, "T1002_IMU2"), "IMU2")
        ]
    
    min_value = 7
    max_value = 500
    
    gyro = graphGyro(file_names, None, (min_value, max_value))
    gyro.loadFiles()
    gyro.plotVsTemp(gyro.dataframes)
    gyro.plot()

    
    
    