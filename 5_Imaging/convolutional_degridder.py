import numpy as np

def fft_degrid(model_image,scaled_uv,Nx,Ny,convolution_filter):
    """
    Convolutional degridder
    
    Keyword arguments:
    model_image --- model image of the sky to degrid onto non-regular uv coordinates
    scaled_uv --- interferometer's uv coordinates. (Prerequisite: these uv points are already scaled by the simularity
                  theorem, such that -N_x*Cell_l*0.5 <= theta_l <= N_x*Cell_l*0.5 and
                  -N_y*Cell_m*0.5 <= theta_m <= N_y*Cell_m*0.5
    Nx,Ny --- size of image in pixels
    convolution_filter --- pre-instantiated AA_filter anti-aliasing filter object
    """
    model_vis_regular = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(model_image)))
    vis = np.zeros([scaled_uv.shape[0]],dtype=np.complex)
    for r in range(0,scaled_uv.shape[0]):
        disc_u = int(round(scaled_uv[r,0]))
        disc_v = int(round(scaled_uv[r,1]))
        frac_u_offset = int((1 - scaled_uv[r,0] + disc_u) * convolution_filter.oversample)
        frac_v_offset = int((1 - scaled_uv[r,1] + disc_v) * convolution_filter.oversample)
        if (disc_v + convolution_filter.full_sup_wo_padding  >= Ny or 
            disc_u + convolution_filter.full_sup_wo_padding >= Nx or
            disc_v < 0 or disc_u < 0): 
            continue
        interpolated_value = 0.0 + 0.0j
        for conv_v in range(0,convolution_filter.full_sup_wo_padding):
            v_tap = convolution_filter.filter_taps[conv_v * convolution_filter.oversample + frac_v_offset]  
            for conv_u in range(0,convolution_filter.full_sup_wo_padding):
                u_tap = convolution_filter.filter_taps[conv_u * convolution_filter.oversample + frac_u_offset]
                conv_weight = v_tap * u_tap
                interpolated_value += model_regular[disc_u - half_sup + conv_u, disc_v - half_sup + conv_v] * conv_weight
        vis[r] = interpolated_value
    return vis