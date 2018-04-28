import sys
# coding: utf-8
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u

r = Simbad.query_object(sys.argv[1])

print(r)

c = SkyCoord(r['RA'],r['DEC'],unit=(u.hourangle,u.degree))

print(sys.argv)
print(c.to_string())
print("Ecliptic Coord:",c.barycentrictrueecliptic)
print("Galactic Coord=",c.galactic)
