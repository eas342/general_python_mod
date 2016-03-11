import matplotlib.pyplot as plt
from astropy.io import fits
import pdb
import matplotlib
import numpy as np

def plot_spextool(filename):
    #Plots a spectrum output by spextool
    # Make a bigger font size
    matplotlib.rcParams.update({'font.size': 18})
    hdulist = fits.open(filename)

    head = hdulist[0].header
    a = hdulist[0].data

    plt.plot(a[0,:],a[1,:])

    if head['XUNITS'] == 'um':
        xunit = '$\mu$m'
    else:
        xunit = head['XUNITS']
      
    plt.xlabel('Wavelength ('+xunit+')')
    
    if head['YUNITS'] == 'ergss-1cm-2A-1':
        yunit = 'erg s$^{-1}$ cm$^{-2}$ $\AA^{-1}$'
    else:
        yunit = head['YUNITS']
  
    plt.ylabel('Flux ('+yunit+')')
    
    plt.tight_layout()
	
    plt.show()

def color_array(ncol):
	
	colcycle = np.array(['peru','brown','darkslategray','fuchsia','darkolivegreen',
		'indigo','darkgoldenrod'])
	navailable = len(colcycle)
	colorarr = colcycle[np.mod(np.arange(ncol),navailable)]
	return colorarr
	
	