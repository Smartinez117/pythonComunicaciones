# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:52:31 2024

@author: eneas
"""

"""
Created on Wed Aug 23 11:51:50 2023

@author: eneas
"""

import scipy.io.wavfile as wav
import scipy.signal as fil
import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

file_name = 'C:/Users/Usuario/Desktop/comunicaciones/Script PythonMatlab-20240818/a.wav'

signal, Fs = sf.read(file_name)

signal = signal[0:200000,] #/ 32767

#sd.play(signal, Fs)

#%%

L = signal.size
Ts = 1/Fs;
fs = 1/Ts;
t = np.linspace(0,L-1,L)*Ts # TIEMPO

fc = 10e3;   # Configurable
Tc = 1/fc;

Am = np.abs(np.min(signal)) # Muestro este valor

mn = signal/Am

f = np.linspace(-0.5,0.5,len(t))*(1/Ts)
X = np.fft.fft(mn)

#%%
plt.figure(10)
plt.subplot(211)
plt.plot(t,mn)
plt.grid()
plt.draw()
plt.subplot(212)
plt.plot(f,np.abs(np.fft.fftshift(X)))
plt.grid()
plt.draw()
#%% Modulacion BLU

kr = 3
Ac = kr*Am      # Configurable

ka = Am/Ac      # Indice de Modulacion
y = fil.hilbert(mn)
# oscilador
c = 1*np.exp(1j*2*np.pi*(fc)*t)
# señal AM
xc = np.real(Ac*(y)*c)

Xc = np.fft.fft(xc)
#%%
#sd.play(xc, Fs)
#%%
plt.figure(20)
plt.subplot(211)
plt.plot(t,xc)
plt.grid()
plt.draw()
plt.subplot(212)
plt.plot(f,np.abs(np.fft.fftshift(Xc)))
plt.grid()
plt.draw()

#%%
# Demodulacion sincronica

fcd = fc # configurable
osr = np.cos(2*np.pi*(fcd)*t);
sr = xc*osr;
Sc = np.fft.fft(sr)
#%%
#sd.play(sr, Fs)
#%%
plt.figure(30)
plt.subplot(211)
plt.plot(t,sr)
plt.grid()
plt.draw()
plt.subplot(212)
plt.plot(f,np.abs(np.fft.fftshift(Sc)))
plt.grid()
plt.draw()

#%%

# Filtro Pasa Bajo
wp = 5e3
ws = 10e3
gpass = 1
gstop = 40
system = fil.iirdesign(wp, ws, gpass, gstop, fs = Fs)
w, h = fil.freqz(*system)

mrc = fil.lfilter(system[0],system[1],sr)

Vm0 = np.mean(mrc);

mr = mrc - Vm0      # mensage recivido

Mr = np.fft.fft(mr)

#%%
plt.figure(40)
plt.subplot(211)
plt.plot(t,mr)
plt.grid()
plt.draw()
plt.subplot(212)
plt.plot(f,np.abs(np.fft.fftshift(Mr)))
plt.grid()
plt.draw()
#%%
sd.play((mr), Fs)

#%%
