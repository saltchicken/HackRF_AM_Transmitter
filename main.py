import numpy as np
import SoapySDR
from SoapySDR import SOAPY_SDR_TX

sample_rate = 8000000
carrier_freq = 10000000
mod_freq = 1000
mod_period = 1 / mod_freq
sample_count = int(mod_period * sample_rate)
time_step = 1 / sample_rate

time_samples = np.linspace(0, mod_period, sample_count, endpoint=False)
mod_signal = np.sin(2 * np.pi * mod_freq * time_samples)
carrier_signal = np.sin(2 * np.pi * carrier_freq * time_samples)
transmit_signal = np.multiply(mod_signal, carrier_signal)
transmit_signal /= np.max(transmit_signal)

# Convert the signal to a signed 8-bit integer
transmit_signal = ((transmit_signal * 128) + 128).astype(np.int8)

sdr_device = SoapySDR.Device({"driver": "hackrf"})
sdr_device.setSampleRate(SOAPY_SDR_TX, 0, sample_rate)
sdr_device.setFrequency(SOAPY_SDR_TX, 0, carrier_freq)
sdr_device.setGain(SOAPY_SDR_TX, 0, 40)
tx_stream = sdr_device.setupStream(SOAPY_SDR_TX, "CF32")
sdr_device.activateStream(tx_stream)
sdr_device.writeStream(tx_stream, [transmit_signal], len(transmit_signal))
sdr_device.deactivateStream(tx_stream)
sdr_device.closeStream(tx_stream)
sdr_device.close()
