from bokeh.plotting import figure, output_file
from bokeh.layouts import gridplot, row, column
from bokeh.models import CustomJS, Button
from bokeh import events
from bokeh.layouts import layout
import pandas as pd
import numpy as np
import math

'''
Changelog:
- Added errors to SED (they were being calculated but were not added to the final plot)
- Added the readlocal() and plotdata() functions
- Added many more comments throughout source code

Known Issues:
- Detections at large distance from focus are slightly innacurate due to lack of projection support in Bokeh 
- Crashes (usually upon multiple consecutive executions) in timseries analysis tool

To Do:
- Clean up errors
- ADD UPPER LIMITS TO SED TOOL + Check issues with plotting
- Could add an errors log which saves any errors experienced during a datapage/figure's creation
'''

# File handling -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Used for saving data (using the save_data parameter), does the actual saving of data to a file
'''
def savefile(data,identifier,extension='csv',pos=None,source=None):
	# Sort between pos and source input
	if pos!=None:
		file_name=getfilename(identifier=identifier,extension=extension,pos=pos)
	elif source!=None:
		file_name=getfilename(identifier=identifier,extension=extension,source=source)
	
	# Check file extension, don't include pandas dataframe index
	if extension=='csv':
		data.to_csv(file_name,index=False)

'''
Used for saving data (using the save_data parameter), generates the file path and name to pass to save_file()
'''
def getfilename(identifier,extension,pos=None,source=None):
	import os
	
	# middle_str is the pos coordinates, i.e. ra_dec
	if pos!=None:
		middle_str=f'{pos[0]}_{pos[1]}'
		
		file_name=f'{middle_str}_{identifier}.{extension}'
	
	# prefix_str is J... name, middle_str is the Gaia source_id
	elif source!=None:
		prefix_str=convertsource(source=source)
		middle_str=str(source)
		
		file_name=f'{prefix_str}_{middle_str}_{identifier}.{extension}'

	# get working directory and append the file_name to this so that it is saved in location of whatever script is using the tools
	file_name=os.path.join(os.getcwd(),file_name)

	return file_name

'''
Used to convert Gaia source_id into a J... identifier (really just grabs ra,dec,pmra,pmdec from a Gaia search for this source_id and then proper motion corrects and uses convertpos() below.)
'''
def convertsource(source):
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	# Get Gaia data
	gaia_data=gaiaquery(source=source)

	ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
	pos=[ra,dec]
	
	# Correct proper motion to epoch of 2000 used for coordinates. Gaia coordinates are already in ICRS frame of reference so don't need to do anything here.
	pos=CorrectPM([2016,0],[2000,0],ra,dec,pmra,pmdec)

	# Use convertpos() with the corrected object coordinates
	ObjRef=convertpos(pos=pos)
	
	return ObjRef

'''
Used to convert object coordinates into a J... identifier (not really for use outside of convertsource(), as these identifiers don't have a clear definition outside of a reference Gaia source_id.)
'''
def convertpos(pos):
	from astropy.coordinates import Angle
	from astropy import units as u

	# Check for a negative declination, only used to later make sure correct signs are shown in the resulting identifier
	ra,dec=pos[0],pos[1]
	if dec<0:
		negativeDec=True
	else:
		negativeDec=False

	ra=Angle(ra,u.degree)
	dec=Angle(dec,u.degree)
	
	# Do unit conversion from deg --> hms/dms
	ra=ra.hms
	dec=dec.dms
	
	# Create ra_arr and dec_arr containing [H,M,S] and [D,M,S]
	ra_arr=np.array([0,0,0],dtype=float)
	dec_arr=np.array([0,0,0],dtype=float)		

	ra_arr[0]=ra[0]
	ra_arr[1]=ra[1]
	ra_arr[2]=ra[2]

	dec_arr[0]=dec[0]
	dec_arr[1]=dec[1]
	dec_arr[2]=dec[2]

	# Convert all negative values to positive (if declination is positive, this is fixed later), this stops the identifier looking like: J...-D-M-S
	ra_str_arr=[]
	for element in ra_arr:
		if element<0:
			element=element*-1

		# Will only retain the SS part from final iteration (which is the only bit you need, since this is the final remainder at the end)
		ra_remainder=element-int(element)		

		element=int(element)
		element=str(element).zfill(2) # Force leading zeros to make each element 2 digits long
		ra_str_arr.append(element)

	# Do the same for dec
	dec_str_arr=[]
	for element in dec_arr:
		if element<0:
			element=element*-1
		
		dec_remainder=element-int(element)
		
		element=int(element)
		element=str(element).zfill(2)
		dec_str_arr.append(element)

	# Format remainder: force 2 decimal places, round to 2 decimal places and remove '0.'
	ra_str_arr[2]+=str('{:.2f}'.format(round(ra_remainder,2))[1:])
	dec_str_arr[2]+=str('{:.2f}'.format(round(dec_remainder,2))[1:])
	
	# Writes final identifier and takes account of negative decs.
	if negativeDec==True:
		objRef=f'J{ra_str_arr[0]}{ra_str_arr[1]}{ra_str_arr[2]}-{dec_str_arr[0]}{dec_str_arr[1]}{dec_str_arr[2]}'
	elif negativeDec==False:
		objRef=f'J{ra_str_arr[0]}{ra_str_arr[1]}{ra_str_arr[2]}+{dec_str_arr[0]}{dec_str_arr[1]}{dec_str_arr[2]}'
	else:
		print('objRef Error')
		return None
	
	return objRef

# Data Queries ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Perform a data query to PanSTARRS
'''
def panstarrsquery(source=None,pos=None,radius=3,save_data=False): # maybe have a keep_cols parameter?
	from .Surveys.PanSTARRS import PanSTARRSQueryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	if source!=None and pos!=None:
		raise Exception('[panstarrsquery]: simulatenous source and pos input detected')
	
	if source!=None:
		# get Gaia data and correct for proper motion to time of PanSTARRS
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2012,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[panstarrsquery]: either source or pos input required')

	# get PanSTARRS data
	data=PanSTARRSQueryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='PanSTARRS-Data',extension='csv',pos=pos,source=source)

	return data

