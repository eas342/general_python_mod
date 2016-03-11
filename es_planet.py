from astropy import units as u
from astropy import constants as const
from astropy.units import cds
cds.enable()
import time
import numpy as np
import yaml
import pdb


def calc_t14():
	"""
	This function calculates the expected duration. Useful when it's not specified and the Rp/R* ratio isn't given
	"""
	pp = yaml.load(open('params/planet_duration_p.yaml'))
	## From Seager & , 2013
	## http://seagerexoplanets.mit.edu/ftp/Papers/Seager2003.pdf
	## Equation 3
	k = float((pp['radius (Rearth)'] * cds.Rgeo / (pp['Rstar (Rsun)'] * cds.Rsun)).si)
	incrad = pp['Incl (deg)'] * np.pi/180.
	arg = np.sqrt(((1. + k)**2 - (pp['a/Rstar'] * np.cos(incrad))**2)/(1. - np.cos(incrad)**2)) / pp['a/Rstar']
	tdur_day = (pp['P (days)'] / np.pi) * np.arcsin(arg)
	tdur_hr = tdur_day * 24.
	
	print 'Duration (hours)= '+str(tdur_hr)
