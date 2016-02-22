#!/bin/bash

#original data: jake:/home/makhathini/griffin/msdir/*.ms

wsclean -name KAT-7_6h60s_dec-30_10MHz_10chans_uniform_n100 -size 512 512 -scale 0.006 -nosmallinversion -weight uniform -niter 100 KAT-7_6h60s_dec-30_10MHz_10chans.ms
