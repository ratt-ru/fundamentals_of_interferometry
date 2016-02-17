#!/bin/bash

#original data: fundamentals_of_interferometry/data/simulated_kat_7_vis/simulated_KAT-7_ms.tar.gz

#Obs length
wsclean -name KAT-7_0.167h60s_dec-30_10MHz_10chans_natural -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_0.167h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_2h60s_dec-30_10MHz_10chans_natural     -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_2h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_4h60s_dec-30_10MHz_10chans_natural     -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_4h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_natural     -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_6h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_8h60s_dec-30_10MHz_10chans_natural     -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_8h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_10h60s_dec-30_10MHz_10chans_natural    -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_10h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_12h60s_dec-30_10MHz_10chans_natural    -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_12h60s_dec-30_10MHz_10chans.ms

#channels
wsclean -name KAT-7_6h60s_dec-30_10MHz_1chans_natural      -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_6h60s_dec-30_10MHz_1chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_100chans_natural    -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_6h60s_dec-30_10MHz_100chans.ms

#declination
wsclean -name KAT-7_6h60s_dec30_10MHz_10chans_natural      -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_6h60s_dec30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec0_10MHz_10chans_natural       -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_6h60s_dec0_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-60_10MHz_10chans_natural     -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_6h60s_dec-60_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-90_10MHz_10chans_natural     -size 512 512 -scale 0.006 -nosmallinversion -weight natural KAT-7_6h60s_dec-90_10MHz_10chans.ms

#Obs length
wsclean -name KAT-7_0.167h60s_dec-30_10MHz_10chans_uniform -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_0.167h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_2h60s_dec-30_10MHz_10chans_uniform     -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_2h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_4h60s_dec-30_10MHz_10chans_uniform     -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_4h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_uniform     -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_6h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_8h60s_dec-30_10MHz_10chans_uniform     -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_8h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_10h60s_dec-30_10MHz_10chans_uniform    -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_10h60s_dec-30_10MHz_10chans.ms
wsclean -name KAT-7_12h60s_dec-30_10MHz_10chans_uniform    -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_12h60s_dec-30_10MHz_10chans.ms

#channels
wsclean -name KAT-7_6h60s_dec-30_10MHz_1chans_uniform      -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_6h60s_dec-30_10MHz_1chans.ms
wsclean -name KAT-7_6h60s_dec-30_10MHz_100chans_uniform    -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_6h60s_dec-30_10MHz_100chans.ms

#declination
wsclean -name KAT-7_6h60s_dec30_10MHz_10chans_uniform      -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_6h60s_dec30_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec0_10MHz_10chans_uniform       -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_6h60s_dec0_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-60_10MHz_10chans_uniform     -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_6h60s_dec-60_10MHz_10chans.ms
wsclean -name KAT-7_6h60s_dec-90_10MHz_10chans_uniform     -size 512 512 -scale 0.006 -nosmallinversion -weight uniform KAT-7_6h60s_dec-90_10MHz_10chans.ms

