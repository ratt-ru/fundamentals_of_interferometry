#!/bin/bash

#original data: fundamentals_of_interferometry/data/simulated_kat_7_vis/simulated_KAT-7_ms.tar.gz

#NOTE: this script path needs to be updated
UVSCRIPT=fundamentals_of_interferometry/5_Imaging/scripts/plotUVcoverage.py

#Obs length
$UVSCRIPT -l 1000 -f KAT-7_0.167h60s_dec-30_10MHz_10chans.ms -s KAT-7_0.167h60s_dec-30_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_2h60s_dec-30_10MHz_10chans.ms     -s KAT-7_2h60s_dec-30_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_4h60s_dec-30_10MHz_10chans.ms     -s KAT-7_4h60s_dec-30_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_6h60s_dec-30_10MHz_10chans.ms     -s KAT-7_6h60s_dec-30_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_8h60s_dec-30_10MHz_10chans.ms     -s KAT-7_8h60s_dec-30_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_10h60s_dec-30_10MHz_10chans.ms    -s KAT-7_10h60s_dec-30_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_12h60s_dec-30_10MHz_10chans.ms    -s KAT-7_12h60s_dec-30_10MHz_10chans.png

#channels
$UVSCRIPT -l 1000 -f KAT-7_6h60s_dec-30_10MHz_1chans.ms   -s KAT-7_6h60s_dec-30_10MHz_1chans.png
$UVSCRIPT -l 1000 -f KAT-7_6h60s_dec-30_10MHz_100chans.ms -s KAT-7_6h60s_dec-30_10MHz_100chans.png

#declination
$UVSCRIPT -l 1000 -f KAT-7_6h60s_dec30_10MHz_10chans.ms  -s KAT-7_6h60s_dec30_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_6h60s_dec0_10MHz_10chans.ms   -s KAT-7_6h60s_dec0_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_6h60s_dec-60_10MHz_10chans.ms -s KAT-7_6h60s_dec-60_10MHz_10chans.png
$UVSCRIPT -l 1000 -f KAT-7_6h60s_dec-90_10MHz_10chans.ms -s KAT-7_6h60s_dec-90_10MHz_10chans.png

