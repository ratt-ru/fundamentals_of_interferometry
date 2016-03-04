import numpy as np
import os
import sys

# Hack to import 5_Imaging.track_simulator.py
base_dir, current_dir = os.path.split(os.getcwd())
imaging_dir = os.path.join(base_dir, '5_Imaging')
sys.path.insert(0, imaging_dir)

from track_simulator import sim_uv

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

def brightness(I, Q, U, V):
    """ Create a brightness matrix from the supplied stokes parameters """

    # Sanity checks
    assert I.ndim == Q.ndim == U.ndim == V.ndim == 1, \
        "Stokes parameters should only have one dimension."
    assert I.shape == Q.shape == U.shape == V.shape, \
        "I, Q, U and V do not have the same shape."

    # Setup our array dimensions
    nsrc = I.shape[0]

    # Create a nsrc x 2 x 2 matrix to hold the complex polarisation values
    B = np.empty(shape=(nsrc, 2, 2), dtype=np.complex128)

    # Compute the polarisation values
    B[:,0,0] = I + Q
    B[:,0,1] = U + V*1j
    B[:,1,0] = U - V*1j
    B[:,1,1] = I - Q

    return B

def lm_2_rad(ra, dec):
    """
    Creates source information given the supplied arrays.

    Arguments:
        ra : ndarray/list
            An array of shape (nsrc,) describing the
            right ascension for each source in degrees.
        dec : ndarray
            An array of shape (nsrc,) describing the
            declination for each source in degrees.

    Returns:
        A  (nsrc, 2) array containing
        the l and m coordinates in radians
    """

    # Sanity checks
    assert ra.ndim == dec.ndim == 1, \
        "Input arrays should only have one dimension."
    assert ra.shape == dec.shape, \
        "Input arrays do not have the same shape."

    # Right ascension (degrees) to radians
    # Declination (degrees) to radians
    # Right ascension deltas in radians
    ra_rad = ra * np.pi / 180
    dec_rad = dec * np.pi / 180    
    ra_delta_rad = ra - ra[0]

    # Create the empty lm array. Compute l and m.
    nsrc = ra.shape[0]
    lm = np.empty(shape=(nsrc,2), dtype=np.float64)
    lm[:,0] = np.cos(dec_rad)*np.sin(ra_delta_rad)
    lm[:,1] = np.sin(dec_rad)*np.cos(dec_rad[0]) - \
        np.cos(dec_rad)*np.sin(dec_rad[0])*np.sin(ra_delta_rad)

    return lm

# Speed of light in metres
C = 299792458

def phase(lm, uvw, frequency):
    """
    Compute the complex phase RIME term,
    given lm and uvw coordinates, as well as
    a list of frequencies.

    Arguments:
        lm : float array of shape (nsrc, 2)
            lm coordinates for each source in radians
        uvw : float array of shape (ntime, na, 3)
            uvw coordinates for each baseline in metres
        frequency : float array of shape (nchan)
            frequencies for each channel in hz

    Returns an array of complex values with
    shape (nsrc, ntime, na, nchan) representing
    the phase term.

    """

    assert lm.ndim == 2 and lm.shape[1] == 2, \
        "lm array should have shape (nsrc, 2)"
    assert uvw.ndim == 3 and uvw.shape[2] == 3, \
        "uvw array should have shape (ntime, na, 3)"
    assert frequency.ndim == 1, \
        "frequency array should have shape (nchan)"

    nsrc = lm.shape[0]
    ntime, na = uvw.shape[0], uvw.shape[1]
    nchan = frequency.shape[0]

    # Reference l and m slices for convenenience and compute n from them
    l, m = lm[:,0], lm[:,0]
    n = np.sqrt(1.0 - l**2 - m**2) - 1.0

    assert not np.isnan(n).any(), \
        ("Some values of l and m produce invalid values for n."
        "Check that 1 - l**2 - m**2 >= 0 holds for all l and m")

    # Reference u, v and w for convenience
    u, v, w = uvw[:,:,0], uvw[:,:,1], uvw[:,:,2]

    # Compute phase from outer product of the source and uvw coordinates
    phase =((np.outer(l, u) + np.outer(m, v) + np.outer(n, w))
        .reshape(nsrc, ntime, na) )

    # Now compute and return the complex phase
    return np.exp(-2*np.pi*1j*phase[:,:,:,np.newaxis]
        *frequency[np.newaxis,np.newaxis,np.newaxis,:]/C)


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

def KAT7_antenna_uvw(ref_ra=60, ref_dec=45):
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


def rime(ant_uvw, sources, frequencies):
    """
    Computes the RIME from the supplied argument.

    Arguments:
        ant_uvw : ndarray
            An array of shape (ntime, na, 3) containing
            the antenna UVW coordinates as they change
            over time.
        sources : ndarray
            An array of shape (nsrc, 6) containing rows
            with data [l, m, I, Q, U, V] defining the
            point source locations and stokes parameters
            in degrees and Jy respectively
        frequencies: ndarray
            An array of shape (nchan,) containing the
            frequencies.

    Returns a (ntime, nbl, nchan, 2, 2) ndarray of
    complex visibilities
    """
    # Derive lm and brightness matrix from the above array
    # *sources.T passes in transposed columns to the 
    # l, m, Q, U, V function arguments
    l, m, I, Q, U, V = sources.T

    # Work out lm in radians and compute the brightness matrix
    lm = lm_2_rad(l, m)
    B = brightness(I, Q, U, V)

    # Determine our problem dimensions
    ntime, na, _ = ant_uvw.shape
    nbl = na*(na+1)//2
    nsrc, _ = lm.shape
    nchan, = frequencies.shape

    print 'RIME Dimensions'
    print 'nsrc:   %s' % nsrc
    print 'ntime:  %s' % ntime
    print 'na:     %s' % na
    print 'nbl:    %s' % nbl
    print 'nchan:  %s' % nchan

    # Compute per antenna phase term
    K_per_ant = phase(lm, ant_uvw, frequencies)

    # Get an index that converts our per antenna values
    # into per baseline values. K_pq = K_p - K_q
    ap_idx = ap_index(nsrc=nsrc, ntime=ntime, na=na, nchan=nchan)
    K_per_bl = K_per_ant[ap_idx]
    K_p, K_q = K_per_bl[0], K_per_bl[1]

    # Compute source coherencies
    X_pqs = (K_p[:,:,:,:,np.newaxis,np.newaxis]*
        B[:,np.newaxis,np.newaxis,np.newaxis,:]*
        K_q[:,:,:,:,np.newaxis,np.newaxis])
    assert X_pqs.shape == (nsrc, ntime, nbl, nchan, 2, 2)

    # Sum over source dimension to produce visibilities
    V_pq = X_pqs.sum(axis=0)
    assert V_pq.shape == (ntime, nbl, nchan, 2, 2)

    # Return visibilities
    return V_pq.reshape(ntime, nbl, nchan, 2, 2)

