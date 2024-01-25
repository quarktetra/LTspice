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
import pandas as pd
df = pd.DataFrame()

# make sure the working directory is the one that contains the .asc file.
# if not, you can set below   (requires os)
if True:
    path="C:/Users/451516/Documents/github/aLIGOrfPhotoDetectors/LSC RFPD Simulation Files/BluePrints/"
    os.chdir(path)

filepath = '9_1MHzBP.raw'     # will have several columns. We are interested in  frequency and V(vout9.1)
LTR = RawRead(filepath)

traces= LTR.get_trace_names()
print(traces)

df['de']=  np.array(LTR.get_trace(traces[0]) )
for trace in traces:
    df[trace] =np.array(LTR.get_trace(trace) )
#print(LTR.get_raw_property())

df.to_csv('2S1N.csv')
print(df)

