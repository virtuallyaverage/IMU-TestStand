import csv
from tqdm import tqdm
import pandas as pd
from io import StringIO

def process_file(file_name: str, in_directory: str, in_format: str = ".bin", out_directory:str|None = None):
    """Processes file and places a csv formatted file next to original if no out_directory specified

    Args:
        file_name (str): file name (no extension) (must be raw bytes)
        in_directory (str): in_directory containing files
    """
    raw_directory = in_directory + "\\" + file_name + in_format
    
    if out_directory == None: #if we are given out directory handle accordingly
        finished_directory = in_directory + "\\" + file_name + ".csv"
    else:
        finished_directory = out_directory+ "\\" + file_name + ".csv"
        
    with open(raw_directory, 'rb') as f:
        data = f.read()

    phrase = b"Begin\n"
    data = data[data.find(phrase)+phrase.__len__()::] # trim data to useful portion

    data_str = data.decode('utf-8')
    lines = data_str.split('\n')[:-1] # drop last nan 

    #resave csv file
    with open(finished_directory, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in tqdm(lines):
            writer.writerow(line[:-1].split(',')) # drop exta row
            
def get_dataframe(directory, file_name):
    return pd.read_csv(StringIO(open_csv(directory, file_name)))
          
def open_csv(directory, file_name):
    with (open(directory+"\\"+file_name+".csv", 'r')) as file:
        return file.read()    

if __name__ == "__main__":
    file_name = "v1"
    in_directory = r"data\bmi270\static"
    
    process_file(file_name, in_directory)