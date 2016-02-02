import matplotlib.pyplot as plt
from astropy.io import fits

def plot_spextool(filename):
    #Plots a spectrum output by spextool
    hdulist = fits.open(filename)
    
    