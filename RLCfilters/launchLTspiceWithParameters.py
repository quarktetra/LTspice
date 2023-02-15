# Modified from: https://github.com/acidbourbon/numpy_ltspice_filter
# this codes simply executes LTspice on a .asc file

import sys
import numpy as np
import matplotlib.pyplot as plt

import os
from scipy import interpolate, signal
import filecmp
from shutil import copyfile
import sys
from PyLTSpice.LTSpice_RawRead import RawRead


def runLTspice(simname,**kwargs):
  theWD = os.getcwd()
  target_dir = os.path.dirname(simname)
  print(target_dir)
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




params = {
  "C1":"174p",
  "L1": "1800n",
  "pointsPerDecade": "100" ,
  "freqStop":"100Meg",
   "freqStart": "1Meg"
}

with open("paramE.txt","w") as f:
    for key in params:
      f.write(".param {:s} {:s}\n".format( key,params[key]  ))
    f.write("\n")
    f.close()


fileName="9_1MHzBPwithExtParam"
runLTspice(fileName+".asc")
filepath = fileName+'.raw'     # will have several columns. We are interested in  frequency and V(vout9.1)
LTR = RawRead(filepath)

print(LTR.get_trace_names())
#print(LTR.get_raw_property())

xa= LTR.get_trace("frequency")
xa=np.asarray(xa).real      # converting to np for later analysis
ya= LTR.get_trace("V(vout9.1)")
ya=np.asarray(ya)   # this is in complex form, cartesian apparently
ya=np.abs(ya)

plt.plot(xa, ya)    #Amplitude vs Freq.
plt.grid(True, which="both", ls="-")
plt.xscale('log')
plt.xlabel("Frequency(Hz)")
plt.ylabel("Gain")
plt.title("Frequency responce of the BandPass filter C1:" +params["C1"]+"; L1:" +params["L1"])
plt.savefig('9_1MHzBP_freq_response_withParameters.png', dpi=300)

plt.show()

