from contextlib import contextmanager
import os
import sys
import pdb

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
    
def find_startline(filename,phrase,skipblank=False,zerobased=False):
## Finds the starting line in a text file
## Useful when data starts after a specific line
## EXAMPLE
## headline = es_gen.find_startline(configfile,lookuptext,skipblank=True,zerobased=True)
## data = ascii.read(configfile,data_start=headline+2,header_start=headline)


    if zerobased:
        startnumber=0
    else:
        startnumber=1
    
    counter=startnumber
    with open(filename) as myFile:
        for num, line in enumerate(myFile,startnumber):
            if phrase in line:
                if skipblank:
                    linenum = counter
                else:
                    linenum = num
            if line != '\n': 
                counter=counter+1
           
    return linenum
    