'''
Perform a data query to SkyMapper
'''
def skymapperquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.SkyMapper import SkyMapperQueryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	if source!=None and pos!=None:
		raise Exception('[skymapperquery]: simulatenous source and pos input detected')
	
	# get Gaia data and correct for proper motion to time of SkyMapper
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2016,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[skymapperquery]: either source or pos input required')
	
	# get SkyMapper data
	data=SkyMapperQueryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='SkyMapper-Data',extension='csv',pos=pos,source=source)

	return data

'''
Perform a data query to Gaia
'''
def gaiaquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.Gaia import GaiaQuerySource
	from .Surveys.Gaia import GaiaQueryCoords

	if source!=None and pos!=None:
		raise Exception('[gaiaquery]: simulatenous source and pos input detected')
	
	# Don't need to do proper motion correction within Gaia
	if source!=None:
		data=GaiaQuerySource(source=source)
	elif pos!=None:
		ra,dec=pos[0],pos[1]
		data=GaiaQueryCoords(ra,dec)
	else:
		raise Exception('[gaiaquery]: either source or pos input required')
	
	if save_data==True:
		savefile(data=data,identifier='Gaia-Data',extension='csv',pos=pos,source=source)

	return data

'''
Perform a data query to GALEX
'''
def galexquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.GALEX import GALEXQueryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	if source!=None and pos!=None:
		raise Exception('[galexquery]: simulatenous source and pos input detected')
	
	# get Gaia data and correct for proper motion to time of GALEX
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[galexquery]: either source or pos input required')

	# get GALEX data
	data=GALEXQueryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='GALEX-Data',extension='csv',pos=pos,source=source)

	return data

'''
Perform a data query to ROSAT
'''
def rosatquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.ROSAT import ROSATQueryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	

	if source!=None and pos!=None:
		raise Exception('[rosatquery]: simulatenous source and pos input detected')
	
	# get Gaia data and correct for proper motion to time of ROSAT
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[1991,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[rosatquery]: either source or pos input required')
	
	# get ROSAT data
	data=ROSATQueryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='ROSAT-Data',extension='csv',pos=pos,source=source)
		
	return data

'''
Perform a data query to SDSS
'''
def sdssquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.SDSS import get_data
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	

	if source!=None and pos!=None:
		raise Exception('[sdssquery]: simulatenous source and pos input detected')
	
	# get Gaia data and correct for proper motion to time of SDSS
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2017,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[sdssquery]: either source or pos input required')
	
	# get SDSS data
	data=get_data(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='SDSS-Data',extension='csv',pos=pos,source=source)

	return data

'''
Perform a data query to WISE
'''
def wisequery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.WISE import get_data
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM		

	if source!=None and pos!=None:
		raise Exception('[wisequery]: simulatenous source and pos input detected')
	
	# get Gaia data and correct for proper motion to time of WISE
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2010,5],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[wisequery]: either source or pos input required')
	
	# get WISE data
	data=get_data(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='WISE-Data',extension='csv',pos=pos,source=source)

	return data

'''
Performs a data query to 2MASS, can't seem to use numbers in an import name :(
'''
def twomassquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.TWOMASS import get_data
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	
	
	if source!=None and pos!=None:
		raise Exception('[twomassquery]: simulatenous source and pos input detected')
	
	# get Gaia data and correct for proper motion to time of 2MASS
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2010,5],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None
		
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[twomassquery]: either source or pos input required')
	
	# get 2MASS data
	data=get_data(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='2MASS-Data',extension='csv',pos=pos,source=source)

	return data

