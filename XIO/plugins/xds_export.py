# -*- coding: utf-8 -*-

__version__ = "0.3.1"
__author__ = "Pierre Legrand (pierre.legrand@synchrotron-soleil.fr)"
__date__ = "10-11-2009"
__copyright__ = "Copyright (c) 2007-2009 Pierre Legrand"
__license__ = "New BSD License http://www.opensource.org/licenses/bsd-license.php"

import time
from math import pi, cos, sin

from pycgtypes import vec3
from pycgtypes import mat3

X, Y, Z = vec3(1,0,0), vec3(0,1,0), vec3(0,0,1)
fmt = "%9.6f %9.6f %9.6f"

def detCoordinates2(X, Y, twotheta_vect, twotheta_angle):
    fmt = "0.000000 %.6f %.6f"
    return fmt % (cos(twotheta*pi/180.), sin(twotheta*pi/180.))

def detCoordinates(twotheta):
    fmt = "0.000000 %.6f %.6f"
    return fmt % (cos(twotheta*pi/180.), sin(twotheta*pi/180.))

def det_dist(distance, dettype):
    detori = XDS_detector_dict["orient"][dettype]
    return distance*detori[2]

def det_spindle(dettype):
    return fmt % tuple(XDS_detector_dict["orient"][dettype][3])
    
def polarization(wavelength):
    if 1.5414 < wavelength < 1.5422:
        return 0.5
    else:
        return 0.99

def det_axis_x(twotheta, dettype):
    detori = XDS_detector_dict["orient"][dettype]
    return fmt % tuple(detori[0]*mat3().rotation(twotheta*pi/180, detori[4]))

def det_axis_y(twotheta, dettype):
    detori = XDS_detector_dict["orient"][dettype]
    return fmt % tuple(detori[1]*mat3().rotation(twotheta*pi/180, detori[4]))

def det_beam_x(x0, y0, qx, qy, dettype):
    _def = XDS_detector_dict["orient"][dettype][5]
    orgx, orgy = x0/qx, y0/qy
    if _def == "XY": return orgx
    elif _def == "YX": return orgy

def det_beam_y(x0, y0, qx, qy, dettype):
    _def = XDS_detector_dict["orient"][dettype][5]
    orgx, orgy = x0/qx, y0/qy
    if _def == "XY": return orgy
    elif _def == "YX": return orgx

XDS_detector_dict = {
  "detector_name":{
    "mar":       "MAR345",
    "mar555":    "MAR345",
    "marccd":    "CCDCHESS",
    "adsc":      "ADSC",
    "raxis":     "RAXIS",
    "minicbf":   "PILATUS",
    "mscccd":    "SATURN",
  },
  "overload":{
    "mar":       130000,
    "mar555":    250000,
    "marccd":     65000,
    "adsc":       65000,
    "raxis":     262100, # this is for raxisII. 1000000 for raxisIV. and 2000000 for raxisV
    "minicbf":  1048500,
    "mscccd":   1000000,
  },
  "minval":{
    "mar":      0,
    "mar555":   0,
    "marccd":   1,
    "adsc":     1,
    "raxis":    0,
    "minicbf":  0,
    "mscccd":   1,
  },
  "min_number_of_pixels":{
    "mar":      8,
    "mar555":   4,
    "marccd":   8,
    "adsc":     8,
    "raxis":    8,
    "minicbf":  4,
    "mscccd":   8,
  },
  "orient":{ # X_det, Y_det, distanceSign, spindle_axis, twoThetaAxis, beamdef
    "mar":      ( X, Y, 1, X, Y, "XY"),
    "mar555":   ( X, Y, 1, X, X, "XY"),
    "marccd":   ( X, Y, 1, X, X, "YX"),
    "adsc":     ( X, Y, 1, X, X, "YX"),
    "raxis":    ( X, Y,-1, Y, Y, "XY"),
    "minicbf":  ( X, Y, 1, X, X, "XY"),
    "mscccd":   (-X, Y,-1,-Y, Y, "XY"),
  }
}

TEMPLATE = """! File Automaticaly generated by XIO
!       date: %s
!       Beamline SOLEIL-Proxima1
""" % (time.ctime())

