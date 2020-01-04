import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

np.random.seed(6)
sampleRate = 10
cutoff = 2
noise = True
hpf = False
lpf = False
integral = True
derivative = True
velocity = True
displacement = True
t = np.arange(0, sampleRate, 0.1)
s = np.sin(t)
#c = -np.cos(t)

if noise:
    s += + np.random.normal(0, 100, t.shape)
plt.plot(t, s)
#plt.plot(t, c)

if hpf:
    b, a = signal.butter(1, 2*cutoff/sampleRate, btype='high')
    s = signal.filtfilt(b, a, s)
    plt.plot(t, s)

if lpf:
    b, a = signal.butter(1, 2*cutoff/sampleRate, btype='low')
    s = signal.filtfilt(b, a, s)
    plt.plot(t, s)

if velocity:
    v = np.zeros_like(s)
    for i, val in enumerate(s):
        v[i] = np.trapz(s[0:i], t[0:i])
    plt.plot(t, v)

if displacement:
    d = np.zeros_like(v)
    for i, val in enumerate(v):
        d[i] = np.trapz(v[0:i], t[0:i])
    plt.plot(t, d)

rms = 1
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid(True, which='both')


plt.show()