# Imaging Queries ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Performs an imaging query to PanSTARRS
'''
def getpanstarrsimage(source=None,pos=None,image_size=30,band='g',overlay=['gaia'],get_time=False):
	from astropy.time import Time

	from .Surveys.PanSTARRS import get_info
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.PanSTARRS import get_plot
	from .Overlays.Overlay_Selection import overlaySelection

	if source!=None and pos!=None:
		raise Exception('[getpanstarrsimage]: simulatenous source and pos input detected')
	
	if source!=None:
		# Fetch coordinates and proper motion for object
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			if get_time==False:
				return None
			else:
				return None, None
		
		# Get an image and the time at which it was taken
		mjd=get_info(ra=ra,dec=dec,size=image_size,band=band)[1]
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		
		# Correct for proper motion to this image time
		pos_corrected=CorrectPM([2016,0],imageTime,ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	
	elif pos!=None:
		# No proper motion correction
		ra,dec=pos[0],pos[1]
		mjd=get_info(ra=ra,dec=dec,size=image_size,band=band)[1]
		
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
	else:
		raise Exception('[getpanstarrsimage]: either source or pos input required')
	
	# Fetch second (final) image using coordinates corrected to the time of the 1st image
	plot=get_plot(ra=ra,dec=dec,size=image_size,band=band)

	if plot==None:
		if get_time==False:
			return None
		else:
			return None, None

	# Get half image size (in deg, used for detection size scaling)
	border=image_size/7200

	# if using a source input, passing pmra and pmdec performs adaptive pm correction
	if source!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border,pmra,pmdec)
	elif pos!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border)
		
	# Only need a legend for overlays if any were found
	if plot!=None and detections_made!=False:
		plot.legend.click_policy="hide"	

		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js)  

	# rename output html files
	if source!=None:
		output_file(f'{source}_image.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_image.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_image.html")

	if get_time==True:
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		return plot, imageTime
	else:
		return plot

'''
Performs an imagine query to SkyMapper (see getpanstarrsimage for further comments, functioniality is the same)
'''
def getskymapperimage(source=None,pos=None,image_size=30,band='g',overlay=['gaia'],get_time=False):
	from astropy.time import Time
	
	from .Surveys.SkyMapper import get_info
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.SkyMapper import get_plot
	from .Overlays.Overlay_Selection import overlaySelection

	if source!=None and pos!=None:
		raise Exception('[getskymapperimage]: simulatenous source and pos input detected')
	
	if source!=None:
		# Fetch coordinates and proper motion for object
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			if get_time==False:
				return None
			else:
				return None, None

		# Get an image and get the time it was taken
		mjd=get_info(ra=ra,dec=dec,size=image_size,band=band)[1]
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		
		# Correct for proper motion to this image time
		pos_corrected=CorrectPM([2016,0],imageTime,ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	
	elif pos!=None:
		# No proper motion correction
		ra,dec=pos[0],pos[1]
		mjd=get_info(ra=ra,dec=dec,size=image_size,band=band)[1]
		
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
	else:
		raise Exception('[getskymapperimage]: either source or pos input required')
	
	# Fetch final image using coordinates corrected to the time of the original image
	plot=get_plot(ra=ra,dec=dec,size=image_size,band=band)

	if plot==None:
		if get_time==False:
			return None
		else:
			return None, None

	# Get half image size (in deg, used for detection size scaling)
	border=image_size/7200

	if source!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border,pmra,pmdec)
	elif pos!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border)
	
	
	if plot!=None and detections_made!=False:
		plot.legend.click_policy="hide"	

		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js)  

	if source!=None:
		output_file(f'{source}_image.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_image.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_image.html")

	if get_time==True:
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		return plot, imageTime
	else:
		return plot

'''
Performs an imaging query to DSS (see getpanstarrsimage for further comments, functionality is the same)
'''
def getdssimage(source=None,pos=None,image_size=30,overlay=['gaia'],get_time=False):
	from astropy.time import Time
	
	from .Surveys.DSS import get_info
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.DSS import get_plot
	from .Overlays.Overlay_Selection import overlaySelection

	if source!=None and pos!=None:
		raise Exception('[getdssimage]: simulatenous source and pos input detected')
	
	if source!=None:
		# Fetch coordinates and proper motion for object
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			if get_time==False:
				return None
			else:
				return None, None
		
		# Get an image and get the time it was taken
		mjd=get_info(ra=ra,dec=dec,size=image_size)[1]
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
			
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		
		# Correct for proper motion to this image time
		pos_corrected=CorrectPM([2016,0],imageTime,ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	
	elif pos!=None:
		# No proper motion correction
		ra,dec=pos[0],pos[1]
		mjd=get_info(ra=ra,dec=dec,size=image_size)[1]
			
		if mjd==None:
			if get_time==False:
				return None
			else:
				return None, None
	else:
		raise Exception('[getdssimage]: either source or pos input required')
	
	# Fetch final image using coordinates corrected to the time of the original image
	plot=get_plot(ra=ra,dec=dec,size=image_size)

	if plot==None:
		if get_time==False:
			return None
		else:
			return None, None

	# Get half image size (in deg, used for detection size scaling)
	border=image_size/7200

	if source!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border,pmra,pmdec)
	elif pos!=None:
		plot,detections_made=overlaySelection(plot,ra,dec,overlay,mjd,image_size,border)

	plot.legend.click_policy="hide"	

	if plot!=None and detections_made!=None:
		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js)  

	if source!=None:
		output_file(f'{source}_image.html')
	
	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_image.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_image.html")

	if get_time==True:
		imageTime=Time(mjd,format='mjd').to_datetime()
		imageTime=[imageTime.year,imageTime.month]
		return plot, imageTime
	else:
		return plot

# Exhaustitive imaging query ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Performs an imaging query to PanSTARRS/SkyMapper/DSS according to the hierarchy: PanSTARRS>SkyMapper>DSS
'''
def getimage(source=None,pos=None,image_size=30,overlay=['gaia'],get_time=False,band='g'):
	if source!=None and pos!=None:
		raise Exception('[getimage]: simulatenous source and pos input detected')	
	elif source==None and pos==None:
		raise Exception('[getimage]: either source or pos input required')	

	if source!=None and get_time==True:
		image_axis,image_time=getpanstarrsimage(source=source,get_time=True,band=band,overlay=overlay,image_size=image_size)
		if image_axis==None:
			image_axis,image_time=getskymapperimage(source=source,get_time=True,band=band,overlay=overlay,image_size=image_size)
			if image_axis==None:
				image_axis,image_time=getdssimage(source=source,get_time=True,overlay=overlay,image_size=image_size)
		
		return image_axis,image_time
	
	elif pos!=None and get_time==True:
		image_axis,image_time=getpanstarrsimage(pos=pos,get_time=True,band=band,overlay=overlay,image_size=image_size)
		if image_axis==None:
			image_axis,image_time=getskymapperimage(pos=pos,get_time=True,band=band,overlay=overlay,image_size=image_size)
			if image_axis==None:
				image_axis,image_time=getdssimage(pos=pos,get_time=True,overlay=overlay,image_size=image_size)
				
		return image_axis,image_time
	
	elif source!=None and get_time==False:
		image_axis=getpanstarrsimage(source=source,get_time=False,band=band,overlay=overlay,image_size=image_size)
		if image_axis==None:
			image_axis=getskymapperimage(source=source,get_time=False,band=band,overlay=overlay,image_size=image_size)
			if image_axis==None:
				image_axis=getdssimage(source=source,get_time=False,overlay=overlay,image_size=image_size)
				
		return image_axis
				
	elif pos!=None and get_time==False:
		image_axis=getpanstarrsimage(pos=pos,get_time=False,band=band,overlay=overlay,image_size=image_size)
		if image_axis==None:
			image_axis=getskymapperimage(pos=pos,get_time=False,band=band,overlay=overlay,image_size=image_size)
			if image_axis==None:
				image_axis=getdssimage(pos=pos,get_time=False,overlay=overlay,image_size=image_size)
		
		return image_axis
				
