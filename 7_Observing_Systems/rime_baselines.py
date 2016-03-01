import numpy as np

def create_baselines(bl_len, hour_start, hour_end, ntime, declination):
    """
    Simulate baselines

    Arguments:
        bl_len : list
            A list of baseline lengths, in metres.
        hour_start : int
            Hour at which the observation starts
        hour_end : int
            Hour at which the observation ends
        ntime : int
            Number of timesteps to simulate
        declination : int
            Declination in degrees

    Returns:
        An ndarray of shape (ntime, nbl, 3)
    """

    # Cast to ndarray and sanity check
    bl_len = np.asarray(bl_len)
    assert bl_len.ndim == 1
    nbl = bl_len.shape[0]
    nhours = hour_end - hour_start

    # Create a space of computation over the length of observation
    H = np.linspace(hour_start, hour_end, ntime)
    delta = declination*np.pi/180

    # Create the result array and populate it
    uvw = np.empty(shape=(ntime, nbl, 3), dtype=np.float64)
    uvw[:,:,0] = bl_len[np.newaxis,:]*np.cos(H)[:,np.newaxis]
    uvw[:,:,1] = bl_len[np.newaxis,:]*np.sin(H)[:,np.newaxis]*np.sin(delta)
    uvw[:,:,2] = bl_len[np.newaxis,:]*np.sin(H)[:,np.newaxis]*-np.cos(delta)

    return uvw

create_baselines([100, 200, 300], -6, 6, 600, 60)