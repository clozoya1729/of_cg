# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import signal
#
# np.random.seed(6)
# sampleRate = 10
# cutoff = 2
# noise = True
# hpf = True
# lpf = True
# integral = True
# derivative = True
# velocity = False
# displacement = False
# t = np.arange(0, sampleRate, 0.1)
# s = np.sin(t)
# #c = -np.cos(t)
#
# if noise:
#     s += + np.random.normal(0, 100, t.shape)
# plt.plot(t, s)
# #plt.plot(t, c)
#
# if hpf:
#     b, a = signal.butter(1, 2*cutoff/sampleRate, btype='high')
#     s = signal.filtfilt(b, a, s)
#     plt.plot(t, s)
#
# if lpf:
#     b, a = signal.butter(1, 2*cutoff/sampleRate, btype='low')
#     s = signal.filtfilt(b, a, s)
#     plt.plot(t, s)
#
# if velocity:
#     v = np.zeros_like(s)
#     for i, val in enumerate(s):
#         v[i] = np.trapz(s[0:i], t[0:i])
#     plt.plot(t, v)
#
# if displacement:
#     d = np.zeros_like(v)
#     for i, val in enumerate(v):
#         d[i] = np.trapz(v[0:i], t[0:i])
#     plt.plot(t, d)
#
# rms = 1
# plt.xlabel('Time')
# plt.ylabel('Amplitude')
# plt.grid(True, which='both')
#
#
# plt.show()

import random
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

signalFrequency = np.pi
samps = 50
axOffset = 5

integrate = False
noise = True
lpf = True
hpf = False

fig, ax = plt.subplots(1, 1)
sinegraph, = ax.plot([], [])
lowpassGraph, = ax.plot([], [])
integralGraph, = ax.plot([], [])
ax.set_ylim([- 20,  20])

X = np.linspace(0, signalFrequency, samps)
V = np.zeros_like(X)
F1 = np.zeros_like(X)
D = np.zeros_like(V)
Dsum = 0


if integrate:
    for j, val in enumerate(V):
        D[j] = np.trapz(V[0:j], X[0:j])


def sine(q):
    i = q
    global V
    global Dsum
    Xx = 5*np.linspace(i, i + signalFrequency, samps)
    X[:-1] = X[1:]
    X[-1] = Xx[-1]
    V[:-1] = V[1:]
    V[-1] = np.sin(i)
    if noise:
        V[-1] += random.randint(-1000, 1000) / 1000
    if lpf:
        b, a = signal.butter(1, 2*1/signalFrequency, btype='high')
        F1 = signal.filtfilt(b, a, V)
        lowpassGraph.set_data(X, F1)
    if integrate:
        Dsum += np.trapz(V[-2:], X[-2:])
        D[:-1] = D[1:]
        D[-1] = Dsum
        integralGraph.set_data(X, D)
    sinegraph.set_data(X, V)
    ax.set_xlim([X[0] - axOffset, X[-1] + signalFrequency + axOffset])


anim = animation.FuncAnimation(fig, sine, interval=100)
plt.grid(True, which='both')

plt.show()
