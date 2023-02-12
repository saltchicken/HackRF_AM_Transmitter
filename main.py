import numpy as np
import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants

fs = 8000000
fc = 10000000
fm = 1000
T = 1/fm
N = T*fs
ts = 1/fs
t = np.linspace(0, T, N, endpoint=False)
m = np.sin(2*np.pi*fm*t)
c = np.sin(2*np.pi*fc*t)
y = np.multiply(m, c)
y = y/np.max(y)

# Convert the signal to a signed 8-bit integer
y = (y * 128) + 128
y = y.astype(np.int8)

# Create an instance of the SoapySDRDevice
sdr = SoapySDR.Device()
sdr.open(dict(driver="hackrf"))
sdr.setSampleRate(SOAPY_SDR_TX, 0, fs)
sdr.setFrequency(SOAPY_SDR_TX, 0, fc)
sdr.setGain(SOAPY_SDR_TX, 0, 40)
txStream = sdr.setupStream(SOAPY_SDR_TX, "CF32")
sdr.activateStream(txStream)
sdr.writeStream(txStream, [y], len(y))
sdr.deactivateStream(txStream)
sdr.closeStream(txStream)
sdr.close()