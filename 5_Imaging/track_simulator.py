import numpy as np
from matplotlib import pyplot as plt

def sim_uv(ref_ra, ref_dec, 
           observation_length_in_hrs, 
           integration_length, 
           enu_coords,
           latitude,
           plot_on=False):
    """
    Simulates uv coverage given antenna coordintes in the East-North-Up frame
    
    Keyword arguments:
    ref_ra --- Right Ascension of pointing centre (degrees)
    ref_dec --- Declination of pointing centre (degrees)
    integration_length --- Integration length in hours
    enu_coordinates --- East-North-Up coordinates of antenna array at some latitude
    latitude --- Latitude (degrees) of reference point near antenna array
    plot_on --- Plots the projected u,v coverage after simulation (default=false)
    """
    no_antenna = enu_coords.shape[0]
    no_baselines = no_antenna * (no_antenna - 1) // 2 + no_antenna
    cphi = np.cos(np.deg2rad(latitude))
    sphi = np.sin(np.deg2rad(latitude))
    reference_dec_rad = np.deg2rad(ref_dec)
    integration_length_in_deg = integration_length / 24.0 * 360.0
    no_timestamps = int(observation_length_in_hrs / integration_length)
    row_count = no_timestamps * no_baselines

    l = no_antenna
    k = no_antenna
    uvw = np.empty([row_count,3])
    
    for r in range(0,row_count):
        timestamp = r / (no_baselines)
        baseline_index = r % (no_baselines)
        increment_antenna_1_coord = (baseline_index / k)
        
        # calculate antenna 1 and antenna 2 ids based on baseline index using some fancy
        # footwork ;). This indexing scheme will enumerate all unique baselines per
        # timestamp.
        
        l -= (1) * increment_antenna_1_coord
        k += (l) * increment_antenna_1_coord
        antenna_1 = no_antenna-l
        antenna_2 = no_antenna + (baseline_index-k)
        new_timestamp = ((baseline_index+1) / no_baselines)
        k -= (no_baselines-no_antenna) * new_timestamp
        l += (no_antenna-1) * new_timestamp
        #conversion to local altitude elevation angles:
        be,bn,bu = enu_coords[antenna_1] - enu_coords[antenna_2]
        mag_b = np.sqrt(be**2 + bn**2 + bu**2)
        epsilon = 0.000000000001
        A = np.arctan2(be,(bn + epsilon))
        E = np.arcsin(bu/(mag_b + epsilon))
        #conversion to equitorial coordinates:
        sA = np.sin(A)
        cA = np.cos(A)
        sE = np.sin(E)
        cE = np.cos(E)
        Lx = (cphi*sE-sphi*cE*cA)*mag_b
        Ly = (cE*sA)*mag_b
        Lz = (sphi*sE+cphi*cE*cA)*mag_b
        #conversion to uvw, where w points to the phase reference centre
        rotation_in_radians = np.deg2rad(timestamp*integration_length_in_deg + ref_ra)
        sin_ra = np.sin(rotation_in_radians)
        cos_ra = np.cos(rotation_in_radians)
        sin_dec = np.sin(reference_dec_rad)
        cos_dec = np.cos(reference_dec_rad)
        u = -sin_ra*Lx + cos_ra*Ly
        v = -sin_dec*cos_ra*Lx - sin_dec*sin_ra*Ly + cos_dec*Lz
        w = cos_dec*cos_ra*Lx + cos_dec*sin_ra*Ly + sin_dec*Lz
        uvw[r] = [u,v,w]
        
    if plot_on:
        hrs = int(observation_length_in_hrs)
        mins = int(observation_length_in_hrs * 60 - hrs*60)
        plt.figure(figsize=(5,5))
        plt.title("UV COVERAGE (%dh:%dm @ RA=%f, DEC=%f)" % (hrs,mins,ref_ra,ref_dec))
        plt.plot(uvw[:,0],uvw[:,1],"r.",label="Baselines")
        plt.plot(-uvw[:,0],-uvw[:,1],"b.",label="Conjugate Baselines")
        plt.xlabel("u ($cycles\cdot rad^{-1}\cdot m^{-1}$)")
        plt.ylabel("v ($cycles\cdot rad^{-1}\cdot m^{-1}$)")
        plt.legend(bbox_to_anchor=(1.75, 1.0))
        plt.show()
    return uvw