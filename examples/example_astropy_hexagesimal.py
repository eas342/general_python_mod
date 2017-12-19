
# coding: utf-8

# ## Example Astropy Conversion from Decimal to Hexagismal

# In[1]:

from astropy import units as u
from astropy.coordinates import SkyCoord


# In[2]:

c1 = SkyCoord(082.563716 * u.deg,62.893349 * u.deg)


# In[3]:

print(c1.ra.to_string(u.hour), c1.dec.to_string(u.deg))


# In[ ]:



