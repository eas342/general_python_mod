from contextlib import contextmanager
import os
import sys
import pdb
import numpy as np
import fnmatch
import warnings

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
    
def es_strmatch(text,list):
## Searches the list for text (with wildcards)    
## Returns the indices where it was found
    
    foundind = []
    for ind, item in enumerate(list):
        if fnmatch.fnmatch(item,text):
            foundind.append(ind)
    return foundind

def robust_poly(x,y,polyord,sigreject=3.0,iteration=3):
    finitep = np.isfinite(y) & np.isfinite(x)
    goodp = finitep ## Start with the finite points
    for iter in range(iteration):
        if len(np.where(goodp)[0]) < polyord:
            warntext = "Less than "+str(polyord)+"points accepted, returning flat line"
            warnings.warn(warntext)
            coeff = np.zeros(polyord)
            coeff[0] = 1.0
        else:           
            coeff = np.polyfit(x[goodp],y[goodp],polyord)
            ymod = np.poly1d(coeff)
            resid = np.abs(ymod(x) - y)
            madev = np.nanmedian(np.abs(resid - np.nanmedian(resid)))
            goodp = (np.abs(resid) < (sigreject * madev))
    
        
    return coeff

