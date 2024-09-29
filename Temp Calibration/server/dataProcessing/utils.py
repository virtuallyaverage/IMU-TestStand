import pandas as pd
from io import StringIO
from scipy.stats import linregress

def get_dataframe(directory, file_name):
    return pd.read_csv(StringIO(open_csv(directory, file_name)))
          
def open_csv(directory, file_name):
    if directory is not None:
        with (open(directory+"\\"+file_name+".csv", 'r')) as file:
            return file.read()  
    else:
        with (open(file_name+".csv", 'r')) as file:
            return file.read()  
    
# Function to plot best-fit line
def plot_best_fit(ax, x, y, label):
    slope, intercept, rvalue, _, _ = linregress(x, y)
    print(f"Line {label} Slope: {toScientific(slope)} Coef. Determination: {toScientific(rvalue**2)} Intercept: {toScientific(intercept)}")
    ax.plot(x, slope * x + intercept, label=f'{label} E:{toScientific(slope)} R2:{toScientific(rvalue**2)}', linestyle='--')
    
def toScientific(num, sigfigs: int = 3) -> str:
    string = f"{num :0.3g}"
    return string