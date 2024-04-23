import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from def_vlist import V_list_gen
from def_flist import F_list_gen
from def_CpG_Sweep_meas import WK6500B_CpG_Sweep_meas
import pyvisa

# Name setting
DevName = 'HZO_CV_4V'
# AC setting
Level = 30e-3  # AC level
Speed = 'MED'  # measurement speed: MAX; FAST; MED; SLOW;

# Sweep loop (inner loop) and Step Loop (outer loop) in a nested for loop
SweepLoop = 'v'  # SweepLoop = 'V' or 'F'

# Frequency step settings
# Freq_list = [1e3, 1e4, 1e5]  # Frequency list
Fstart = 1e5
Fstop = 1e6  # Maximum frequency = 1e6
PointsPerDecade = 1  # number of points per decade
# frequency list generation with uniform distribution in log scale
Freq_list = F_list_gen(Fstart, Fstop, PointsPerDecade)
print(Freq_list)

# Voltage sweep settings
Vstart = -3
Vstop = 3
Vstep = 0.1  # Must be divisible by Vstop - Vstart, preferably divisible by Vstop
isHys = 1  # 1, measure hysteresis; 0, no hysteresis
# voltage list generation
V_list = V_list_gen(Vstop, Vstart, Vstep, isHys)
print(V_list)

Fig = 1  # 1 to plot 0 none

# Impedance sweep measurements
WK6500B_CpG_Sweep_meas(Level, Speed, V_list, Freq_list, DevName, SweepLoop, Fig)
