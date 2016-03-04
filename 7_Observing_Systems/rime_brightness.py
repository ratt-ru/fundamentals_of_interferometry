from attrdict import AttrDict
import numpy as np

dims = AttrDict({
    'nsrc' : 10,
    'npol' : 4,
})

def create_brightness(I, Q, U, V):
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

def create_sources(ra, dec, I, Q, U, V):
    """
    Creates source information given the supplied arrays.

    Arguments:
        ra : ndarray/list
            An array of shape (nsrc,) describing the
            right ascension for each source in degrees.
        dec : ndarray
            An array of shape (nsrc,) describing the
            declination for each source in degrees.
        I : ndarray
            An array of shape (nsrc,) describing the
            I stokes for each source in Jy.
        Q : ndarray
            An array of shape (nsrc,) describing the
            Q stokes for each source in Jy.
        U : ndarray
            An array of shape (nsrc,) describing the
            U stokes for each source in Jy.
        V : ndarray
            An array of shape (nsrc,) describing the
            V stokes for each source in Jy.

    Returns:
        A tuple (lm, B) where lm is a (nsrc, 2) array containing
        the l and m coordinates in radians and B is
        a (nsrc, 2, 2) array representing the brightness matrix
    """

    # Sanity checks
    assert ra.ndim == dec.ndim == I.ndim == Q.ndim == U.ndim == V.ndim == 1, \
        "Input arrays should only have one dimension."
    assert ra.shape == dec.shape == I.shape == Q.shape == U.shape == V.shape, \
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

    return lm, create_brightness(I, Q, U, V)

# Create random right ascension coordinates (in degrees)
# Create random declination coordinates (in degrees)
ra = np.random.random(size=(dims.nsrc,)) * 360
dec = np.random.random(size=(dims.nsrc,)) * 90

# Assuming monochromatic coherent radiation,
# create some random stokes parameters
Q = np.random.random(size=(dims.nsrc,)) - 0.5
U = np.random.random(size=(dims.nsrc,)) - 0.5
V = np.random.random(size=(dims.nsrc,)) - 0.5
I = np.sqrt(Q**2 + U**2 + V**2)

# Get our lm and brightness coordinates
lm, B = create_sources(ra, dec, I, Q, U, V)

assert lm.shape == (dims.nsrc, 2)
assert B.shape == (dims.nsrc, 2, 2)