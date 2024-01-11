# Toolkit
Collection of tools for data fetching, plotting and analysis

## Installation

1. With pip, the package can be installed using:

```
pip install AstroToolkit
```

2. Once this has finished, you should navigate to the package location. This should be in a '.../Lib/site-packages/AstroToolkit' folder where ... is your python install location. If you wish to find this, you can can run the following commands:

```
python

from AstroToolkit.Tools import getztfanalysis
getztfanalysis(source=6050296829033196032)
```

As long as there are no issues with ZTF, this **should return an error** which will include the file path.

3. Navigate to this file in any terminal that can access your python environment, and run either buildwin.bat (windows) or build.sh (linux).

4. Re-run the above python commands and the error should no longer appear. The package is now fully installed.

***NOTE***: See README.txt (Linux) or README - Windows.txt (Windows) in the above directory for any additional dependencies.

## Usage

### 1. Bokeh

***NOTE:*** AstroToolkit uses Bokeh as its plotting library. The official documentation can be found at https://bokeh.org/. All plots will be saved as a static .html file, which can be opened in the browser (or from a python script using:

```
show(plot)
```

where 'plot' is the name of the parameter that the plot is assigned to.

***NOTE:*** All legends can be hidden/shown in plots by double clicking the figure. Individual legend elements can be hidden/shown by single clicking them in the legend.

### 2. Importing Tools

**All Tools in the package are located in AstroToolkit.Tools**

### 3. Input

***All Toolkit functions require atleast one input from:***
1. source = ...
   
where source is a Gaia source_id (string)

2. pos = ...

where pos is a 1D list with two elements: [ra,dec] in units of degrees

<br>

**For example:**

when trying to obtain a panstarrs image, there are therefore two options:

```
getpanstarrsimage(source=...)
````

and

```
getpanstarrsimage(pos=...)
```

The key difference between these input formats is the way that proper motion is handled. Given coordinates (pos), the results retrieved by any Toolkit function are simply the raw data obtained from that location
in the epoch of the survey in question, with no proper motion correction. The one exception for this is detection overlays in imaging functions, as these are still possible without an initial reference proper motion (i.e. a 
specific object in Gaia).

In contrast to this, any Toolkit functions called using a Gaia source_id as input will correct for any proper motion of that object between the time at which the data was taken and Gaia's epoch of Jan 2016, *pre-execution*. An
example of this difference is seen in imaging functions for objects with a large proper motion. Here, using a source as input will result in an image that is centred on the object, regardless of the magnitude of its
proper motion.

Using a position as input may still produce an image which contains the object, but it is unlikely to be centred as the focus of the image has not accounted for the proper motion of the object.


<br>

***Note:*** As the functions need to sort between the different input formats, explicit declaration is required, i.e.:

```
getpanstarrsimage(6050296829033196032)
```

will fail.

Instead, use:

```
getpanstarrsimage(source=6050296829033196032)
```

# Toolkit Functions

## save_data naming conventions
The 'save_data' parameter can be passed into most tools to export raw data to a .csv file. The naming convention for these files is as follows:

For 'pos' input:
```
ra_dec_identifier.csv
```
for 'source' input:
```
JHHMMSS.SS+DDMMSS.SS_source_identifier.csv
```
where 'identifier' gives a label to the data (e.g. 'ztflc' for ZTF light curves).

## Imaging functions

These functions produce images of objects from supported surveys.

***Note:*** When not using source mode, some detections can be missing for high proper motion objects. When using a source_id as input, this is no longer an issue as 'adaptive' proper motion correction is used. Here, the search radius for detections is increased to include the maximum distance that the object could have travelled in the gap between the epoch of the image and the epoch of the detection coordinates so that it is still picked up.

### 1. getpanstarrsimage
Retrieves Pan-STARRS image 

```
getpanstarrsimage(source=None,pos=None,image_size=30,band='g',overlay=['gaia'],get_time=False)
```

where:
```
source     = integer/string
           = Gaia source_id (e.g. 6050296829033196032).
```
```
pos        = 1D tuple of two integers
           = [ra,dec], object coordinates in degrees.
```
```
image_size = integer
           = size of image in arcseconds (maximum = 1500).
```
```
band       = string
           = list of all filters to include (e.g. for all filters, use band='grizy').
