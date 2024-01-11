from astropy.table import Table

'''
gets a list of sources from a fits file
'''
def get_source_list(file_name):
    if not file_name.endswith('.fits'):
        file_name+='.fits'
       
    # read file into a pandas dataframe 
    try:
        data=Table.read(file_name).to_pandas()
    except:
        raise Exception(f'File: {file_name} not found, or invalid format.')
    
    # get source_id column
    try:
        sources=data.loc[:,'source_id'].tolist()
    except:
        raise Exception('No source_id column found.')

    return sources

def get_pos_list(file_name):
    if not file_name.endswith('.fits'):
        file_name+='.fits'

    # read file into pandas dataframe
    try:
        data=Table.read(file_name).to_pandas()
    except:
        raise Exception(f'File: {file_name} not found, or invalid format.')
    
    # get ra and dec columns
    try:
        ra=data.loc[:,'ra'].tolist()
        dec=data.loc[:,'dec'].tolist()
    except:
        raise Exception('ra/dec columns not found.')
    
    # zips ra and dec values into pos ([ra,dec]) as supported by the rest of the toolkit
    pos_list=[list(x) for x in zip(ra,dec)]
    
    return pos_list