# A simple example to read simulation results from LT spice
# Get the asc file here:https://github.com/quarktetra/LTspice/blob/main/RLCfilters/9_1MHzBP.asc
# run the following code in CMD (windows OS):
#"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe" -Run -b 9_1MHzBP.asc
# This will create the   9_1MHzBP.raw file we will use
# 9_1MHzBP.raw is also available here:      https://github.com/quarktetra/LTspice/tree/main/RLCfilters
from PyLTSpice import RawRead    #https://pypi.org/project/PyLTSpice/
import cmath             # dealing with complex numbers
from matplotlib import pyplot as plt
import numpy as np
import os

# make sure the working directory is the one that contains the .asc file.
# if not, you can set below   (requires os)
if False:
    path="path to the directory"
    os.chdir(path)

filepath = '9_1MHzBP.raw'     # will have several columns. We are interested in  frequency and V(vout9.1)
LTR = RawRead(filepath)

print(LTR.get_trace_names())
print(LTR.get_raw_property())

xa= LTR.get_trace("frequency")
xa=np.asarray(xa).real      # converting to np for later analysis
ya= LTR.get_trace("V(vout9.1)")
ya=np.asarray(ya)   # this is in complex form, cartesian apparently
ya=np.abs(ya)

plt.plot(xa, ya)    #Amplitude vs Freq.
plt.grid(True, which="both", ls="-")
plt.xscale('log')
plt.show()