# Photometry Queries  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
These all act in the same way as data queries, just with all non-photometry data excluded so see these for comments.
'''

def getpanstarrsphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.PanSTARRS import PanSTARRSGetPhotometryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	

	if source!=None and pos!=None:
		raise Exception('[getpanstarrsphot]: simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None

		pos_corrected=CorrectPM([2016,0],[2012,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[getpanstarrsphot]: either source or pos input required')
		
	data=PanSTARRSGetPhotometryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='PanSTARRS-Phot',extension='csv',pos=pos,source=source)

	return data

def getskymapperphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.SkyMapper import SkyMapperGetPhotometryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	if source!=None and pos!=None:
		raise Exception('[getskymapperphot]: simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2016,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[getskymapperphot]: either source or pos input required')

	data=SkyMapperGetPhotometryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='SkyMapper-Phot',extension='csv',pos=pos,source=source)

	return data

def getgaiaphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.Gaia import GaiaGetPhotometryCoords
	from .Surveys.Gaia import GaiaGetPhotometrySource
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	if source!=None and pos!=None:
		raise Exception('[getgaiaphot]: simulatenous source and pos input detected')
	
	if source!=None:
		data=GaiaGetPhotometrySource(source=source)
	elif pos!=None:
		ra,dec=pos[0],pos[1]
		data=GaiaGetPhotometryCoords(ra,dec,radius)
	else:
		raise Exception('[getgaiaphot]: either source or pos input required')

	if save_data==True:
		savefile(data=data,identifier='Gaia-Phot',extension='csv',pos=pos,source=source)

	return data

def getgalexphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.GALEX import GALEXGetPhotometryCoords
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	if source!=None and pos!=None:
		raise Exception('[getgalexphot]: simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None

		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[getgalexphot]: either source or pos input required')

	data=GALEXGetPhotometryCoords(ra,dec,radius)
	
	if save_data==True:
		savefile(data=data,identifier='GALEX-Phot',extension='csv',pos=pos,source=source)

	return data

def getsdssphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.SDSS import get_photometry
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	

	if source!=None and pos!=None:
		raise Exception('[getsdssphot]: simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[getsdssphot]: either source or pos input required')
	
	data=get_photometry(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='SDSS-Phot',extension='csv',pos=pos,source=source)

	return data

def getwisephot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.WISE import get_photometry
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	
	
	if source!=None and pos!=None:
		raise Exception('[getwisephot]: simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[getwisephot]: either source or pos input required')
	
	data=get_photometry(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='WISE-Phot',extension='csv',pos=pos,source=source)

	return data

def gettwomassphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.TWOMASS import get_photometry
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM	
	
	if source!=None and pos!=None:
		raise Exception('[gettwomassphot]: simulatenous source and pos input detected')
	
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2007,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[gettwomassphot]: either source or pos input required')
	
	data=get_photometry(ra=ra,dec=dec,radius=radius)
	
	if save_data==True:
		savefile(data=data,identifier='2MASS-Phot',extension='csv',pos=pos,source=source)

	return data

'''
Didn't include a ROSAT option here since it doesn't seem to provide photometry similar to the other surveys (i.e. they are derived from elsewhere, etc.)
'''

# Bulk Photometry Query

'''
Basically just does all the photometry queries above and stitches them together in a single dictionary.
'''
def getbulkphot(radius=3,source=None,pos=None,save_data=False):
	from .Surveys.Gaia import GaiaGetPhotometryCoords
	from .Surveys.GALEX import GALEXGetPhotometryCoords
	from .Surveys.ROSAT import ROSATGetPhotometryCoords
	from .Surveys.PanSTARRS import PanSTARRSGetPhotometryCoords
	from .Surveys.SkyMapper import SkyMapperGetPhotometryCoords
	from .Surveys.SDSS import get_photometry as get_phot_sdss
	from .Surveys.WISE import get_photometry as get_phot_wise
	from .Surveys.TWOMASS import get_photometry as get_phot_twomass
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	
	if source!=None and pos!=None:
		raise Exception('[getbulkphot]: simulatenous source and pos input detected')
	
	# Correct for proper motion, and save as a set of coordinates for use in each photometry search (per-survey)
	if source!=None:		
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
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
		else:
			return None
		
	elif pos!=None:
		ra_panstarrs,dec_panstarrs=pos[0],pos[1]
		ra_skymapper,dec_skymapper=pos[0],pos[1]
		ra_gaia,dec_gaia=pos[0],pos[1]
		ra_galex,dec_galex=pos[0],pos[1]
		ra_rosat,dec_rosat=pos[0],pos[1]
		ra_sdss,dec_sdss=pos[0],pos[1]
		ra_wise,dec_wise=pos[0],pos[1]
		ra_twomass,dec_twomass=pos[0],pos[1]
		
	else:
		raise Exception('[getbulkphot]: either source or pos input required')

	# Make a dictionary with the surveys as keys
	photometry={'gaia':None,'galex':None,'rosat':None,'panstarrs':None,'skymapper':None,'sdss':None,'wise':None,'twomass':None}
	
	# Get photometry data from all supported surveys
	try:
		data=GaiaGetPhotometryCoords(ra_gaia,dec_gaia,radius)
		photometry['gaia']=data
	except:
		pass
	try:
		data=GALEXGetPhotometryCoords(ra_galex,dec_galex,radius)
		photometry['galex']=data
	except:
		pass
	try:
		data=ROSATGetPhotometryCoords(ra_rosat,dec_rosat,radius)
		photometry['rosat']=data
	except:
		pass
	try:
		data=PanSTARRSGetPhotometryCoords(ra_panstarrs,dec_panstarrs,radius)
		photometry['panstarrs']=data
	except:
		pass
	try:
		data=SkyMapperGetPhotometryCoords(ra_skymapper,dec_skymapper,radius)
		photometry['skymapper']=data
	except:
		pass
	try:
		data=get_phot_sdss(ra=ra_sdss,dec=dec_sdss,radius=radius)
		photometry['sdss']=data
	except:
		pass
	try:
		data=get_phot_wise(ra=ra_wise,dec=dec_wise,radius=radius)
		photometry['wise']=data
	except:
		pass
	try:
		data=get_phot_twomass(ra=ra_twomass,dec=dec_twomass,radius=radius)
		photometry['twomass']=data
	except:
		pass
	
	# Need to save data a bit differently here as there are multiple dataframes (one for each survey that returns data), this puts them all in one csv, separated by one empty row.
	if save_data==True:
		file_name=getfilename(identifier='BulkPhot',extension='csv',pos=pos,source=source)

		with open(file_name,'w') as f:
			for key in photometry:
				try:
					# add a column denoting the survey
					photometry[key].insert(0,'survey',key)
					photometry[key].to_csv(f,index=False,lineterminator='\n')
					
					f.write('\n')
				except:
					pass

	return photometry

# Timeseries Queries -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Performs a data query to ZTF
'''
def ztfquery(source=None,pos=None,radius=3,save_data=False):
	from .Surveys.ZTF import getData as getZTFData	
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	if source!=None and pos!=None:
		raise Exception('[ztfquery]: simulatenous source and pos input detected')
	
	# get Gaia data and correct to time of ZTF
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2019,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[ztfquery]: either source or pos input required')
	
	# get ZTF data
	data=getZTFData(ra,dec,radius)

	# Same as for getbulkphot (see above), need to save multiple dataframes so need to use a slightly different method for saving the data.
	if save_data==True:
		data_dict={'g':data[0],'r':data[1],'i':data[2]}

		file_name=getfilename(identifier='ZTF-Data',extension='csv',pos=pos,source=source)
		
		with open(file_name,'w') as f:
			for key in data_dict:
				try:
					data_dict[key].insert(0,'band',key)
					data_dict[key].to_csv(f,index=False,lineterminator='\n')
					
					f.write('\n')
				except:
					pass
					
	return data

