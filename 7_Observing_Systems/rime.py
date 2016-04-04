import numpy as np

from rime_lib import KAT7_antenna_uvw, rime

# Define our sources in this array, each row has the form
# [l, m, I, Q, U, V] with l and m in degrees and stokes
# parameters in Jy
sources = np.array([
    [50, 50, 1.0, 0.0, 0.0, 0.0,],
    [35, 75, 2.0, 0.0, 0.0, 0.0,],
])

# Compute the RIME over eight frequencies
frequencies = np.linspace(1.3e9, 1.5e9, 8)
# Use the uvw coordinates of the KAT7 antenna
uvw = KAT7_antenna_uvw()

# Compute the RIME
vis = rime(uvw, sources, frequencies)

# Work out visibility dimensions
ntime, nbl, nchan, _, _ = vis.shape

print vis
print 'Computed complex visibilities of shape ({t}x{bl}x{ch}x2x2)'.format(
    t=ntime, bl=nbl, ch=nchan)