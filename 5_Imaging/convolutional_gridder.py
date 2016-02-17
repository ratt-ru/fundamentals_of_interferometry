import numpy as np

def grid_ifft(vis,scaled_uv,Nx,Ny,convolution_filter):
    """
    Convolutional gridder
    
    Keyword arguments:
    vis --- Visibilities as sampled by the interferometer
    scaled_uv --- interferometer's uv coordinates. (Prerequisite: these uv points are already scaled by the simularity
                  theorem, such that -N_x*Cell_l*0.5 <= theta_l <= N_x*Cell_l*0.5 and
                  -N_y*Cell_m*0.5 <= theta_m <= N_y*Cell_m*0.5
    Nx,Ny --- size of image in pixels
    convolution_filter --- pre-instantiated AA_filter anti-aliasing filter object
    """
    measurement_regular = np.zeros([Nx,Ny],dtype=np.complex) #one grid for the resampled visibilities
    #for deconvolution the PSF should be 2x size of the image (see Hogbom CLEAN for details)
    sampling_regular = np.zeros([2*Nx,2*Ny],dtype=np.complex) #one grid for the resampled sampling function
    for r in range(0,scaled_uv.shape[0]):
        disc_u = int(round(scaled_uv[r,0]))
        disc_v = int(round(scaled_uv[r,1]))
        frac_u_offset = int((1 - scaled_uv[r,0] + disc_u) * convolution_filter.oversample)
        frac_v_offset = int((1 - scaled_uv[r,1] + disc_v) * convolution_filter.oversample)
        if (disc_v + convolution_filter.full_sup_wo_padding  >= Ny or 
            disc_u + convolution_filter.full_sup_wo_padding >= Nx or
            disc_v < 0 or disc_u < 0): 
            continue
        for conv_v in range(0,convolution_filter.full_sup_wo_padding):
            v_tap = convolution_filter.filter_taps[conv_v * convolution_filter.oversample + frac_v_offset]  
            for conv_u in range(0,convolution_filter.full_sup_wo_padding):
                u_tap = convolution_filter.filter_taps[conv_u * convolution_filter.oversample + frac_u_offset]
                conv_weight = v_tap * u_tap
                measurement_regular[disc_u - convolution_filter.half_sup + conv_u, disc_v - convolution_filter.half_sup + conv_v] += vis[r] * conv_weight
                sampling_regular[disc_u - convolution_filter.half_sup + conv_u, disc_v - convolution_filter.half_sup + conv_v] += (1+0.0j) * conv_weight
    dirty_sky = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(measurement_regular)))
    psf = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(sampling_regular)))
    dirty_sky /= np.max(psf) # normalize by the centre value of the PSF
    return dirty_sky, psf