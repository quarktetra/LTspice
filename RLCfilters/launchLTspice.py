import sys
import numpy as np
import matplotlib.pyplot as plt

import os
from scipy import interpolate, signal
import filecmp
from shutil import copyfile
import sys
from PyLTSpice import RawRead


def runLTspice(simname,**kwargs):
  theWD = os.getcwd()
  target_dir = os.path.dirname(simname)

  if( target_dir != ""):
    simname = os.path.basename(simname)
    os.chdir(target_dir)

  verbose = kwargs.get("verbose",False)
  interpol = kwargs.get("interpolate",True)

  default_ltspice_command = "C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe -Run -b "
  if sys.platform == "linux":
    default_ltspice_command = 'wine C:\\\\Program\\ Files\\\\LTC\\\\LTspiceXVII\\\\XVIIx64.exe -Run -b '
  elif sys.platform == "darwin":
    default_ltspice_command = '/Applications/LTspice.app/Contents/MacOS/LTspice -b '
  ltspice_command = kwargs.get("ltspice_command",default_ltspice_command)

  if sys.platform == "darwin":
    simname = simname.replace(".cir","")
  else:
    simname = simname.replace(".asc","")

    if sys.platform == "linux":
      os.system(ltspice_command+" {:s}.asc".format(simname))
    elif sys.platform == "darwin":
      os.system(ltspice_command+" {:s}.cir".format(simname))
    else:
      import subprocess
      subprocess.run([*ltspice_command.split(), "{:s}.asc".format(simname)])

  os.chdir(theWD)
runLTspice(f"C:\\Users\\451516\\Documents\\github\\aLIGOrfPhotoDetectors\\LSC RFPD Simulation Files\\BluePrints\\2S1N.asc")