# Timeseries Plotting ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Fetches ZTF light curves
'''
def getztflc(source=None,pos=None,radius=3,return_raw=False,save_data=False):
	from .Surveys.ZTF import getLightCurve as getZTFLightCurve
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.ZTF import getData

	if source!=None and pos!=None:
		raise Exception('[getztflc]: simulatenous source and pos input detected')
	
	# get Gaia data and correct to time of ZTF
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
			pos_corrected=CorrectPM([2016,0],[2019,0],ra,dec,pmra,pmdec)
			ra,dec=pos_corrected[0],pos_corrected[1]
		else:
			return None

	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[getztflc]: either source or pos input required')
	
	# get ZTF light curves (return_raw just tells it to return them as separate figure objects (i.e. don't combine them))
	plot=getZTFLightCurve(ra,dec,radius,return_raw)
	
	# change name of output html file
	if source!=None:
		output_file(f'{source}_lightcurve.html')
	
	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_lightcurve.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_lightcurve.html")
	
	# save data (as in ztfquery() and getbulkphot())
	if save_data==True:
		data=getData(ra,dec,radius)
		
		data_dict={'g':data[0],'r':data[1],'i':data[2]}

		file_name=getfilename(identifier='ZTF-Data',extension='csv',pos=pos,source=source)
		
		with open(file_name,'w') as f:
			for key in data_dict:
				try:
					data_dict[key].insert(0,'band',key)
					data_dict[key].to_csv(f,index=False,lineterminator='\n')

					f.write('\n')
				except:
					pass

	return plot

# SED Plotting -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Creates an SED from photometry acquired from supported surveys (this is done in essentially the same way as getbulkphot(), but more handling done inside SED.py)
'''
def getsed(source=None,pos=None,radius=3,save_data=False):
	from .Figures.SED import get_plot
	
	if source!=None and pos!=None:
		raise Exception('[getsed]: simulatenous source and pos input detected')

	# get plot if not saving data, otherwise get plot and raw data  (after unit conversions which are performed within SED.py)
	if source!=None:
		if save_data==False:
			plot=get_plot(source=source,radius=radius)
		else:
			plot,data=get_plot(source=source,radius=radius,save_data=True)
	elif pos!=None:
		if save_data==False:
			plot=get_plot(pos=pos,radius=radius)
		else:
			plot,data=get_plot(pos=pos,radius=radius,save_data=True)
	else:
		raise Exception('[getsed]: either source or pos input required')

	if plot!=None:
		plot.legend.click_policy="hide"	
		
		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js)  
	else:
		return None

	if source!=None:
		output_file(f'{source}_sed.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_sed.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_sed.html")
	
	if save_data==True:
		savefile(data=data,identifier='SED-Data',extension='csv',pos=pos,source=source)

	return plot

# Spectra Queries --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Fetches SDSS spectra
'''
def getsdssspectrum(source=None,pos=None,radius=3,save_data=False):
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM
	from .Surveys.SDSS import get_plot

	if source!=None and pos!=None:
		raise Exception('[getsdssspectrum]: simulatenous source and pos input detected')
	
	# get Gaia data and correct for proper motion to time of SDSS
	if source!=None:
		gaia_data=gaiaquery(source=source)
		if isinstance(gaia_data,pd.DataFrame):
			ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		else:
			return None
		
		pos_corrected=CorrectPM([2016,0],[2017,0],ra,dec,pmra,pmdec)
		ra,dec=pos_corrected[0],pos_corrected[1]
	elif pos!=None:
		ra,dec=pos[0],pos[1]
	else:
		raise Exception('[getsdssspectrum]: either source or pos input required')
	
	# same as for SEDs, return only plot if not saving data, otherwise return plot and the final data used to create it.
	if save_data==False:
		plot=get_plot(ra=ra,dec=dec,radius=radius)
	else:
		plot,data=get_plot(ra=ra,dec=dec,radius=radius,save_data=True)

	if source!=None:
		output_file(f'{source}_spectrum.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_spectrum.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_spectrum.html")
	
	if save_data==True:
		savefile(data=data,identifier='SDSS-Data',extension='csv',pos=pos,source=source)

	return plot

# HR diagram --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Creates a HRD using a background sample, allows for multiple sources to be used at once.
'''
def gethrd(source=None,sources=None):
	from .Figures.HRD import get_plot
	if source==None and sources==None:
		raise Exception('[gethrd]: source/sources input required')
	
	if source!=None:
		plot=get_plot(source=source)
	elif sources!=None:
		plot=get_plot(sources=sources)
	else:
		raise Exception('[gethrd]: source/sources input required.')
	
	if plot!=None:
		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js) 
	
	# names output html file for one or multiple sources
	if source!=None:
		output_file(f'{source}_hrd.html')
	elif sources==None:
		sources_str=''
		for i in range(0,len(sources)-1):
			sources_str.append(str(sources[i]))+','
		sources_str.append(source[len(source)-1])
		output_file(f'{sources}_hrd.html')

	return plot

