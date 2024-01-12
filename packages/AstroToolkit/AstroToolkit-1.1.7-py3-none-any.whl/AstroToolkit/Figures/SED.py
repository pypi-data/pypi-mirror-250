from ssl import cert_time_to_seconds
import astropy.units as u
import math
import pandas as pd
import matplotlib
import numpy as np
from bokeh.plotting import figure,show
from bokeh.models import Whisker, ColumnDataSource

from ..Surveys.Gaia import GaiaQuerySource
from ..Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
from ..Surveys.SDSS import get_photometry as get_phot_sdss
from ..Surveys.WISE import get_photometry as get_phot_wise
from ..Surveys.TWOMASS import get_photometry as get_phot_twomass
from ..Surveys.Gaia import GaiaGetPhotometryCoords
from ..Surveys.GALEX import GALEXGetPhotometryCoords
from ..Surveys.PanSTARRS import PanSTARRSGetPhotometryCoords
from ..Surveys.SkyMapper import SkyMapperGetPhotometryCoords

# used to calculate fluxes using zero point, mag and wavelength of filter
def zeropoint(mag,zp,wl):
	flux=zp*10**(-0.4*mag)
	c=2.988*10**18
	fnl=1*10**(-23)
	flux=flux/((fnl*c)/wl**2)*1000
	return flux