```
```
overlay    = 1D tuple of strings
           = for example, for Gaia and ZTF overlays, use overlay=['gaia','ztf']. Note, only supported for fits output_format.
```
```
get_time   = Bool
           = Returns Bokeh figure, image time in format [year,month]
```

returns: Bokeh figure or None (if no data retrieved).

### 2. getskymapperimage

```
getskymapperimage(source=None,pos=None,image_size=30,band='g',overlay=['gaia'],get_time=False)
```

where:
```
source     = integer/string
           = Gaia source_id (e.g. 6050296829033196032).
```
```
pos        = 1D tuple of two integers
           = [ra,dec], object coordinates in degrees.
```
```
image_size = integer
           = size of image in arcseconds (maximum = 1500).
```
```
band       = string
           = list of all filters to include (e.g. for all filters, use band='grizy').
```
```
overlay    = 1D tuple of strings
           = for example, for Gaia and ZTF overlays, use overlay=['gaia','ztf']. Note, only supported for fits output_format.
```
```
get_time   = Bool
           = Returns Bokeh figure, image time in format [year,month]
```

returns: Bokeh figure or None (if no data retrieved).

### 3. getdssimage

```
getdssimage(source=None,pos=None,image_size=30,overlay=['gaia'],get_time=False)
```

where:
```
source     = integer/string
           = Gaia source_id (e.g. 6050296829033196032).
```
```
pos        = 1D tuple of two integers
           = [ra,dec], object coordinates in degrees.
```
```
image_size = integer
           = size of image in arcseconds (maximum = 1500).
```
```
overlay    = 1D tuple of strings
           = for example, for Gaia and ZTF overlays, use overlay=['gaia','ztf']. Note, only supported for fits output_format.
```
```
get_time   = Bool
           = Returns Bokeh figure, image time in format [year,month]
```

returns: Bokeh figure or None (if no data retrieved).

### 4. getimage

Returns result of an exhaustitive image search (i.e. first searches PanSTARRS, if unsuccessful > searches SkyMapper, if unsuccessful > searches DSS)

```
getimage(source=None,pos=None,image_size=30,overlay=['gaia'],get_time=False,band='g')
```

where:
```
source     = integer/string
           = Gaia source_id (e.g. 6050296829033196032).
```
```
pos        = 1D tuple of two integers
           = [ra,dec], object coordinates in degrees.
```
```
image_size = integer
           = size of image in arcseconds (maximum = 1500).
```
```
band       = string
           = list of all filters to include (e.g. for all filters, use band='grizy').
```
```
overlay    = 1D tuple of strings
           = for example, for Gaia and ZTF overlays, use overlay=['gaia','ztf']. Note, only supported for fits output_format.
```
```
get_time   = Bool
           = Returns Bokeh figure, image time in format [year,month]
```

***NOTE:*** 'band' parameter has no effect on DSS as this only supports g band imaging.

returns: Bokeh figure or None (if no data retrieved).

## Data queries

These functions return all raw data retrieved from various surveys.

### 1. panstarrsquery

```
panstarrsquery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
	  = search radius of query in arcseconds.   
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 2. skymapperquery

```
skymapperquery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
    	  = search radius of query in arcseconds.   
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 3. gaiaquery

```
gaiaquery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.   
```
```
catalogue = string
          = 'dr2' or 'dr3'. Determines the data release from which the data is retrieved.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 4. galexquery

```
galexquery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.   
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 5. rosatquery

```
rosatquery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 6. ztfquery

```
ztfquery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 7. sdssquery

```
sdssquery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 8. wisequery

```
wisequery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 9. twomassquery

```
twomassquery(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).


## Photometry queries

These functions return only the photometry retrieved from various surveys.

### 1. getpanstarrsphot

