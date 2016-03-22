"""
    A subset of functions taken from:
    
    PySatel - a Python framework for automated processing of scientific data
    acquired from spacecraft instruments.
    Copyright (C) 2010 David Parunakian
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    https://code.google.com/p/pysatel/source/browse/trunk/coord.py?r=22
"""

import numpy as np

# Constants defined by the World Geodetic System 1984 (WGS84)
#see:
#   https://en.wikipedia.org/wiki/GRS_80
#   https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#The_application_of_Ferrari.27s_solution
#   https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates
a = 6378137. #[m]
b = 6356752.3142 #[m]
esq = 0.00669437999014
e1sq = 0.00673949674228
f = 1 / 298.257223563

def cbrt(x):
    if x >= 0: return pow(x, 1.0/3.0)
    else: return -pow(np.abs(x), 1.0/3.0)

def geodetic2ecef(lat, lon, alt, degrees=True):
    """geodetic2ecef(lat, lon, alt)
                     [deg][deg][m]
    Convert geodetic coordinates to ECEF.
    https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#From_geodetic_to_ECEF_coordinates
    """
    if degrees:
        lat = np.deg2rad(lat)
        lon = np.deg2rad(lon)
    xi = np.sqrt(1. - esq * (np.sin(lat)**2.))
    x = (a / xi + alt) * np.cos(lat) * np.cos(lon)
    y = (a / xi + alt) * np.cos(lat) * np.sin(lon)
    z = (a / xi * (1. - esq) + alt) * np.sin(lat)
    return x, y, z

def ecef2geodetic(x, y, z, degrees=True):
    """ecef2geodetic(x, y, z)
                     [m][m][m]
    Convert ECEF coordinates to geodetic.
    J. Zhu, "Conversion of Earth-centered Earth-fixed coordinates \
    to geodetic coordinates," IEEE Transactions on Aerospace and \
    Electronic Systems, vol. 30, pp. 957-961, 1994.
    https://en.wikipedia.org/wiki/Geographic_coordinate_conversion#The_application_of_Ferrari.27s_solution
    """
    r = np.sqrt(x * x + y * y)
    Esq = a * a - b * b
    F = 54. * b * b * z * z
    G = r * r + (1. - esq) * z * z - esq * Esq
    C = (esq * esq * F * r * r) / (pow(G, 3.))
    S = cbrt(1. + C + np.sqrt(C * C + 2. * C))
    P = F / (3. * pow((S + 1. / S + 1.), 2.) * G * G)
    Q = np.sqrt(1. + 2. * esq * esq * P)
    r_0 =  -(P * esq * r) / (1. + Q) + np.sqrt(0.5 * a * a*(1. + 1.0 / Q) - \
        P * (1. - esq) * z * z / (Q * (1. + Q)) - 0.5 * P * r * r)
    U = np.sqrt(pow((r - esq * r_0), 2.) + z * z)
    V = np.sqrt(pow((r - esq * r_0), 2.) + (1. - esq) * z * z)
    Z_0 = b * b * z / (a * V)
    h = U * (1. - b * b / (a * V))
    lat = np.arctan((z + e1sq * Z_0) / r)
    lon = np.arctan2(y, x)
    if degrees: return np.rad2deg(lat), np.rad2deg(lon), h
    else: return lat, lon, h

if __name__ == '__main__':
    print 'Running test cases'

    #known values for Chilbolton Observatory
    chilbolton={'lat': 51.143833512,
                'lon': -1.433500703,
                'h': 176.028,
                'x': 4008438.457200000,
                'y': -100309.724927000,
                'z': 4943735.828}

    X,Y,Z = geodetic2ecef(chilbolton['lat'], chilbolton['lon'], chilbolton['h'])
    lat,lon,h = ecef2geodetic(chilbolton['x'], chilbolton['y'], chilbolton['z'])
    print 'Known    (lat,lon,h):', chilbolton['lat'], chilbolton['lon'], chilbolton['h']
    print 'Computed (lat,lon,h):', lat,lon,h
    print 'Delta    (lat,lon,h):', np.abs(chilbolton['lat']-lat), np.abs(chilbolton['lon']-lon), np.abs(chilbolton['h']-h)

    print 'Known    (x,y,z):', chilbolton['z'], chilbolton['y'], chilbolton['z']
    print 'Computed (x,y,z):', X,Y,Z
    print 'Delta    (x,y,z):', np.abs(chilbolton['x']-X), np.abs(chilbolton['y']-Y), np.abs(chilbolton['z']-Z)

    print 'Made it through without any errors.'

