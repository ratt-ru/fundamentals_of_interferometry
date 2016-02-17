#!/usr/bin/python
"""Plot UVW positions from an MS"""

import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)

import numpy as np
import matplotlib.pyplot as plt
import sys
import pyrap.tables as tbls

cc = 299792458.

if __name__ == '__main__':                                                                                                                          
    from optparse import OptionParser
    o = OptionParser()
    o.set_usage('%prog [options] MS_FILE')
    o.set_description(__doc__)
    o.add_option('-d', '--uvdist', dest='uvdist', action='store_true',
        help='Plot a histogram of the number of samples based on their UV distance')
    o.add_option('-f', '--freqs', dest='freqs', action='store_true',
        help='Include frequency information in plot')
    o.add_option('-l', '--limit', dest='limit', default=None,
        help='Set the uv coverage limit, no default')
    o.add_option('-s', '--savefig', dest='savefig', default=None,
        help='Save figure')
    opts, args = o.parse_args(sys.argv[1:])

    ms = tbls.table(args[0], readonly=True)
    uvw = ms.getcol('UVW')
    ms.close()

    ms = tbls.table(args[0]+'/SPECTRAL_WINDOW', readonly=True)
    freqs = ms.getcol('CHAN_FREQ')[0]
    ms.close()

    fig = plt.figure( figsize=(8.5,8) ) #(width, height)

    if opts.uvdist:
        if opts.freqs:
            uvdist = []
            for freq in freqs:
                wl = cc / freq
                uvdist.append(np.sqrt( ((uvw[:,0] / wl)**2) + ((uvw[:,1] / wl)**2) ))
            uvdist = np.array(uvdist).flatten()
            plt.hist(uvdist, bins=50, alpha=.5)
            plt.xlabel('uv Distance ($\lambda$)', fontsize=20)
        else:
            uvdist = np.sqrt((uvw[:,0]**2) + (uvw[:,1]**2))
            plt.hist(uvdist, bins=50, alpha=.5)
            plt.xlabel('uv Distance (m)', fontsize=20)
        plt.ylabel('# Baselines', fontsize=20)
        plt.title('uv Distribution', fontsize=20)
    else:
        axes = plt.axes()
        if opts.freqs:
            if len(freqs)==1:
                wl = cc/freqs[0]
                plt.scatter(uvw[:,0]/wl, uvw[:,1]/wl, marker='s', edgecolor='none', c=(0.0,0.0,1.0), alpha=0.25)
                plt.scatter(-1.*uvw[:,0]/wl, -1.*uvw[:,1]/wl, marker='s', edgecolor='none', c=(0.0,0.0,1.0), alpha=0.25)
            else:
                crange = freqs - np.min(freqs)
                crange /= np.max(crange)
                for color,freq in zip(crange,freqs):
                    wl = cc/freq
                    plt.scatter(uvw[:,0]/wl, uvw[:,1]/wl, marker='s', edgecolor='none', c=(1.0-color,0.0,color), alpha=0.25)
                    plt.scatter(-1.*uvw[:,0]/wl, -1.*uvw[:,1]/wl, marker='s', edgecolor='none', c=(1.0-color,0.0,color), alpha=0.25)
            plt.xlabel("uu ($\lambda$)", fontsize=20)
            plt.ylabel("vv ($\lambda$)", fontsize=20)
        else:
            plt.plot(uvw[:,0], uvw[:,1], 'k.')
            plt.plot(-1.*uvw[:,0], -1.*uvw[:,1], 'k.')
            plt.xlabel("uu (m)", fontsize=20)
            plt.ylabel("vv (m)", fontsize=20)
        if not opts.limit is None:
            limit = float(opts.limit)
            plt.xlim(-1.*limit, limit)
            plt.ylim(-1.*limit, limit)

        ax = plt.gca()
        ax.set_aspect('equal')
        plt.grid(True)
        plt.title('uv Coverage')

    if opts.savefig: plt.savefig(opts.savefig)
    else: plt.show()