```
getpanstarrsphot(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
  	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 2. getskymapperphot

```
getskymapperphot(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 3. getgaiaphot

```
getgaiaphot(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 4. getgalexphot

```
getgalexphot(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
 	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 5. getsdssphot

```
getsdssphot(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 6. getwisephot

```
getwisephot(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

### 7. gettwomassphot

```
gettwomassphot(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
 	  = saves raw data to a .csv file.
```

returns: pandas dataframe or None (if no data retrieved).

## Photometry bulk search

This function returns all retrieved photometry for all supported surveys for a given object.

### 1. getbulkphot

```
getbulkphot(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: dictionary in format: 'survey':pandas dataframe or None (if no data retrieved).

## Timeseries queries

These functions create light curves from supported surveys.

### 1. getztflc

```
getztflc(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: Bokeh figure or None (if no data retrieved).

## SED queries

This function creates a spectral energy distribution from all supported surveys.

### 1. getsed

```
getsed(source=None,pos=None,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: matplotlib axis or None (if no data retrieved).

## Spectra queries

These functions retrieve spectra from supported surveys.

### 1. getsdssspectrum

```
getsdssspectrum(source=None,pos=None,radius=3,save_data=False)
```

where:
```
source    = integer/string
          = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
radius    = integer
          = search radius of query in arcseconds.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: Bokeh figure or None (if no data retrieved).

## HR diagram function

### 1. gethrd

```
gethrd(source=None)
```

where:
```
source = integer/string
       = Gaia source_id (e.g. 6050296829033196032).
```

returns: Bokeh figure or None (if no data retrieved).

## Timeseries analysis tools

### 1. getztfanalysis

Allows for timeseries analysis of ZTF data for a given object.

```
getztfanalysis(source=None,pos=None)
```

where:
```
source = integer/string
       = Gaia source_id (e.g. 6050296829033196032).
```
```
pos    = 1D tuple of two integers
       = [ra,dec], object coordinates in degrees.
```

### 2. getps

Produces a power spectrum using ZTF data for a given object.

```
getps(source=None,pos=None,save_data=False)
```

where:
```
source    = integer/string
	  = Gaia source_id (e.g. 6050296829033196032).
```
```
pos       = 1D tuple of two integers
          = [ra,dec], object coordinates in degrees.
```
```
save_data = Bool
	  = saves raw data to a .csv file.
```

returns: Bokeh figure or None (if no data retrieved).

## Miscellaneous tools

### 1. correctPM

```
correctPM(input,target,ra,dec,pmra,pmdec)
```

where:
```
input  = 1D tuple of integers in form [year, month]
       = current epoch of coordinates
```
```
output = 1D tuple of integers in form [year, month]
       = target epoch of coordinates
```
```
ra     = float
       = right ascension of object in degrees
```
```
dec    = float
       = declination of object in degrees
```
```
pmra   = float
       = right ascension component of proper motion in milli-arcseconds/year
```
```
pmdec  = float
       = declination component of proper motion in milli-arcseconds/year
```

returns: ra (float), dec (float). 

### 2. getgaiacoords

```
getgaiacoords(source)

```

where:
```
source = integer/string
       = Gaia source_id (e.g. 6050296829033196032).
```

returns: 1D tuple of floats in format [ra,dec] or None (if no data retrieved).

### 3. getgaiasource

```
getgaiasource(pos,radius=3)
```

where:
```
pos    = 1D tuple of two integers
       = [ra,dec], object coordinates in degrees.
```
```
radius = integer
       = search radius of query in arcseconds.
```

returns: string or None (if no data retrieved)

### 4. getsources

```
getsources(file_name)
```

where:
```
file_name = string
          = .fits file containing a column 'source_id' of Gaia source IDs
```

returns: list of source_id's.

### 5. getpositions

```
getpositions(file_name)
```

where:
```
file_name = string
          = .fits file containing two columns 'ra' and 'dec'
```

returns: list of 'pos' objects, i.e. a list of lists with each 'pos' = [ra,dec].

### 6. getsd

Gets a spatial distribution plot of all objects in a .fits file.

```
getsd(file_name)
```

where:
```
file_name = string
          = .fits file containing two columns 'ra' and 'dec'
```

returns: bokeh plot or None (if no data retrieved).

### 7. convertsource

Converts a gaia source_id to a JHHMMSS.SS+DDMMSS.SS identifier (as seen in the save_data file naming convention).

```
convertsource(source)
```

where:
```
source = integer/string
       = Gaia source_id (e.g. 6050296829033196032).
```

### 8. readlocal

Reads a local csv-esque file (ie. columns separated by a separator, rows separated by a newline) into a 2D list containing the column data. A complete file name is not needed, the search will pick up any file whos name contains the input Gaia source_id or position in the format: ra_dec (i.e. the same format used throughout the toolkit for saving data).

```
readlocal(source=None,pos=None,extension='csv',headers=True,separator=',',getfilename=False):
```

where:

```
source      = integer/string
            = Gaia source_id (e.g. 6050296829033196032).
```
```
pos         = 1D tuple of two integers
            = [ra,dec], object coordinates in degrees.
```
```
extension   = string
            = file extension (without the '.')
```
```
headers     = boolean
	    = tells the tool whether to ignore the first row of data (if being used as column headers)
```
```
separator   = str
	    = tells the tool what separator to expect between columns
```
```
getfilename = boolean
	    = tells the tool whether to also return the name of the file it found
```

### 9. plotdata

A significantly simplified plotting function  for making quick Bokeh plots. 

***Note:*** This function is only intended to make the quick creation of basic Bokeh plots easier. For fully customizable Bokeh plots, refer to the Bokeh documentation.

```
plotdata(x,y,x_err=None,y_err=None,title=None,xlabel=None,ylabel=None,xtype='linear',ytype='linear',marker='circle',colour='black',legend='Data Points')
```

where:

```
x      = tuple
       = coordinates of data points on x-axis
```
```
y      = tuple
       = coordinates of data points on y axis
```
```
x_err  = tuple
       = x errors on data points (in same order as x)
```
```
y_err  = tuple
       = y errors on data points (in same order as x)
```
```
title  = string
       = plot title
```
```
xlabel = string
       = x-axis label
```
```
ylabel = string
       = y-axis label
```
```
xtype  = string, 'linear' or 'log'
       = x-axis type
```
```
ytype  = string, 'linear' or 'log'
       = y-axis type
```
```
marker = string, 'circle' or 'line'
       = type of plot (circle = scatter, line = line)
```
```
colour = colour of markers/lines/error bars
```
```
legend = name to give the data points in the legend
```

## Datapage functions

These functions are used to create custom datapages from any plots/data supported by AstroToolkit.

***NOTE:*** An example of datapage creation can be found within the packages 'Examples' folder, named 'datapage_creation.py' (within the …/Lib/site-packages/AstroToolkit from earlier). This can be imported from a python terminal using from AstroToolkit.Examples import datapage_creation.

### 1. getgrid

Helps with datapage creation.

```
getgrid(dimensions,plots,grid_size=250)
```
where:
```
dimensions = 1D Tuple
           = grid dimensions in format [width,height]. E.g. for a grid that is 6 units wide and 3 units tall, use dimensions = [6,3]
```
```
plots      = 2D Tuple
           = Tuple of plots, with their desired dimensions included. E.g. for a 2x2 plot and two 2x1 plots, use plots = [[plot1,2,2],[plot2,2,1],[plot3,2,1]].
```
```
grid_size  = int
           = size of each square of the grid to which all plots are scaled.
```

returns: list of plots stripped of their dimensions. E.g. for the plots = ... input above, the following will be returned:

```
[plot1,plot2,plot3]
```

where all plots have been scaled to the desired grid size.

***NOTE:*** Again, see the datapage_creation example as noted above for an example.

### 2. getinfobuttons

Returns a Bokeh figure containing SIMBAD and Vizier buttons for use in datapages.

```
getinfobuttons(grid_size,source=None,pos=None,simbad_radius=3,vizier_radius=3)
```

where:
```
grid_size = size of the grid to which the buttons are scaled.
```
```
source        = integer/string
              = Gaia source_id (e.g. 6050296829033196032).
```
```
pos           = 1D tuple of two integers
              = [ra,dec], object coordinates in degrees.
```
```
simbad_radius = int
              = radius to use in SIMBAD queries
```
```
vizier_radius = int
              = radius to use in Vizier queries
```

returns: Bokeh figure

# Currently supported imaging overlays

1. gaia (default)
2. galex_nuv
3. galex_fuv
4. ztf
5. rosat

*Note*: all overlays are proper motion corrected except rosat in all imaging functions. ZTF detections are particularly expensive, but can be useful in 'tracking' high proper motion objects through time.

# TestFile

To run a file that tests all functions, use:

```
from AstroToolkit.Miscellaneous import TestFile
```