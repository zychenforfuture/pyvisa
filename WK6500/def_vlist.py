import numpy as np


def V_list_gen(Vstop, Vstart, Vstep, isHys):
    if isHys == 0:
        V_list = np.arange(Vstart, Vstop + Vstep, Vstep)
    else:
        V_list = np.arange(Vstart, Vstop + Vstep, Vstep)
        V_list = np.concatenate((V_list[:-1], V_list[::-1]))
    return V_list


if __name__ == '__main__':
    # The code here will only be executed when this file is run directly
    Vstart = 3
    Vstop = -3
    Vstep = -0.05  # Must be divisible by Vstop - Vstart, preferably divisible by Vstop
    isHys = 1  # 1, measure hysteresis; 0, no hysteresis
    # voltage list generation
    print(V_list_gen(Vstop, Vstart, Vstep, isHys))
