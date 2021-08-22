import numpy as np

def grid_ifft(vis, uvw, ref_lda, Nx, Ny, convolution_filter):
    """
    Convolutional gridder (continuum)

    Keyword arguments:
    vis --- Visibilities as sampled by the interferometer
    uvw --- interferometer's scaled uvw coordinates
            (Prerequisite: these uv points are already scaled by the similarity
            theorem, such that -N_x*Cell_l*0.5 <= theta_l <= N_x*Cell_l*0.5 and
            -N_y*Cell_m*0.5 <= theta_m <= N_y*Cell_m*0.5)
    ref_lda --- array of reference lambdas (size of vis channels)
    Nx,Ny --- size of image in pixels
    convolution_filter --- pre-instantiated AA_filter anti-aliasing
                           filter object
    """
    assert vis.shape[1] == ref_lda.shape[0], (vis.shape[1], ref_lda.shape[0])
    filter_index = \
        np.arange(-convolution_filter.half_sup,convolution_filter.half_sup+1)
    # one grid for the resampled visibilities per correlation:
    measurement_regular = \
        np.zeros([vis.shape[2],Ny,Nx],dtype=np.complex)
    # for deconvolution the PSF should be 2x size of the image (see 
    # Hogbom CLEAN for details), one grid for the sampling function:
    sampling_regular = \
        np.zeros([2*Ny,2*Nx],dtype=np.complex)
    for r in range(uvw.shape[0]):
        for c in range(vis.shape[1]):
            scaled_uv = uvw[r,:] / ref_lda[c]
            disc_u = int(np.round(scaled_uv[0]))
            disc_v = int(np.round(scaled_uv[1]))
            frac_u_offset = int((1 + convolution_filter.half_sup +
                                 (-scaled_uv[0] + disc_u)) *
                                convolution_filter.oversample)
            frac_v_offset = int((1 + convolution_filter.half_sup +
                                 (-scaled_uv[1] + disc_v)) *
                                convolution_filter.oversample)
            disc_u_psf = int(np.round(scaled_uv[0]*2))
            disc_v_psf = int(np.round(scaled_uv[1]*2))
            frac_u_offset_psf = int((1 + convolution_filter.half_sup +
                                     (-scaled_uv[0]*2 + disc_u_psf)) *
                                    convolution_filter.oversample)
            frac_v_offset_psf = int((1 + convolution_filter.half_sup +
                                     (-scaled_uv[1]*2 + disc_v_psf)) *
                                    convolution_filter.oversample)
            if (disc_v + Ny // 2 + convolution_filter.half_sup >= Ny or
                disc_u + Nx // 2 + convolution_filter.half_sup >= Nx or
                disc_v + Ny // 2 - convolution_filter.half_sup < 0 or
                disc_u + Nx // 2 - convolution_filter.half_sup < 0):
                continue
            for conv_v in filter_index:
                v_tap = \
                    convolution_filter.filter_taps[conv_v *
                                                   convolution_filter.oversample
                                                   + frac_v_offset]
                v_tap_psf = \
                    convolution_filter.filter_taps[conv_v *
                                                   convolution_filter.oversample
                                                   + frac_v_offset_psf]

                grid_pos_v = disc_v + conv_v + Ny // 2
                grid_pos_v_psf = disc_v_psf + conv_v + Ny
                for conv_u in filter_index:
                    u_tap = \
                        convolution_filter.filter_taps[conv_u *
                                                       convolution_filter.oversample
                                                       + frac_u_offset]
                    u_tap_psf = \
                        convolution_filter.filter_taps[conv_u *
                                                       convolution_filter.oversample
                                                       + frac_u_offset_psf]
                    conv_weight = v_tap * u_tap
                    conv_weight_psf = v_tap_psf * u_tap_psf
                    grid_pos_u = disc_u + conv_u + Nx // 2
                    grid_pos_u_psf = disc_u_psf + conv_u + Nx
                    for p in range(vis.shape[2]):
                        measurement_regular[p, grid_pos_v, grid_pos_u] += \
                            vis[r, c, p] * conv_weight
                    # assuming the PSF is the same for different correlations:
                    sampling_regular[grid_pos_v_psf, grid_pos_u_psf] += \
                        (1+0.0j) * conv_weight_psf

    dirty = np.zeros(measurement_regular.shape, dtype=measurement_regular.dtype)
    psf = np.zeros(sampling_regular.shape, dtype=sampling_regular.dtype)

    for p in range(vis.shape[2]):
        dirty[p,:,:] = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(measurement_regular[p,:,:])))
    psf[:,:] = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(sampling_regular[:,:])))
    return dirty,psf
