import os 
__version__ = '0.0.2'

def get_file_abs(path):
    paths = os.listdir(path)
    return [os.path.join(path,tmp) for tmp in paths] 