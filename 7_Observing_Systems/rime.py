import numpy as np

from rime_phase import create_phase_term
from rime_brightness import create_sources
from rime_antenna import KAT7_antenna_uvw_coordinates, ap_index

KAT7_ant_uvw = KAT7_antenna_uvw_coordinates()

# l, m, I, Q, U, V
sources = np.array([
    [50, 50, 1.0, 0.0, 0.0, 0.0,],
    [35, 75, 2.0, 0.0, 0.0, 0.0,],
])

frequencies = np.linspace(1.3e9, 1.5e9, 8)

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
    lm, B = create_sources(*sources.T) 

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

    ap_idx = ap_index(nsrc=nsrc, ntime=ntime, na=na, nchan=nchan)
    K_per_ant = create_phase_term(lm, KAT7_ant_uvw, frequencies)
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

    # Return
    return V_pq.reshape(ntime, nbl, nchan, 2, 2)

vis = rime(KAT7_ant_uvw, sources, frequencies)
print vis