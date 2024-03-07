import pyvisa
import time

def WK6500B_init(Speed, Level):
    # initiate WK6500B
    # Mode: Cp-G
    # Bias: ON

    rm = pyvisa.ResourceManager()
    v = rm.open_resource('GPIB0::6::INSTR')

    v.write('*CLS;*RST')  # clear a lot
    # Set the output level of the selected bias source.
    v.write(':METER:BIAS-TYPE VOL')  # Select the bias source: Voltage bias.
    v.write(':METER:DISP ABS')  # Select the meter mode display format. Absolute display.
    v.write(':METER:FUNC:1 C;2 G')  # Set to Cp-G
    v.write(':METER:EQU-CCT PAR')  # Select the equivalent circuit. Parallel circuit.
    v.write(':METER:RANGE AUTO')  # Select the measurement ranging setting: Auto-range
    v.write(':METER:SPEED '+str(Speed))  # Select the measurement ranging setting: Auto-range
    v.write(':METER:LEVEL '+str(Level)+'V')  # Select the equivalent circuit. Parallel circuit.
    v.write(':METER:BIAS-STAT ON')  # Change the state of the selected bias source.
    
    time.sleep(0.1)
    
    return v
if __name__ == '__main__':
    Speed = 'MED'  # measurement speed: MAXimum; FAST; MEDium; SLOW;
    Level = 30e-3  # AC level
    v = WK6500B_init(Speed, Level)
    v.query('*IDN?')
    v.write(':METER:BIAS 0')
    v.write(':METER:FREQ 1000')
    print(v.query(':METER:TRIG ONCE'))
    v.write(':METER:BIAS 0')
    v.write(':METER:BIAS-STAT OFF')
    v.close()
    print('WK6500B is initiated')