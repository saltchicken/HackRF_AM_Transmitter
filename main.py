import numpy as np
import hackrf

fs = 8000000
fc = 10000000
# Message signal frequency
fm = 1000

# Time interval
T = 1/fm

# Number of samples
N = T*fs

# Sampling interval
ts = 1/fs

# Time vector
t = np.linspace(0, T, N, endpoint=False)

# Message signal
m = np.sin(2*np.pi*fm*t)

# Carrier signal
c = np.sin(2*np.pi*fc*t)

# Amplitude modulation
y = np.multiply(m, c)

# Normalize the signal
y = y/np.max(y)

# Convert the signal to a signed 8-bit integer
y = (y * 128) + 128
y = y.astype(np.int8)

hackrf = hackrf.HackRF()
hackrf.sample_rate = fs
hackrf.center_freq = fc
hackrf.txvga_gain = 40
hackrf.transmit(y)

hackrf.close()