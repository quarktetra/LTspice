import sys
import os
import filecmp
from shutil import copyfile
import sys
from PyLTSpice import RawRead
import subprocess


def runLTspice(simname):
  target_dir = os.path.dirname(simname)
  #print(target_dir)
  #if( target_dir != ""):
  #  simname = os.path.basename(simname)
  #  os.chdir(target_dir)
  #print(os.getcwd())
  default_ltspice_command = "C:\PROGRA~1\LTC\LTspiceXVII\XVIIx64.exe -Run -b "

  simname = simname.replace(".asc","")
  print(*default_ltspice_command.split(), "{:s}.asc".format(simname))
  subprocess.run([*default_ltspice_command.split(), "{:s}.asc".format(simname)])

runLTspice(f"C:/Users/451516/Documents/github/aLIGOrfPhotoDetectors/LSC RFPD Simulation Files/BluePrints/2S1N.asc")
