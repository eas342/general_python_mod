from contextlib import contextmanager
import os
import sys

@contextmanager
def suppress_stdout():
    ## Short little function from Jarron that allows you to ignore annoying output
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
			
            
def find_files(name,path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result, len(result)
    
#def find_startline():
    