# Timeseries analysis -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Uses timeseries tools to perform timeseries analysis on ztf data
'''
def getztfanalysis(source=None,pos=None):
	from .Timeseries.ztfanalysis import getanalysis
	
	if pos!=None:
		data=ztfquery(pos=pos)
	elif source!=None:
		data=ztfquery(source=source)
	else:
		raise Exception('[getztfanalysis]: either source or pos input required')

	# check for missing data in each of the 3 bands (g,r,i)
	empty_count=0
	for item in data:
		if not isinstance(item,pd.DataFrame):
			empty_count+=1
	
	# if no data, return none. Otherwise combine data
	if empty_count!=3:
		data=pd.concat(data)
	else:
		return None

	getanalysis(data)

def getps(source=None,pos=None,save_data=False):
	from .Timeseries.ztfanalysis import getpowerspectrum
	
	if pos!=None:
		data=ztfquery(pos=pos)
	elif source!=None:
		data=ztfquery(source=source)
	else:
		raise Exception('[getztfanalysis]: either source or pos input required')

	# check for missing data in each of the 3 bands (g,r,i)
	empty_count=0
	for item in data:
		if not isinstance(item,pd.DataFrame):
			empty_count+=1
	
	# if no data, return none. Otherwise combine data
	if empty_count!=3:
		data=pd.concat(data)
	else:
		return None	

	# same as for SEDs/SDSS spectra, get plot if not saving data, otherwise get plot and the raw data used to create it
	if save_data==True:
		plot,ps_data=getpowerspectrum(data,save_data=True)
	else:
		plot=getpowerspectrum(data)

	if source!=None:
		output_file(f'{source}_powspec.html')

	elif pos!=None:
		if pos[1]>=0:
			output_file(f"{pos[0]}+{pos[1]}_powspec.html")	
		else:
			output_file(f"{pos[0]}{pos[1]}_powspec.html")

	if save_data==True:
		savefile(data=ps_data,identifier='PS-Data',extension='csv',pos=pos,source=source)

	return plot

# Miscellaneous Tools -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Used to correct for proper motion
'''
def correctPM(input_time,target_time,ra,dec,pmra,pmdec,radius=None):
	from .Miscellaneous.ProperMotionCorrection import PMCorrection as CorrectPM

	data=CorrectPM(input_time,target_time,ra,dec,pmra,pmdec,radius)
	return data

