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
    goodp = np.where(np.isfinite(y))
    for iter in range(iteration):
        if len(goodp[0]) < polyord:
            warntext = "Less than "+str(polyord)+"points accepted, returning flat line"
            warnings.warn(warntext)
            coeff = np.zeros(polyord)
            coeff[0] = 1.0
        else:           
            coeff = np.polyfit(x[goodp],y[goodp],polyord)
            ymod = np.poly1d(coeff)
            resid = np.abs(ymod(x) - y)
            madev = np.median(np.abs(resid - np.median(resid)))
            goodp = np.where(np.abs(resid) < (sigreject * madev))

        
    return coeff

def sigprint(number,nsig,dostop=False):
    """
    Returns a string with the given number of significant digits.
    For numbers >= 1e4, and less than 0.001, it does exponential notation
    This is almost what ":.3g".format(x) does, but in the case
    of '{:.3g}'.format(2189), we want 2190 not 2.19e3. Also in the case of
    '{:.3g}'.format(1), we want 1.00, not 1
    """
    
    if ((abs(number) >= 1e-3) and (abs(number) < 1e4)) or number ==0:
        place = decplace(number) - nsig + 1
        decval = 10**place
        outnum = np.round(np.float(number) / decval) * decval
        if place >= 0: place=0
        fmt='.'+str(int(abs(place)))+'f'
    else:
        stringnsig = str(int(nsig-1))
        fmt = '.'+stringnsig+'e'
        outnum=number
    wholefmt = "{0:"+fmt+"}"
    
    return wholefmt.format(outnum)

def decplace(number):
    """
    Finds the decimal place of the leading digit of a number. For 0, it assumes
    a value of 0 (the one's digit)
    """
    if number == 0:
        place = 0
    else:
        place = np.floor(np.log10(np.abs(number)))
    return place

def roundfromErr(number,error,numsigErr=2,simple=False):
    """
    Rounds a number appropriately from the error bars and returns a string.
    Example: roundval, rounderr = roundfromErr(123.441,12.447) gives
    123 and 12, for 123 +/- 12
    """
    ## Decimal place of last significant digit
    decplaceUse = decplace(error) + 1 - numsigErr
    numsigVal = decplace(number) - decplaceUse + 1
    if simple == True:
    ## This is a much simpler implementation taking advantage of g
        valuestring = ("{0:."+str(int(numsigVal))+"g}").format(number)
        errstring = ("{0:."+str(int(numsigErr))+"g}").format(error)
    else:
        valuestring = sigprint(number,numsigVal)
        errstring = sigprint(error,numsigErr)
    
    return valuestring, errstring
    