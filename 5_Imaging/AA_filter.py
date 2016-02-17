import numpy as np

class AA_filter:
    """
    Anti-Aliasing filter
    
    Keyword arguments for __init__:
    filter_half_support --- Half support (N) of the filter; the filter has a full support of N*2 + 1 taps
    filter_oversampling_factor --- Number of spaces in-between grid-steps (improves gridding/degridding accuracy)
    filter_type --- box (nearest-neighbour), sinc or gaussian_sinc
    """
    half_sup = 0
    oversample = 0
    full_sup_wo_padding = 0
    full_sup = 0
    no_taps = 0
    filter_taps = None
    def __init__(self, filter_half_support, filter_oversampling_factor, filter_type):
        self.half_sup = filter_half_support
        self.oversample = filter_oversampling_factor
        self.full_sup_wo_padding = (filter_half_support * 2 + 1)
        self.full_sup = self.full_sup_wo_padding + 2 #+ padding
        self.no_taps = self.full_sup + (self.full_sup - 1) * (filter_oversampling_factor - 1)
        taps = np.arange(-self.no_taps//2,self.no_taps//2 + 1)/float(filter_oversampling_factor)
        if filter_type == "box":
            self.filter_taps = np.where((taps >= -0.5) & (taps <= 0.5),
                                        np.ones([len(taps)]),np.zeros([len(taps)]))
        elif filter_type == "sinc":
            self.filter_taps = np.sinc(taps)
        elif filter_type == "gaussian_sinc":
            alpha_1=1.55
            alpha_2=2.52
            self.filter_taps = np.sin(np.pi/alpha_1*(taps+0.00000000001))/(np.pi*(taps+0.00000000001))*np.exp(-(taps/alpha_2)**2)
        else:
            raise ValueError("Expected one of 'box','sinc' or 'gausian_sinc'")