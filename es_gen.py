from contextlib import contextmanager
import os
import sys
import pdb
import numpy as np
import fnmatch
import warnings
from scipy.interpolate import UnivariateSpline, LSQUnivariateSpline

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

def search_file(fileName,phrase,occurence=1,zeroBased=False,skipBlank=False):
    """ Searches a file for the Nth occurence of a phrase 
    
    
    Arguments
    ----------
    fileName: str
        File name
    phrase: str
        Text to search for
    occurrence: int
        The Nth occrence to return the line number
    zeroBased: bool, optional
        Use zero-based counting if True, It uses one-based counting by default.
    """
    if zeroBased == True:
        adjustment=0
    else: adjustment = 1
    
    counter = 1
    isFound = False
    with open(fileName) as f:
        for i, line in enumerate(f):
            if phrase in line:
                if counter == occurence:
                    isFound = True
                    return i + adjustment
                    break
                counter = counter + 1
    if isFound == False:
        print('Phrase '+phrase+' not found')
        return -1

def read_one_line(fileName,lineNumber,zeroBased=False):
    """ Reads one line from a file, inspired by 
    (http://stackoverflow.com/questions/2081836/reading-specific-lines-only-python)
    
    Arguments
    ----------
    filename: str
        File name
    lineNumber: int
        number of the line
    zeroBased: bool, optional
        Use zero-based counting if True, It uses one-based counting by default.
    """
    if zeroBased == True:
        adjustment=0
    else: adjustment = 1
    
    with open(fileName) as f:
        for i, line in enumerate(f):
            if i == lineNumber-adjustment:
                return line
                break
    

def es_strmatch(text,list):
## Searches the list for text (with wildcards)    
## Returns the indices where it was found
    
    foundind = []
    for ind, item in enumerate(list):
        if fnmatch.fnmatch(item,text):
            foundind.append(ind)
    return foundind

def robust_poly(x,y,polyord,sigreject=3.0,iteration=3,useSpline=False,knots=None):
    finitep = np.isfinite(y) & np.isfinite(x)
    goodp = finitep ## Start with the finite points
    for iter in range(iteration):
        if np.sum(goodp) < polyord:
            warntext = "Less than "+str(polyord)+"points accepted, returning flat line"
            warnings.warn(warntext)
            coeff = np.zeros(polyord)
            coeff[0] = 1.0
        else:
            if useSpline == True:
                if knots is None:
                    spl = UnivariateSpline(x[goodp], y[goodp], k=polyord, s=sSpline)
                else:
                    spl = LSQUnivariateSpline(x[goodp], y[goodp], knots, k=polyord)
                ymod = spl(x)
            else:
                coeff = np.polyfit(x[goodp],y[goodp],polyord)
                yPoly = np.poly1d(coeff)
                ymod = yPoly(x)
            
            resid = np.abs(ymod - y)
            madev = np.nanmedian(np.abs(resid - np.nanmedian(resid)))
            goodp = (np.abs(resid) < (sigreject * madev))
    
    if useSpline == True:
        return spl
    else:
        return coeff

