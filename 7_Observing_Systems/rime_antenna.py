import numpy as np
import os
import sys

# Hack to import 5_Imaging.track_simulator.py
base_dir, current_dir = os.path.split(os.getcwd())
imaging_dir = os.path.join(base_dir, '5_Imaging')
sys.path.insert(0, imaging_dir)

from track_simulator import sim_uv

def dec_degrees(degree_str):
    """ Convert a coordinate in DD:MM:SS.SS to decimal degrees """
    DECIMAL_DEGREE_DIVISORS = [1, 60, 3600, 216000]
    
    return sum(float(v) / DECIMAL_DEGREE_DIVISORS[i]
        for i, v in enumerate(degree_str
            .replace('.', ':')
            .split(':')))

"""
Array location
(nominal)    -30:43:17.34, 21:24:38.46, 1038
(latitude - DD:MM:SS.SS, longitude - DD:MM:SS.SS, altitude above MSL - m)
"""
KAT7_location = [dec_degrees('-30:43:17.34'), dec_degrees('21:24:38.46'), float('1038')]

"""
Antenna 1   25.095, -9.095, 0.045 (East, North, Up in metres, offset from array location)
Antenna 2   90.284, 26.380, -0.226
Antenna 3   3.985, 26.893, 0.000
Antenna 4   -21.605, 25.494, 0.019
Antenna 5   -38.272, -2.592, 0.391
Antenna 6   -61.595, -79.699, 0.702
Antenna 7   -87.988, 75.754, 0.138
"""
KAT7_ants = np.array([
    [25.095, -9.095, 0.045],
    [90.284, 26.380, -0.226],
    [3.985, 26.893, 0.000],
    [-21.605, 25.494, 0.019],
    [-38.272, -2.592, 0.391],
    [-61.595, -79.699, 0.702],
    [-87.988, 75.754, 0.138]
], dtype=np.float64)

ALL_SLICE = slice(None, None, 1)
SRC_SLICE  = (np.newaxis, ALL_SLICE, np.newaxis, np.newaxis, np.newaxis)
TIME_SLICE = (np.newaxis, np.newaxis, ALL_SLICE, np.newaxis, np.newaxis)
ANT_SLICE = (ALL_SLICE, np.newaxis, ALL_SLICE, ALL_SLICE, np.newaxis)
CHAN_SLICE = (np.newaxis, np.newaxis, np.newaxis, np.newaxis, ALL_SLICE)

def ap_index(nsrc=0, ntime=1, na=1, nchan=0):
    """
    Returns an antenna pair index suitable for producing
    a per baseline mapping of per antenna values.
    Indexes arrays of shape (nsrc, ntime, na, nchan). Returns
    an array of shape (2, nsrc, time, nbl, chan).

    The following must hold:
        ntime > 0 and na > 0

    If nsrc == 0 or nchan == 0 these dimension should not
    be present in the indexed shape and won't be present in
    the returned shape.

    >>> uvw_ant_coords = np.random.random(size=(10,7,3))
    >>> api = ap_index(ntime=10, na=7)
    >>> uvw_mapping = uvw_ant_coords[api]
    >>> uvw_bl_coords = uvw_mapping[0] - uvw_mapping[1]
    """
    needed = (_, S, T, A, C) = True, nsrc > 0, ntime > 0, na > 0, nchan > 0

    assert T, 'Number of timesteps must be greater than 1'
    assert A, 'Number of antenna must be greater than 1'

    nbl = na*(na+1)/2

    # This produces the default antenna pair mapping
    # ANT1: 0000 111 22 3
    # ANT2: 0123 123 23 3
    default_ap = np.tile(np.int32(np.triu_indices(na, 0)), ntime) \
            .reshape(2, ntime, nbl)

    # The index that we're going to return
    idx = []

    # These slices, when used to index the actual index values
    # below (np.arange(...) and default_ap), produce broadcasts
    # when idx is used to index an array
    if S:
        src_slice  = tuple([s for s, n in zip(SRC_SLICE, needed) if n])
        idx.append(np.arange(nsrc)[src_slice])

    time_slice = tuple([t for t, n in zip(TIME_SLICE, needed) if n])
    idx.append(np.arange(ntime)[time_slice])

    ant_slice  = tuple([a for a, n in zip(ANT_SLICE, needed) if n])
    idx.append(default_ap[ant_slice])

    if C:
        chan_slice = tuple([c for c, n in zip(CHAN_SLICE, needed) if n])
        idx.append(np.arange(nchan)[chan_slice])

    return idx

def KAT7_antenna_uvw_coordinates(ref_ra=60, ref_dec=45):
    """
    Returns the KAT7 antenna UVW coordinates for a given
    pointing direction.
    """

    # ref_ra = 0 to 360
    # ref_dec = 0 to 90

    bl_uvw = sim_uv(ref_ra=ref_ra, ref_dec=ref_dec,
        observation_length_in_hrs=12, integration_length=3,
        enu_coords=KAT7_ants, latitude=KAT7_location[1])

    # Check that we get the correct number of baselines
    # including auto-correlations
    na = KAT7_ants.shape[0]   
    nbl = na*(na+1)/2 
    ntime = bl_uvw.shape[0]//nbl
    assert bl_uvw.shape == (ntime*nbl, 3)

    bl_uvw = bl_uvw.reshape(ntime, nbl, 3)

    # Take the 0:na slice as our antenna coordinates
    # The na: slice can be derived from antenna coordinates
    ant_uvw = -bl_uvw[:,0:na,:]

    # Sanity check the result. Use per baseline antenna pair mappings
    # to index the result array. This produces
    # per antenna values for each baseline which,
    # when differenced, should match the original
    # baseline uvw coordinates
    ap_idx = ap_index(ntime=ntime, na=na)

    bl = ant_uvw[ap_idx]
    assert np.allclose(bl[0] - bl[1], bl_uvw.reshape(ntime, nbl, 3))

    return ant_uvw

coords = KAT7_antenna_uvw_coordinates()