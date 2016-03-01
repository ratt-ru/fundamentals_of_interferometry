import numpy as np

# Speed of light in metres
C = 299792458

def create_phase_term(lm, uvw, frequency):
    """
    Compute the complex phase RIME term,
    given lm and uvw coordinates, as well as
    a list of frequencies.

    Arguments:
        lm : float array of shape (nsrc, 2)
            lm coordinates for each source in radians
        uvw : float array of shape (ntime, nbl, 3)
            uvw coordinates for each baseline in metres
        frequency : float array of shape (nchan)
            frequencies for each channel in hz

    Returns an array of complex values with
    shape (nsrc, ntime, nbl, nchan) representing
    the phase term.

    """

    assert lm.ndim == 2 and lm.shape[1] == 2, \
        "lm array should have shape (nsrc, 2)"
    assert uvw.ndim == 3 and uvw.shape[2] == 3, \
        "uvw array should have shape (ntime, nbl, 3)"
    assert frequency.ndim == 1, \
        "frequency array should have shape (nchan)"

    nsrc = lm.shape[0]
    ntime, nbl = uvw.shape[0], uvw.shape[1]
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
        .reshape(nsrc, ntime, nbl) )

    # Now compute and return the complex phase
    return np.exp(-2*np.pi*1j*phase[:,:,:,np.newaxis]
        *frequency[np.newaxis,np.newaxis,np.newaxis,:]/C)

nsrc, ntime, nbl, nchan = 10, 20, 30, 64

# Create some random lm and UVW coordinates
lm = np.random.random(size=(nsrc, 2))*0.1
uvw = np.random.random(size=(ntime, nbl, 3))
frequency = np.linspace(1.3e9, 1.5e9, nchan)

phase = create_phase_term(lm, uvw, frequency)
assert phase.shape == (nsrc, ntime, nbl, nchan)