TEMPLATE += """
 JOB= ALL ! XYCORR INIT COLSPOT IDXREF DEFPIX XPLAN INTEGRATE CORRECT

 NAME_TEMPLATE_OF_DATA_FRAMES= %(NAME_TEMPLATE_OF_DATA_FRAMES)s
 DATA_RANGE= %(_DRI)d %(_DRF)d
 SPOT_RANGE= %(_DRI)d %(_DRF)d
 BACKGROUND_RANGE= %(_DRI)d %(_DRB)d

 OSCILLATION_RANGE= %(OSCILLATION_RANGE).3f
 STARTING_ANGLE= %(STARTING_ANGLE).3f
 STARTING_FRAME= %(_DRI)d
 X-RAY_WAVELENGTH= %(X_RAY_WAVELENGTH).5f
 DETECTOR_DISTANCE= %(DETECTOR_DISTANCE).2f
 ORGX= %(ORGX).2f   ORGY= %(ORGY).2f
 DETECTOR= %(DETECTOR)s   MINIMUM_VALID_PIXEL_VALUE= %(MINIMUM_VALID_PIXEL_VALUE)d   OVERLOAD= %(OVERLOAD)d
 DIRECTION_OF_DETECTOR_X-AXIS= %(DIRECTION_OF_DETECTOR_X-AXIS)s
 DIRECTION_OF_DETECTOR_Y-AXIS= %(DIRECTION_OF_DETECTOR_Y-AXIS)s

 NX= %(NX)d    NY= %(NX)d    QX= %(QX).5f  QY= %(QY).5f
 ROTATION_AXIS= %(ROTATION_AXIS)s
 INCIDENT_BEAM_DIRECTION= 0.0 0.0 1.0
 FRACTION_OF_POLARIZATION= %(FRACTION_OF_POLARIZATION).3f
 POLARIZATION_PLANE_NORMAL= 0.0 1.0 0.0

 MINIMUM_NUMBER_OF_PIXELS_IN_A_SPOT= %(MINIMUM_NUMBER_OF_PIXELS_IN_A_SPOT)d
 STRONG_PIXEL= 8.0
 SPOT_MAXIMUM-CENTROID= 2.0

 SPACE_GROUP_NUMBER= 0
 UNIT_CELL_CONSTANTS= 0 0 0 0 0 0

 INCLUDE_RESOLUTION_RANGE= 30.0 0.0
 TRUSTED_REGION= 0.0 1.05
 VALUE_RANGE_FOR_TRUSTED_DETECTOR_PIXELS= 7000 30000

 DELPHI= %(DELPHI).2f
 REFINE(INTEGRATE)= BEAM ORIENTATION CELL
 
 MAXIMUM_NUMBER_OF_PROCESSORS= 16
 MAXIMUM_NUMBER_OF_JOBS= 1
 RESOLUTION_SHELLS=20.0 10.0 6.0 3.0
 TOTAL_SPINDLE_ROTATION_RANGES=15.0 120.0 15.0
 STARTING_ANGLES_OF_SPINDLE_ROTATION=-95.0 95.0 5.0
 PROFILE_FITTING= TRUE
 STRICT_ABSORPTION_CORRECTION= TRUE
 FRIEDEL'S_LAW= TRUE
 ! REFERENCE_DATA_SET=
"""


#     Header Translator Dictionary.
#     Translate image header entries in a new dictionay
#     newdic['X_RAY_WAVELENGTH'] = float(head['Wavelength'])
#
HTD = {
'X_RAY_WAVELENGTH':(['Wavelength'], float),
'DETECTOR_DISTANCE':(['Distance','ImageType'], det_dist),
'ROTATION_AXIS':(['ImageType'], det_spindle),
'FRACTION_OF_POLARIZATION': (['Wavelength'], polarization),
'STARTING_ANGLE':(['PhiStart'], float),
'OSCILLATION_RANGE':(['PhiWidth'], float),
'NX':(['Width'], int),
'NY':(['Height'], int),
'QX':(['PixelX'], float),
'QY':(['PixelY'], float),
'ORGX':(['BeamX','BeamY','PixelX','PixelY','ImageType'], det_beam_x),
'ORGY':(['BeamX','BeamY','PixelX','PixelY','ImageType'], det_beam_y),
'DELPHI':(['PhiWidth'], lambda x: 16*x),
'DIRECTION_OF_DETECTOR_X-AXIS':(['TwoTheta','ImageType'], det_axis_x),
'DIRECTION_OF_DETECTOR_Y-AXIS':(['TwoTheta','ImageType'], det_axis_y),
}

#     Collect Translator Dictionary.
#     Translate collect object attributes to a new dictionay
#     newdic['SPOT_RANGE'] = list(collect.imageRanges)
#
CTD = {
'NAME_TEMPLATE_OF_DATA_FRAMES':(['xdsTemplate'], str),
'DATA_RANGE':(['imageNumbers'], lambda x: [x[0],x[-1]]),
'_DRI':(['imageNumbers'], lambda x: x[0]),
'_DRF':(['imageNumbers'], lambda x: x[-1]),
'_DRB':(['imageNumbers'], lambda x: min(x[0]+9,x[-1])),
'SPOT_RANGE':(['imageRanges'], list),
'BACKGROUND_RANGE':(['imageRanges'], lambda x: [x[0][0],min(x[0][0]+7,x[0][1])]),
'DETECTOR':(['imageType'], lambda x: XDS_detector_dict["detector_name"][x]),
'NAME_TEMPLATE_OF_DATA_FRAMES':(['xdsTemplate'], str),
'OVERLOAD':(['imageType'], lambda x: XDS_detector_dict["overload"][x]),
'MINIMUM_VALID_PIXEL_VALUE':(['imageType'], lambda x: XDS_detector_dict["minval"][x]),
'MINIMUM_NUMBER_OF_PIXELS_IN_A_SPOT':(['imageType'], lambda x: XDS_detector_dict["min_number_of_pixels"][x]),
}
