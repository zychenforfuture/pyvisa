import numpy as np
import matplotlib.pyplot as plt
import os
import time
from datetime import datetime
from def_init import WK6500B_init
import pyvisa

def WK6500B_CpG_Sweep_meas(Level, Speed, V_list, Freq_list, DevName, SweepLoop, Fig):
    
    v = WK6500B_init(Speed, Level)
    print(v.query('*IDN?'))

    if SweepLoop.lower() == 'v':
        DataFileName = '_CpG_Vsweep'
        HeaderNum = len(Freq_list)
    else:
        DataFileName = '_CpG_Fsweep'
        HeaderNum = len(V_list)

    DataFolder = './out/'
    os.makedirs(DataFolder, exist_ok=True)

    TimeStamp = datetime.now().strftime('_%Y%m%d_%H_%M_%S')
    F_res = os.path.join(DataFolder, DevName + DataFileName + TimeStamp + '.csv')
    Fig_res = os.path.join(DataFolder, DevName + DataFileName + TimeStamp + '.jpg')

    with open(F_res, 'w') as fid:
        fid.write('V (V), Freq (Hz), C (F), G (S)\n')

    res = []

    if SweepLoop.lower() == 'v':
        # C-V Voltage sweep
        V = np.nan * np.ones((len(V_list), len(Freq_list)))
        F = V.copy()
        C = V.copy()
        G = V.copy()
        for jj in range(len(Freq_list)):

            Freq = Freq_list[jj]
            strM = [str(f) for f in Freq_list]
            for ii in range(len(V_list)):
                Vbias = V_list[ii]
                v.write(':METER:BIAS '+str(Vbias))
                v.write(':METER:FREQ '+str(Freq))
                v.write(':METER:TRIG ONCE')
                meter_data = v.read()
                while meter_data.startswith('No'):
                    time.sleep(1e-5)
                    v.write(':METER:TRIG ONCE')
                    time.sleep(1e-5)
                    meter_data = v.read()
                #print(meter_data)
                CG_str = meter_data.split(',')

                V[ii, jj] = Vbias
                F[ii, jj] = Freq
                C[ii, jj] = float(CG_str[0])
                G[ii, jj] = float(CG_str[1])

                SweepDelay=1e-6
                time.sleep(SweepDelay)


                with open(F_res, 'a') as fid:
                    fid.write('{},{},{},{}\n'.format(V[ii, jj], F[ii, jj], C[ii, jj], G[ii, jj]))

                res.append([V[:, jj], F[:, jj], C[:, jj], G[:, jj]])
        if Fig != 0:
            plt.close('all')
            plt.subplot(1, 2, 1)
            plt.plot(V, C)
            plt.xlabel('V (V)')
            plt.ylabel('C (F)')
            plt.legend(strM)
            plt.subplot(1, 2, 2)
            plt.plot(V, G)
            plt.xlabel('V (V)')
            plt.ylabel('G (S)')
            plt.legend(strM)
            plt.savefig(Fig_res, format='jpeg') # save the figure to file

    else:
        V = np.nan * np.ones((len(V_list), len(Freq_list)))
        F = V.copy()
        C = V.copy()
        G = V.copy()
        for jj in range(len(V_list)):
            Vbias = V_list[jj]
            strM = [str(f) for f in V_list]
            for ii in range(len(Freq_list)):
                Freq = Freq_list[ii]
                v.write(':METER:BIAS '+str(Vbias))
                v.write(':METER:FREQ '+str(Freq))
                v.write(':METER:TRIG ONCE')
                meter_data = v.read()
                while meter_data.startswith('No'):
                    time.sleep(1e-5)
                    v.write(':METER:TRIG ONCE')
                    time.sleep(1e-5)
                    meter_data = v.read()
                #print(meter_data)
                CG_str = meter_data.split(',')

                V[jj, ii] = Vbias
                F[jj, ii] = Freq
                C[jj, ii] = float(CG_str[0])
                G[jj, ii] = float(CG_str[1])

                SweepDelay=1e-6
                time.sleep(SweepDelay)


                with open(F_res, 'a') as fid:
                    fid.write('{},{},{},{}\n'.format(V[jj, ii], F[jj, ii], C[jj, ii], G[jj, ii]))

                res.append([V[jj, :], F[jj, :], C[jj, :], G[jj, :]])
        if Fig != 0:
            plt.close('all')
            plt.subplot(1, 2, 1)
            plt.plot(F, C)
            plt.xlabel('F (Hz)')
            plt.ylabel('C (F)')
            plt.legend(strM)
            plt.subplot(1, 2, 2)
            plt.plot(F, G)
            plt.xlabel('F (Hz)')
            plt.ylabel('G (S)')
            plt.legend(strM)
            plt.savefig(Fig_res, format='jpeg') # save the figure to file

    v.write(':METER:BIAS 0')
    v.write(':METER:BIAS-STAT OFF')
    v.close()

    return res
if __name__ == '__main__':
    Level = 1
    Speed = 1
    V_list = np.linspace(-1, 1, 11)
    Freq_list = np.logspace(1, 6, 6)
    DevName = 'WK6500B'
    SweepLoop = 'v'
    Fig = 1
    res = WK6500B_CpG_Sweep_meas(Level, Speed, V_list, Freq_list, DevName, SweepLoop, Fig)
    print(res)