def get_plot(source=None,pos=None,radius=3,save_data=False):
	# proper motion corrects positions for use in each supported survey
	if source!=None:
		gaia_data=GaiaQuerySource(source=source)
		ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		
		pos_corrected=CorrectPM([2016,0],[2012,0],ra,dec,pmra,pmdec)
		ra_panstarrs,dec_panstarrs=pos_corrected[0],pos_corrected[1]
		
		pos_corrected=CorrectPM([2016,0],[2016,0],ra,dec,pmra,pmdec)
		ra_skymapper,dec_skymapper=pos_corrected[0],pos_corrected[1]
		
		ra_gaia,dec_gaia=ra,dec
		
		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra_galex,dec_galex=pos_corrected[0],pos_corrected[1]
		
		pos_corrected=CorrectPM([2016,0],[1991,0],ra,dec,pmra,pmdec)
		ra_rosat,dec_rosat=pos_corrected[0],pos_corrected[1]
		
		pos_corrected=CorrectPM([2016,0],[2017,0],ra,dec,pmra,pmdec)
		ra_sdss,dec_sdss=pos_corrected[0],pos_corrected[1]
		
		pos_corrected=CorrectPM([2016,0],[2010,5],ra,dec,pmra,pmdec)
		ra_wise,dec_wise=pos_corrected[0],pos_corrected[1]
		
		pos_corrected=CorrectPM([2016,0],[1999,0],ra,dec,pmra,pmdec)
		ra_twomass,dec_twomass=pos_corrected[0],pos_corrected[1]
		
	elif pos!=None:
		ra_panstarrs,dec_panstarrs=pos[0],pos[1]
		ra_skymapper,dec_skymapper=pos[0],pos[1]
		ra_gaia,dec_gaia=pos[0],pos[1]
		ra_galex,dec_galex=pos[0],pos[1]
		ra_rosat,dec_rosat=pos[0],pos[1]
		ra_sdss,dec_sdss=pos[0],pos[1]
		ra_wise,dec_wise=pos[0],pos[1]
		ra_twomass,dec_twomass=pos[0],pos[1]
	
	filter_arr=[]
	
	error_arr=[]
	wavelength_arr=[]
	flux_arr=[]
	mag_arr=[]
	
	'''
	wavelength_arr = list of lists with wavelengths of each filter in a survey, i.e. [[gaia_g,gaia_r,gaia_i],[galex_nuv,galex_fuv] ... etc.]
	flux = same as above but with the corresponding fluxes
	error_arr = same as above but with the corresponding flux errors
	mag_arr = same as above but with the object's magnitudes through these filters, used to calculate the fluxes
	
	The functionality is the same for each survey, so I probably need to try and parameterise this at some point
	'''

	wavelengths=[]
	flux=[]
	errors=[]
	mags=[]
	# Get survey photometry
	photometry=GaiaGetPhotometryCoords(ra_gaia,dec_gaia,radius=radius)
	if isinstance(photometry,pd.DataFrame):
		# names of filters and errors in survey
		filter_list=['phot_g_mean_mag','phot_rp_mean_mag','phot_bp_mean_mag']
		error_list=['phot_g_mean_mag_error','phot_rp_mean_mag_error','phot_bp_mean_mag_error']
		# zero points of filters
		zero_points=[2.5e-9,1.24e-9,4.11e-9]

		#g,rp,bp
		filter_ref=[5850.88,7690.74,5041.61]
		
		# iterates through filter_list,error_list,zero_points simultaneously
		for filter, error, zp in zip(filter_list,error_list,zero_points):
			try:
				# gets magnitude value in current filter
				mag=photometry._get_value(0,filter)
				mags.append(mag)

				# gets error value for this magnitude
				errors.append((photometry._get_value(0,error)*u.ABmag))
				# gets the wavelength of the current filter
				wavelength=(filter_ref[filter_list.index(filter)])
				wavelengths.append(wavelength)

				# calculates the flux using the current filter's zero point
				fl=zeropoint(mag=mag,zp=zp,wl=wavelength)
				flux.append(fl)

				# appends the filter's name to filter_arr if this was all successful
				filter_arr.append(filter)
			except:
				pass
	
	# Appends the obtained values to the data arrays (see above)
	wavelength_arr.append(wavelengths)
	flux_arr.append(flux)
	error_arr.append(errors)
	mag_arr.append(mags)

	# These are only temporary arrays used in each survey, so here they get over-written. The functionality is then the same for all future surveys, except filter zero points are calculated manually.
	wavelengths=[]
	flux=[]
	errors=[]
	mags=[]
	photometry=GALEXGetPhotometryCoords(ra_galex,dec_galex,radius=radius)
	if isinstance(photometry,pd.DataFrame):
		filter_list=['NUVmag','FUVmag']
		error_list=['e_NUVmag','e_FUVmag']

		#nuv,fuv
		filter_ref=[2303.37,1548.85]
		
		for filter,error in zip(filter_list,error_list):
			try:
				mag=photometry._get_value(0,filter)
				mags.append(mag)
				
				errors.append((photometry._get_value(0,error)*u.ABmag))
				wavelength=(filter_ref[filter_list.index(filter)])
				wavelengths.append(wavelength)
				
				# calculate zero point of current filter manually
				zp=10**((5*np.log10(filter_ref[filter_list.index(filter)])+2.406)/-2.5)
				fl=zeropoint(mag=mag,zp=zp,wl=wavelength)
				flux.append(fl)
					
				filter_arr.append(filter)
			except:
				pass
	wavelength_arr.append(wavelengths)
	flux_arr.append(flux)
	error_arr.append(errors)
	mag_arr.append(mags)

	wavelengths=[]
	flux=[]
	errors=[]
	mags=[]
	photometry=PanSTARRSGetPhotometryCoords(ra_panstarrs,dec_panstarrs,radius=radius)
	if isinstance(photometry,pd.DataFrame):
		filter_list=['gMeanPSFMag','rMeanPSFMag','iMeanPSFMag','zMeanPSFMag','yMeanPSFMag']
		error_list=['gMeanPSFMagErr','rMeanPSFMagErr','iMeanPSFMagErr','zMeanPSFMagErr','yMeanPSFMagErr']

		#g,r,i,z,y
		filter_ref=[4810.16,6155.47,7503.03,8668.36,9613.60]
		
		for filter,error in zip(filter_list,error_list):
			try:
				mag=photometry._get_value(0,filter)
				mags.append(mag)
				
				errors.append((photometry._get_value(0,error)*u.ABmag))
				wavelength=(filter_ref[filter_list.index(filter)])
				wavelengths.append(wavelength)
					
				zp=10**((5*np.log10(filter_ref[filter_list.index(filter)])+2.406)/-2.5)
				fl=zeropoint(mag=mag,zp=zp,wl=wavelength)
				flux.append(fl)
					
				filter_arr.append(filter)
			except:
				pass
	wavelength_arr.append(wavelengths)
	flux_arr.append(flux)
	error_arr.append(errors)
	mag_arr.append(mags)

	wavelengths=[]
	flux=[]
	errors=[]
	mags=[]
	photometry=SkyMapperGetPhotometryCoords(ra_skymapper,dec_skymapper,radius=radius)
	if isinstance(photometry,pd.DataFrame):
		filter_list=['g_psf','r_psf','i_psf','z_psf','u_psf','v_psf']
		error_list=['e_g_psf','e_r_psf','e_i_psf','e_z_psf','e_u_psf','e_v_psf']		

		#g,r,i,z,u,v
		filter_ref=[5016.05,6076.85,6076.85,9120.25,3500.22,3878.68]
		
		for filter,error in zip(filter_list,error_list):
			try:
				mag=photometry._get_value(0,filter)
				mags.append(mag)
				
				errors.append((photometry._get_value(0,error)*u.ABmag))
				wavelength=(filter_ref[filter_list.index(filter)])
				wavelengths.append(wavelength)
					
				zp=10**((5*np.log10(filter_ref[filter_list.index(filter)])+2.406)/-2.5)
				fl=zeropoint(mag=mag,zp=zp,wl=wavelength)
				flux.append(fl)
					
				filter_arr.append(filter)
			except:
				pass
	wavelength_arr.append(wavelengths)
	flux_arr.append(flux)
	error_arr.append(errors)
	mag_arr.append(mags)

	wavelengths=[]
	flux=[]
	errors=[]
	mags=[]
	photometry=get_phot_sdss(ra_sdss,dec_sdss,radius=radius)
	if isinstance(photometry,pd.DataFrame):
		filter_list=['uPmag','gPmag','rPmag','iPmag','zPmag']
		error_list=['e_uPmag','e_gPmag','e_rPmag','e_iPmag','e_zPmag']		
	
		#u,g,r,i,z
		filter_ref=[3608.04,4671.78,6141.12,7457.89,8922.78]
		
		for filter,error in zip(filter_list,error_list):
			try:
				mag=photometry._get_value(0,filter)
				mags.append(mag)
				
				errors.append((photometry._get_value(0,error)*u.ABmag))
				wavelength=(filter_ref[filter_list.index(filter)])
				wavelengths.append(wavelength)
					
				zp=10**((5*np.log10(filter_ref[filter_list.index(filter)])+2.406)/-2.5)
				fl=zeropoint(mag=mag,zp=zp,wl=wavelength)
				flux.append(fl)
					
				filter_arr.append(filter)
			except:
				pass
	wavelength_arr.append(wavelengths)
	flux_arr.append(flux)
	error_arr.append(errors)
	mag_arr.append(mags)

	wavelengths=[]
	flux=[]
	errors=[]
	mags=[]
	photometry=get_phot_wise(ra_wise,dec_wise,radius=radius)
	if isinstance(photometry,pd.DataFrame):
		filter_list=['W1mag','W2mag','W3mag','W4mag']
		error_list=['e_W1mag','e_W2mag','e_W3mag','e_W4mag']

		#w1,w2,w3,w4
		filter_ref=[33526.00,46028.00,115608.00,220883.00]
		
		for filter,error in zip(filter_list,error_list):
			try:
				mag=photometry._get_value(0,filter)
				mags.append(mag)
				
				errors.append((photometry._get_value(0,error)*u.ABmag))
				wavelength=(filter_ref[filter_list.index(filter)])
				wavelengths.append(wavelength)
					
				zp=10**((5*np.log10(filter_ref[filter_list.index(filter)])+2.406)/-2.5)
				fl=zeropoint(mag=mag,zp=zp,wl=wavelength)
				flux.append(fl)
					
				filter_arr.append(filter)
			except:
				pass
	wavelength_arr.append(wavelengths)
	flux_arr.append(flux)
	error_arr.append(errors)
	mag_arr.append(mags)

	wavelengths=[]
	flux=[]
	errors=[]
	mags=[]
	photometry=get_phot_twomass(ra_twomass,dec_twomass,radius=radius)
	if isinstance(photometry,pd.DataFrame):
		filter_list=['Jmag','Hmag','Kmag']
		error_list=['e_Jmag','e_Hmag','e_Kmag']
		
		#j,h,k
		filter_ref=[12350.00,16620.00,21590.00]

		for filter,error in zip(filter_list,error_list):
			try:
				mag=photometry._get_value(0,filter)
				mags.append(mag)
				
				errors.append((photometry._get_value(0,error)*u.ABmag))
				wavelength=(filter_ref[filter_list.index(filter)])
				wavelengths.append(wavelength)
					
				zp=10**((5*np.log10(filter_ref[filter_list.index(filter)])+2.406)/-2.5)
				fl=zeropoint(mag=mag,zp=zp,wl=wavelength)
				flux.append(fl)
					
				filter_arr.append(filter)
			except:
				pass
	wavelength_arr.append(wavelengths)
	flux_arr.append(flux)
	error_arr.append(errors)
	mag_arr.append(mags)

	# strip all data of its units if it has any
	for i in range(0,len(flux_arr)):
		for j in range(0,len(flux_arr[i])):
			try:
				flux_arr[i][j]=flux_arr[i][j].value
			except:
				pass
	for i in range(0,len(error_arr)):
		for j in range(0,len(error_arr[i])):
			error_arr[i][j]=error_arr[i][j].value

	# calculate an array of relative errors from error values (cannot directly calculate errors using error propagation due to quirks of magnitude system (i.e. logarithmic and decreasing >> brighter))
	rel_error_arr=[]
	for i in range(0,len(mag_arr)):	
		flux_arr[i]=np.asarray(flux_arr[i])
		error_arr[i]=np.asarray(error_arr[i])
		mag_arr[i]=np.asarray(mag_arr[i])		

		rel_error_arr.append(flux_arr[i]*error_arr[i]/mag_arr[i])

	# if no data, return None
	if len(wavelength_arr)==0 and len(flux_arr)==0:
		if save_data==True:
			return None, None
		else:
			return None
	
	#Order on plot: GALEX, SDSS, SkyMapper, PanSTARRS, Gaia, 2MASS, WISE
	#Order in script: Gaia, GALEX, PanSTARRS, SkyMapper, SDSS, WISE, 2MASS
	colour_arr=['springgreen','royalblue','gold','aquamarine','deepskyblue','orangered','orange']
	
	# Create figure object
	plot=figure(width=400,height=400,title='SED',x_axis_label=r'\[\lambda_{\text{eff}}\text{ }[\text{AA}]\]',y_axis_label=r'\[\text{flux [mJy]}\]',x_axis_type='log',y_axis_type="log")	

	# Bokeh only understands np nan values, so convert math.nan to np.nan
	for i in range(0,len(wavelength_arr)):
		wavelength_arr[i]=[np.nan if math.isnan(x) else x for x in wavelength_arr[i]]
		flux_arr[i]=[np.nan if math.isnan(x) else x for x in flux_arr[i]]
		rel_error_arr[i]=[np.nan if math.isnan(x) else x for x in rel_error_arr[i]]
	
	# create data sources used to create plots
	sources=[]
	for i in range(0,len(wavelength_arr)):
		upper=[x+e for x,e in zip(flux_arr[i],rel_error_arr[i])]
		lower=[x-e for x,e in zip(flux_arr[i],rel_error_arr[i])]		

		source=ColumnDataSource(data=dict(wavelength=wavelength_arr[i],flux=flux_arr[i],upper=upper,lower=lower))
		sources.append(source)

	surveys=['Gaia','GALEX','PanSTARRS','SkyMapper','SDSS','WISE','2MASS']

	# plot data points
	for i in range(0,len(wavelength_arr)):
		if len(flux_arr[i])>0:
			plot.circle(x='wavelength',y='flux',source=sources[i],color=colour_arr[i],legend_label=f'{surveys[i]}')
			# add errors (has to be handled separately in bokeh :/ )
			errors=Whisker(source=sources[i],base='wavelength',upper='upper',lower='lower',line_width=0.5,line_color=colour_arr[i])
			errors.upper_head.line_width,errors.lower_head.line_width=0.5,0.5
			errors.upper_head.size,errors.lower_head.size=3,3
			errors.upper_head.line_color,errors.lower_head.line_color=colour_arr[i],colour_arr[i]
			plot.add_layout(errors)
			
	# if saving data, flatten arrays to 1d (i.e. you lose information about which survey each point is obtained from, not ideal but cannot seem to write to .csv with different sized dataframes unless 
    # completely separating the data as with getbulkphot() etc, which is then going to annoying to handle. Can improve.
	if save_data==True:
		flat_flux=[]
		flat_wavelength=[]
		flat_error=[]
		for element in flux_arr:
			flat_flux.extend(element)
		for element in wavelength_arr:
			flat_wavelength.extend(element)
		for element in rel_error_arr:
			flat_error.extend(element)
		
		data={'flux [mJy]':flat_flux,'flux_err [mJy]':flat_error,'wavelength [AA]':flat_wavelength}
		df=pd.DataFrame.from_dict(data,orient='index').T
	
		return plot, df

	return plot