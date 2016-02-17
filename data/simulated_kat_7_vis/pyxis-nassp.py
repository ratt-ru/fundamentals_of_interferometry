import Pyxis
from Pyxis.ModSupport import *
import ms
import mqt
import lsm
import glob
import sys
import tempfile

MSDIR = "msdir"
makedir(MSDIR)

ANTENNAS = "observatories/KAT7_ANTENNAS"

MS_List = glob.glob("%s/*.MS"%MSDIR)

DEC_List = [-90, -60, -30, 0, 30] # in Deg
SYNTHESIS_List = [0.167, 1.5, 6, 16] # in Hr
NCHAN_List = [1, 10, 100]

DFREQ = "10MHz"
FREQ0 = "1440MHz"
NCHAN = 10
DEC = -30
SYNTHESIS = 6

LSMREF = "skymodel-nassp.lsm.html"


def simulate():

    direction = "J2000,0deg,%fdeg"%DEC
    v.MS = II("${MSDIR}/KAT-7_${SYNTHESIS}h60s_${DEC}_${DFREQ}_${NCHAN}chans.ms")

    ms.create_empty_ms(msname=MS, freq0=FREQ0, dfreq=DFREQ, nchan=NCHAN, synthesis=SYNTHESIS,
                       dtime=60, direction=direction, pos=ANTENNAS, tel="kat-7")


    tfile = tempfile.NamedTemporaryFile(suffix=".lsm.html")
    tfile.flush()

    tname = tfile.name
    x.sh("tigger-convert --recenter=$direction $LSMREF $tname -f")

    v.LSM = tname

    mqt.msrun(II("${mqt.CATTERY}/Siamese/turbo-sim.py"),
             job = '_tdl_job_1_simulate_MS',
             section = "sim",
             args = ["${lsm.LSM_TDL}"]) 
    
    tfile.close()


def decs():
    pper("DEC", simulate)


def times():
    pper("SYNTHESIS", simulate)


def chans():
    pper("NCHAN", simulate)
