#!/bin/bash

#original data: fundamentals_of_interferometry/data/simulated_kat_7_vis/simulated_KAT-7_ms.tar.gz

wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_r2.0      -size 512 512 -scale 0.006 -nosmallinversion -weight briggs 2.0  -makepsf KAT-7_6h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_r1.0      -size 512 512 -scale 0.006 -nosmallinversion -weight briggs 1.0  -makepsf KAT-7_6h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_r0.5      -size 512 512 -scale 0.006 -nosmallinversion -weight briggs 0.5  -makepsf KAT-7_6h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_r0.0      -size 512 512 -scale 0.006 -nosmallinversion -weight briggs 0.0  -makepsf KAT-7_6h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_r-0.5     -size 512 512 -scale 0.006 -nosmallinversion -weight briggs -0.5 -makepsf KAT-7_6h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_r-1.0     -size 512 512 -scale 0.006 -nosmallinversion -weight briggs -1.0 -makepsf KAT-7_6h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_r-2.0     -size 512 512 -scale 0.006 -nosmallinversion -weight briggs -2.0 -makepsf KAT-7_6h60s_dec-30_10MHz_10chans.ms

