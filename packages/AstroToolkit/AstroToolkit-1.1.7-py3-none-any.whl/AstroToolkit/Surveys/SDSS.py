from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy import units as u
from astroquery.vizier import Vizier
import astropy.coordinates as coord
import pandas as pd
from bokeh.plotting import figure
import astropy
import math

catalogue_name='V/154/sdss16'

Vizier.ROW_LIMIT = -1

'''
Fetches raw data given by SDSS
'''
def get_spectrum_data(ra,dec,radius):
	# sets up a skycoord object used in the search (basically just a pos)
	pos=coords.SkyCoord(ra,dec,unit='deg')
	radius=radius/3600*u.deg

	# fetches data
	data=SDSS.get_spectra(pos,radius)
	if data!=None:
		data=data[0][1]
	else:
		return None, None
	
	spectrum_data=data.data
	
	# formats the data
	log_wavelength=spectrum_data['loglam']
	wavelength=10**log_wavelength*u.AA
	flux=spectrum_data['flux']*10**-17*u.Unit('erg cm-2 s-1 AA-1')

	return wavelength,flux

'''
Creates the spectrum plot
'''
def get_plot(ra,dec,radius=3,save_data=False):
	x,y=get_spectrum_data(ra,dec,radius)

	# strip units
	raw_x=[]
	raw_y=[]
	if save_data==True:
		for i in range(0,len(x)):
			try:
				raw_x.append(x[i].value)
			except:
				raw_x.append(math.nan)
		for i in range(0,len(y)):
			try:
				raw_y.append(y[i].value)
			except:
				raw_y.append(math.nan)
		
		# turns data into a dataframe if it is needed for saving
		data=pd.DataFrame.from_dict({'wavelength [AA]':raw_x,'flux [ergcm-2s-1AA-1]':raw_y},orient='index').T

	if not isinstance(x,astropy.units.quantity.Quantity) or not isinstance(y,astropy.units.quantity.Quantity):
		if save_data==True:
			return None, None
		else:
			return None

	plot=figure(width=400,height=400,title="SDSS Spectrum",x_axis_label=r'\[\lambda\text{ }[\text{AA}]\]',y_axis_label=r"\[\text{flux [erg}\text{ cm }^{-2}\text{ s }^{-1}\text{AA}^{-1}]\]")
	plot.line(x,y,color='black',line_width=1)

	if save_data==True:
		return plot, data

	return plot

'''
Gets vizier data from SDSS (photometry etc.) by coordinates (pos)
'''
def get_data(ra,dec,radius=3):
	data=[]
	
	if not isinstance(radius,int) and not isinstance(radius,float):
		raise Exception('search radius must be a float or an integer')
	
	if not isinstance(ra,float):
		try:
			ra=float(ra)
		except:
			raise Exception('object RA must be a float or an integer')
	if not isinstance(dec,float):
		try:
			dec=float(dec)
		except:
			raise Exception('object DEC must be a float or an integer')
	
	# include all columns
	v=Vizier(columns=['**'])

	#Sends Vizier query, can return multiple objects in given search radius
	data.append(v.query_region(coord.SkyCoord(ra=ra,dec=dec,unit=(u.deg,u.deg),frame='icrs'),width=radius*u.arcsec,catalog=catalogue_name))
	if len(data[0])==0:
		print('[SDSS: get_data] Error: no SDSS data found at given coordinates')
		return None
	data=data[0][0].to_pandas()
	data=data.reset_index(drop=True)
	return data

'''
Gets SDSS photometry by coordinates (pos)
'''
def get_photometry(ra,dec,radius=3):
	SDSSdata=get_data(ra,dec,radius=radius)
	if not isinstance(SDSSdata,pd.DataFrame) or SDSSdata.empty:
		return None
	
	photometry=SDSSdata[['RA_ICRS','DE_ICRS','objID','uPmag','e_uPmag','gPmag','e_gPmag','rPmag','e_rPmag','iPmag','e_iPmag','zPmag','e_zPmag']].copy()

	return photometry