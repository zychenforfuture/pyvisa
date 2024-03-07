import numpy as np

def F_list_gen(Fstart, Fstop, PointsPerDecade):
    Freq_list = np.logspace(np.log10(Fstart), np.log10(Fstop), int(np.log10(Fstop/Fstart)*PointsPerDecade + 1))
    return Freq_list
if __name__ == '__main__':
    # The code here will only be executed when this file is run directly
    Fstart = 1e3
    Fstop = 1e3
    PointsPerDecade = 1
    Freq_list = F_list_gen(Fstart, Fstop, PointsPerDecade)
    print(Freq_list)
    strM = [str(f) for f in Freq_list]
    print(strM)