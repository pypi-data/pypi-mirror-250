from calendar import c
import math

'''
Takes an input year in format [year,month] and corrects coordinates of an object (using its pmra and pmdec) to correct for its proper motion to a target year in format [year,month]
'''
def PMCorrection(input,target,inputObjRA,inputObjDEC,pmRA,pmDEC,radius=None):
	# Filter inputs
	if not isinstance(input[0],int):
		raise Exception('input year must be an integer')
	if not isinstance(input[1],int):
		raise Exception('input month must be an integer')
	if not isinstance(target[0],int):
		raise Exception('target year must be an integer')
	if not isinstance(target[1],int):
		raise Exception('target month must be an integer')
	
	if not isinstance(inputObjRA,float):
		try:
			inputObjRA=float(inputObjRA)
		except:
			raise Exception('object RA must be a float or an integer')
		
	if not isinstance(inputObjDEC,float):
		try:
			inputObjDEC=float(inputObjDEC)
		except:
			raise Exception('object DEC must be a float or an integer')
		
	if not isinstance(pmRA,float):
		try:
			pmRA=float(pmRA)
		except:
			raise Exception('object PM_RA must be a float or an integer')
		
	if not isinstance(pmDEC,float):
		try:
			pmDEC=float(pmDEC)
		except:
			raise Exception('object PM_DEC must be a float or an integer')
	
	inputYear,inputMonth=input[0],input[1]
	targetYear,targetMonth=target[0],target[1]
	
	# get change in years and change in months
	yearDelta=targetYear-inputYear
	monthDelta=targetMonth-inputMonth

	# correct for proper motion
	inputObjRA+=(yearDelta*pmRA/3600000+monthDelta*pmRA/43200000)*1/math.cos(inputObjDEC/360*2*math.pi)
	inputObjDEC+=yearDelta*pmDEC/3600000+monthDelta*pmDEC/43200000
	
	# get time delta in years
	timeDelta=abs(yearDelta+monthDelta/12)
	
	# if a radius is given, use this time delta to scale the radius (used in adaptive proper motion correction)
	if radius!=None:
		radius=radius+math.sqrt((pmRA/1000)**2+(pmDEC/1000)**2)*timeDelta
		return inputObjRA,inputObjDEC,radius
	else:
		return inputObjRA,inputObjDEC