'''
Used to convert a Gaia source_id to its coordinates
'''
def getgaiacoords(source):
	from .Surveys.Gaia import GaiaGetCoords
	
	data=GaiaGetCoords(source)
	return data

'''
Used to convert coordinates of an object to a Gaia source_id
'''
def getgaiasource(pos,radius=3):
	from .Surveys.Gaia import GaiaGetSource
	
	ra,dec=pos[0],pos[1]
	data=GaiaGetSource(ra,dec,radius)
	return data

'''
Used to read Gaia source_ids from a .fits file
'''
def getsources(file_name):
	from .Miscellaneous.ReadFits import get_source_list
	
	sources=get_source_list(file_name)
	return sources

'''
Used to read ra/dec from a .fits file
'''
def getpositions(file_name):
	from .Miscellaneous.ReadFits import get_pos_list
	pos_list=get_pos_list(file_name)
	return pos_list

'''
Used to create a spacial distribution given a .fits file with a set of ra/dec coordinates
'''
def getsd(file_name):
	from .Figures.SD import get_plot
	plot=get_plot(file_name)
	
	if plot!=None:
		# Double click to hide legend
		toggle_legend_js = CustomJS(args=dict(leg=plot.legend[0]), code='''
			 if (leg.visible) {
				 leg.visible = false
				 }
			 else {
				 leg.visible = true
			 }
		''')
	
		plot.js_on_event(events.DoubleTap, toggle_legend_js) 

	return plot

'''
Creates the SIMBAD and Vizier buttons (primarily for use in datapages)
'''
def getinfobuttons(grid_size,source=None,pos=None,simbad_radius=3,vizier_radius=3):
	button_width=round(grid_size/2)
	button_height=round(button_width/3)

	# SIMBAD button
	simbad_button = Button(label="SIMBAD",button_type='primary',height=button_height,width=button_width)	

	if pos!=None:
		ra,dec=pos[0],pos[1]
	elif source!=None:
		gaia_data=gaiaquery(source=source)
		ra,dec,pmra,pmdec=gaia_data['ra'].values[0],gaia_data['dec'].values[0],gaia_data['pmra'].values[0],gaia_data['pmdec'].values[0]
		
		# Scale search radius to include ~26 years of potential proper motion (don't actually correct coordinates, just give a buffer)
		_,_,simbad_radius=correctPM([2016,0],[1990,0],ra,dec,pmra,pmdec,simbad_radius)
		_,_,vizier_radius=correctPM([2016,0],[1990,0],ra,dec,pmra,pmdec,vizier_radius)
	
	# format URL that the button uses
	if pos!=None:
		simbad_url=f'https://simbad.cds.unistra.fr/simbad/sim-coo?Coord={ra}+{dec}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius={simbad_radius}&Radius.unit=arcsec&submit=submit+query&CoordList='
	elif source!=None:
		simbad_url=f'https://simbad.cds.unistra.fr/simbad/sim-coo?Coord={ra}+{dec}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&CooDefinedFrames=none&Radius={simbad_radius}&Radius.unit=arcsec&submit=submit+query&CoordList='
	
	# actual functionality on button click
	simbad_button_js = CustomJS(args=dict(url=simbad_url),code='''
		window.open(url)
	''')
	simbad_button.js_on_event('button_click',simbad_button_js)

	# Vizier button
	vizier_button = Button(label="Vizier",button_type='primary',height=button_height,width=button_width)	
	
	# format URL that the button uses
	if dec>=0:
		vizier_url=f'https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-c={ra}+{dec}&-c.rs={vizier_radius}&-out.add=_r&-sort=_r&-out.max=$4'
	else:
		vizier_url=f'https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-c={ra}{dec}&-c.rs={vizier_radius}&-out.add=_r&-sort=_r&-out.max=$4'
	
	# actual functionality on button click
	vizier_button_js = CustomJS(args=dict(url=vizier_url),code='''
		window.open(url)
	''')
	vizier_button.js_on_event('button_click',vizier_button_js)
	
	# Margin = [Top,Right,Bottom,Left]
	simbad_button.margin=[round(0.1*(grid_size-button_height)),round(1/4*grid_size),0,round(1/4*grid_size)]
	vizier_button.margin=[round(0.05*(grid_size-button_height)),round(1/4*grid_size),0,round(1/4*grid_size)]
	
	# combine both buttons into single column object
	buttons=column(simbad_button,vizier_button,align='center')
	
	return buttons

