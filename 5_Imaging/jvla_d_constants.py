#!/usr/bin/python

import numpy as np

#*************************************************************************************
#JVLA D-CONFIGURATION ANTENNA COORDINATES
#*************************************************************************************

NO_ANTENNA = 27
NO_BASELINES = NO_ANTENNA * (NO_ANTENNA - 1) / 2 + NO_ANTENNA
CENTRE_CHANNEL = 1e9 / 299792458 #Wavelength of 1 GHz
#Antenna positions (from Measurement Set "ANTENNA" table)
#Here we assumed these are in Earth Centred Earth Fixed coordinates, see:
#https://en.wikipedia.org/wiki/ECEF
#http://casa.nrao.edu/Memos/229.html#SECTION00063000000000000000
ANTENNA_POSITIONS = np.array([[-1601710.017000 , -5042006.925200 , 3554602.355600],
                              [-1601150.060300 , -5042000.619800 , 3554860.729400],
                              [-1600715.950800 , -5042273.187000 , 3554668.184500],
                              [-1601189.030140 , -5042000.493300 , 3554843.425700],
                              [-1601614.091000 , -5042001.652900 , 3554652.509300],
                              [-1601162.591000 , -5041828.999000 , 3555095.896400],
                              [-1601014.462000 , -5042086.252000 , 3554800.799800],
                              [-1601185.634945 , -5041978.156586 , 3554876.424700],
                              [-1600951.588000 , -5042125.911000 , 3554773.012300],
                              [-1601177.376760 , -5041925.073200 , 3554954.584100],
                              [-1601068.790300 , -5042051.910200 , 3554824.835300],
                              [-1600801.926000 , -5042219.366500 , 3554706.448200],
                              [-1601155.635800 , -5041783.843800 , 3555162.374100],
                              [-1601447.198000 , -5041992.502500 , 3554739.687600],
                              [-1601225.255200 , -5041980.383590 , 3554855.675000],
                              [-1601526.387300 , -5041996.840100 , 3554698.327400],
                              [-1601139.485100 , -5041679.036800 , 3555316.533200],
                              [-1601315.893000 , -5041985.320170 , 3554808.304600],
                              [-1601168.786100 , -5041869.054000 , 3555036.936000],
                              [-1601192.467800 , -5042022.856800 , 3554810.438800],
                              [-1601173.979400 , -5041902.657700 , 3554987.517500],
                              [-1600880.571400 , -5042170.388000 , 3554741.457400],
                              [-1601377.009500 , -5041988.665500 , 3554776.393400],
                              [-1601180.861480 , -5041947.453400 , 3554921.628700],
                              [-1601265.153600 , -5041982.533050 , 3554834.858400],
                              [-1601114.365500 , -5042023.151800 , 3554844.944000],
                              [-1601147.940400 , -5041733.837000 , 3555235.956000]]);
ARRAY_LATITUDE = 34 + 4 / 60.0 + 43.497 / 3600.0 #Equator->North
ARRAY_LONGITUDE = -(107 + 37 / 60.0 + 03.819 / 3600.0) #Greenwitch->East, prime -> local meridian
REF_ANTENNA = 0
#Conversion from ECEF -> ENU:
#http://www.navipedia.net/index.php/Transformations_between_ECEF_and_ENU_coordinates
slambda = np.sin(np.deg2rad(ARRAY_LONGITUDE))
clambda = np.cos(np.deg2rad(ARRAY_LONGITUDE))
sphi = np.sin(ARRAY_LONGITUDE)
cphi = np.cos(ARRAY_LATITUDE)
ecef_to_enu = [[-slambda,clambda,0],
               [-clambda*sphi,-slambda*sphi,cphi],
               [clambda*cphi,slambda*cphi,sphi]]
ENU = np.empty(ANTENNA_POSITIONS.shape)
for a in range(0,NO_ANTENNA):
    ENU[a,:] = np.dot(ecef_to_enu,ANTENNA_POSITIONS[a,:])
ENU -= ENU[REF_ANTENNA]