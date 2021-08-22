import numpy as np

def fft_degrid(model_image, uvw, ref_lda, Nx, Ny, convolution_filter):
    """
    Convolutional gridder (continuum)

    Keyword arguments:
    model_image --- Model image
    uvw --- interferometer's scaled uvw coordinates
            (Prerequisite: these uv points are already scaled by the similarity
            theorem, such that -N_x*Cell_l*0.5 <= theta_l <= N_x*Cell_l*0.5 and
            -N_y*Cell_m*0.5 <= theta_m <= N_y*Cell_m*0.5)
    ref_lda --- array of reference lambdas (size of vis channels)
    Nx,Ny --- size of image in pixels
    convolution_filter --- pre-instantiated AA_filter anti-aliasing
                           filter object
    """
    assert model_image.ndim == 3
    filter_index = \
        np.arange(-convolution_filter.half_sup,convolution_filter.half_sup+1)
    model_vis_regular = np.zeros(model_image.shape, dtype=np.complex64)
    for p in range(model_image.shape[0]):
        model_vis_regular[p, :, :] = \
            np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(model_image[p, :, :])))
    vis = \
        np.zeros([uvw.shape[0],
                  ref_lda.shape[0],
                  model_image.shape[0]],
                 dtype=np.complex)

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
                grid_pos_v = disc_v + conv_v + Ny // 2
                for conv_u in filter_index:
                    u_tap = \
                        convolution_filter.filter_taps[conv_u *
                                                       convolution_filter.oversample
                                                       + frac_u_offset]
                    conv_weight = v_tap * u_tap
                    grid_pos_u = disc_u + conv_u + Nx // 2
                    for p in range(vis.shape[2]):
                        vis[r, c, p] += \
                            model_vis_regular[p,
                                              grid_pos_v,
                                              grid_pos_u] * conv_weight

    return vis