'''
Reads a local csv-esque data file (i.e. holds data in columns with a given separator) file into a 2D list of columns
'''
def readlocal(source=None,pos=None,extension='csv',headers=True,separator=',',getfilename=False):
	import glob
	import os

	# sets file names to search for. * indicates a wildcard string (i.e. can be anything)
	if source!=None:
		filename=f'*{str(source)}*.{extension}'
	elif source!=None:
		filename=f'*{str(pos[0])}_{str(pos[1])}.{extension}'

	# tells pandas whether to include headers
	if headers==False:
		headers=None
	else:
		headers='infer'
	
	# reads file into a dataframe
	for file_name in glob.glob(filename):
		data=pd.read_csv(os.path.join(os.getcwd(),file_name),header=headers,sep=separator)
	
	# separate columns into 2D list
	data_list=[]
	for column in data:
		data_list.append(data[column].tolist())
	
	# remove extension from file_name before returning
	if getfilename==True:
		file_name=file_name[:len(file_name)-len(extension)-1]
		return data_list,file_name
	else:
		return data_list
	
'''
plots data with very limited customizability, but is substantially easier than learning how to plot bokeh data from scratch.
'''
def plotdata(x,y,x_err=None,y_err=None,title=None,xlabel=None,ylabel=None,xtype='linear',ytype='linear',marker='circle',colour='black',legend='Data Points'):
	from bokeh.plotting import figure,show
	from bokeh.models import Whisker, ColumnDataSource

	# check if marker is supported
	if marker not in ['circle','line']:
		raise Exception('plotlocaldata only supports circle and line markers, for more customizable plotting see bokeh documentation and set up plot manually')

	# bokeh only supports np nan values, so swap math.nan for np.nan
	x=[np.nan if math.isnan(k) else k for k in x]
	y=[np.nan if math.isnan(k) else k for k in y]
	
	# if x_errors given, set up error bars
	if isinstance(x_err,list):
		x_err=[np.nan if math.isnan(k) else k for k in x_err]

		upper=[k+e for k,e in zip(x,x_err)]
		lower=[k-e for k,e in zip(x,x_err)]		

		x_errors=ColumnDataSource(data=dict(x=x,y=y,upper=upper,lower=lower))
		source=ColumnDataSource(data=dict(x=x,y=y))
	else:
		source=ColumnDataSource(data=dict(x=x,y=y))
	
	# if y_errors are given, set up error bars
	if isinstance(y_err,list):
		y_err=[np.nan if math.isnan(k) else k for k in y_err]
		
		upper=[k+e for k,e in zip(y,y_err)]
		lower=[k-e for k,e in zip(y,y_err)]		

		y_errors=ColumnDataSource(data=dict(x=x,y=y,upper=upper,lower=lower))
		source=ColumnDataSource(data=dict(x=x,y=y))
	else:
		source=ColumnDataSource(data=dict(x=x,y=y))
	
	# sets up figure
	plot=figure(width=400,height=400,title=title,x_axis_label=xlabel,y_axis_label=ylabel,x_axis_type=xtype,y_axis_type=ytype)	
	
	# plots data
	if marker=='circle':
		plot.circle(x='x',y='y',source=source,fill_color=colour,line_color=colour,legend_label=legend)
	elif marker=='line':
		plot.line(x='x',y='y',source=source,color=colour,line_width=1)
	
	# plots x_errors
	if isinstance(x_err,list):
		errors=Whisker(source=x_errors,base='y',upper='upper',lower='lower',line_width=0.5,line_color=colour,dimension='width')
		errors.upper_head.line_width,errors.lower_head.line_width=0.5,0.5
		errors.upper_head.size,errors.lower_head.size=3,3
		errors.upper_head.line_color,errors.lower_head.line_color=colour,colour
		plot.add_layout(errors)
		
	# plots y_errors
	if isinstance(y_err,list):
		errors=Whisker(source=y_errors,base='x',upper='upper',lower='lower',line_width=0.5,line_color=colour,dimension='width')
		errors.upper_head.line_width,errors.lower_head.line_width=0.5,0.5
		errors.upper_head.size,errors.lower_head.size=3,3
		errors.upper_head.line_color,errors.lower_head.line_color=colour,colour
		plot.add_layout(errors)
	
	return plot	

# Grid setup for datapage creation ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
Assists in the creation of a grid since I had such an awful time getting it to look reasonably neat, makes the process less painful
'''
def getgrid(dimensions,plots,grid_size=250):	
	for i in range(0,len(plots)):
		# Creates None objects to fill blank space since there cannot be anything that is empty.
		if plots[i][0]==None:
			plots[i][0]=figure(width=plots[i][1]*grid_size,height=plots[i][2]*grid_size)
		else:
			plots[i][0].width,plots[i][0].height=plots[i][1]*grid_size,plots[i][2]*grid_size
	
	# Checks the area occupied by the input plots (i.e. just normalized by /grid_size)
	unit_area=0
	for i in range(0,len(plots)):
		unit_area+=(plots[i][1]*plots[i][2])

	# Checks if the unit area calculated above matches the target unit area as given by the dimensions (i.e. all space must be filled)
	if unit_area!=dimensions[0]*dimensions[1]:
		raise Exception('Entire dimensions must be filled with figures. Pass None to fill empty space.')

	output_file('datapage.html')

	# Strips the plots of their dimensions etc.
	for i in range(0,len(plots)):
		plots[i]=plots[i][0]

	return plots