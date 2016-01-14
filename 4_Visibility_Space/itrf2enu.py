def convert(fileitrf,save_enu=True,plot=False):
    """
      xyz : positions of layouts (numpy array)
    """
  #if anttab:
  #    xyz = table(anttab).getcol("POSITION")
    import numpy as np
    import pyrap.quanta
    import ipdb
    import matplotlib.pyplot as plt
    from pyrap.measures import measures
    import os

    name=os.path.basename(fileitrf).split('.')[0]

    f=open(fileitrf,'r')
    hd=f.readline()
    tabx=[]
    taby=[]
    tabz=[]
    for line in f:
        line=line.strip()
        columns=line.split()
        print columns
        tabx.append(columns[0])
        taby.append(columns[1])
        tabz.append(columns[2])

    xyz=np.array([tabx,taby,tabz]).T.astype(float)
    dm = measures()
    dq = pyrap.quanta
    DEG = 180./np.pi
    EarthRad=6471.
  
    deg2m = 2*np.pi*EarthRad/360. # Arc length subtended by 1 deg at Earth Radius distance
    #ipdb.set_trace()
    p1 = dm.position('itrf',*[dq.quantity(xyz[:,i],'m') for i in range(3)])
    lon = p1['m0']['value']
    lat = p1['m1']['value']
    dx = (lon-lon[0])*np.cos(lat[0])*DEG*deg2m
    dy = (lat-lat[0])*DEG*deg2m
    #ipdb.set_trace()
    if save_enu : np.savetxt('%s.enu.txt'%name,np.array([dx*1e3,dy*1e3]).T)
   # if show_base:
    #    pos = table(base).getcol("POSITION")
    #    p1 = dm.position('itrf',*[dq.quantity(pos[:,i],'m') for i in range(3)])
    #    lon = p1['m0']['value']
    #    lat = p1['m1']['value']
    #    dx = (lon-lon[0])*np.cos(lat[0])*DEG*deg2m
    #    dy = (lat-lat[0])*DEG*deg2m
    if plot: plt.plot(dx,dy,'rx')

    return dx,dy



 
