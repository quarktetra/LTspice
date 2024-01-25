#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt

import os
from scipy import interpolate, signal
import filecmp
from shutil import copyfile
import sys
from PyLTSpice.LTSpice_RawRead import RawRead



def apply_ltspice_filter(simname,sig_in_x,sig_in_y,**kwargs):

  target_dir = os.path.dirname(simname)
  here = os.getcwd()

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



  params  = kwargs.get("params",{})


  if sys.platform == "darwin":
    simname = simname.replace(".cir","")
  else:
    simname = simname.replace(".asc","")



  with open("sig_in.csv_","w") as f:
    for i in range(0,len(sig_in_x)):
      f.write("{:E}\t{:E}\n".format(sig_in_x[i],sig_in_y[i]))
    f.close()

  with open("trancmd.txt_","w") as f:
    f.write(".param transtop {:E}\n".format(sig_in_x[-1]-sig_in_x[0]))
    f.write(".param transtart {:E}\n".format(sig_in_x[0]))
    f.write(".param timestep {:E}\n".format(sig_in_x[1]-sig_in_x[0]))
    f.close()

  with open("param.txt_","w") as f:
    for key in params:
      f.write(".param {:s} {:E}\n".format( key,params[key]  ))
    f.write("\n")
    f.close()


  sth_changed = False

  # check if we ran the simulation before with exact same input, can save time
  if os.path.isfile('sig_in.csv') and filecmp.cmp('sig_in.csv_', 'sig_in.csv') :
    print("sig_in.csv has not changed")
  else:
    sth_changed = True
    copyfile('sig_in.csv_', 'sig_in.csv')

  if os.path.isfile('trancmd.txt') and filecmp.cmp('trancmd.txt_', 'trancmd.txt'):
    print("trancmd.txt has not changed")
  else:
    sth_changed = True
    copyfile('trancmd.txt_', 'trancmd.txt')

  if os.path.isfile('param.txt') and filecmp.cmp('param.txt_','param.txt') :
    print("param.txt has not changed")
  else:
    sth_changed = True
    copyfile('param.txt_','param.txt')


  if os.path.isfile("{:s}.raw".format(simname)): ## raw file already exists
    # get rawfile modification date
    rawmdate = os.path.getmtime("{:s}.raw".format(simname))
    # get ascfile modification date
    ascmdate = os.path.getmtime("{:s}.asc".format(simname))
    if ascmdate > rawmdate: # asc file has been modified in the meantime
      print("{:s}.asc is newer than {:s}.raw".format(simname,simname))
      sth_changed = True
    else:
      print("{:s}.asc is older than {:s}.raw".format(simname,simname))
  else :
    sth_changed = True

  # do not execute ltspice if nothing has changed
  if sth_changed:
    #print("executing ./wine_ltspice.sh, saving STDOUT to wine_ltspice.log")
    #os.system("{:s} {:s}.asc > wine_ltspice.log 2>&1".format(simname))
    if sys.platform == "linux":
      os.system(ltspice_command+" {:s}.asc".format(simname))
    elif sys.platform == "darwin":
      os.system(ltspice_command+" {:s}.cir".format(simname))
    else:
      import subprocess
      subprocess.run([*ltspice_command.split(), "{:s}.asc".format(simname)])

  else:
    print("input data did not change, reading existing .raw file")

  ltr = RawRead("{:s}.raw".format(simname))


  if verbose:
    for name in ltr.get_trace_names():
      for step in ltr.get_steps():
        tr = ltr.get_trace(name)
        print(name)
        print('step {:d} {}'.format(step, tr.get_wave(step)))

  #os.system("./clean_up.sh")
  os.remove("param.txt_")
  os.remove("trancmd.txt_")
  os.remove("sig_in.csv_")

  IR1 = ltr.get_trace("V(vout)")
  x = ltr.get_trace("time")

  #  #### the abs() is a quick and dirty fix for some strange sign decoding errors
  vout_x = abs(x.get_wave(0))
  vout_y = IR1.get_wave(0)

  #  interpolate ltspice output, so you have the same x value spacing as in the input voltage vector
  if interpol:
    f = interpolate.interp1d(vout_x,vout_y, fill_value="extrapolate")
    vout_x = sig_in_x
    vout_y = f(sig_in_x)

  os.chdir(here)
  return (vout_x,vout_y)


##################################################
##             generate test signal             ##
##################################################

# our samples shall be 100 ms wide
sample_width=100e-3
# time step between samples: 0.1 ms
delta_t=0.1e-3
samples = int(sample_width/delta_t)

time = np.linspace(0,sample_width,samples)

# we want 1 V between 10 ms and 30 ms, and 2.5 V between 40 and 70 ms
signal_a = np.cos(1000*time) #0 + 1*((time > 10e-3) * (time < 30e-3)) + 2.5*((time > 40e-3) * (time < 70e-3))



if sys.platform == "darwin":
  """ In order for the command /Applications/LTspice.app/Contents/MacOS/LTspice -b Draft1.cir to work, a netlist file is required."""
  file_extension = "cir"
else:
  file_extension = "asc"



##################################################
##        apply filter - configuration 1        ##
##################################################

# all values in SI units
configuration_1 = {
  "C":100e-6, # 100 uF
  "L":20e-3 # 200 mH
}

dummy, signal_b1 = apply_ltspice_filter(
      f"9_1MHzBP.{file_extension}",
      time, signal_a,
      params=configuration_1
      )



##################################################
##           plot input vs output(s)            ##
##################################################

plt.plot(time,signal_a, label="signal_a (LTSpice input)")
plt.plot(time,signal_b1, label="signal_b1 (LTSpice output, C=100uF, L=200mH)")
plt.xlabel("time (s)")
plt.ylabel("voltage (V)")
plt.ylim((-1,3.5))
plt.grid(True)

plt.legend()
plt.show()
