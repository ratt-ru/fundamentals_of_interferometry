#!/usr/bin/python

import numpy as np

#*************************************************************************************
#JVLA A-CONFIGURATION ANTENNA COORDINATES
#*************************************************************************************

NO_ANTENNA = 27
NO_BASELINES = NO_ANTENNA * (NO_ANTENNA - 1) / 2 + NO_ANTENNA
global CENTRE_CHANNEL
CENTRE_CHANNEL = 299792458 / 1e9 #Wavelength of 1 GHz
#Antenna positions (from Measurement Set "ANTENNA" table)
#Here we assumed these are in Earth Centred Earth Fixed coordinates, see:
#https://en.wikipedia.org/wiki/ECEF
#http://casa.nrao.edu/Memos/229.html#SECTION00063000000000000000
ANTENNA_POSITIONS = np.array([[-1601614.0612 , -5042001.67655,  3554652.4556 ],
                              [-1602592.82353, -5042055.01342,  3554140.65277],
                              [-1604008.70191, -5042135.83581,  3553403.66677],
                              [-1605808.59818, -5042230.07046,  3552459.16736],
                              [-1607962.41167, -5042338.15777,  3551324.88728],
                              [-1610451.98712, -5042471.38047,  3550021.01156],
                              [-1613255.37344, -5042613.05253,  3548545.86436],
                              [-1616361.55414, -5042770.44074,  3546911.38642],
                              [-1619757.27801, -5042937.57456,  3545120.33283],
                              [-1600801.8806 , -5042219.38668,  3554706.38228],
                              [-1599926.05941, -5042772.99258,  3554319.74284],
                              [-1598663.0464 , -5043581.42675,  3553766.97336],
                              [-1597053.09556, -5044604.74775,  3553058.94731],
                              [-1595124.91894, -5045829.51558,  3552210.61536],
                              [-1592894.06565, -5047229.19866,  3551221.18004],
                              [-1590380.58836, -5048810.32526,  3550108.40109],
                              [-1587600.20193, -5050575.97608,  3548885.37942],
                              [-1584460.89944, -5052385.73479,  3547599.95893],
                              [-1601147.88523, -5041733.85511,  3555235.91485],
                              [-1601061.91592, -5041175.90771,  3556057.98198],
                              [-1600929.96685, -5040316.40179,  3557330.27755],
                              [-1600780.99626, -5039347.46356,  3558761.48715],
                              [-1600592.69255, -5038121.38064,  3560574.80334],
                              [-1600374.8084 , -5036704.25301,  3562667.85595],
                              [-1600128.31399, -5035104.17725,  3565024.64505],
                              [-1599855.571  , -5033332.40332,  3567636.57859],
                              [-1599557.83837, -5031396.39194,  3570494.71676]])

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
