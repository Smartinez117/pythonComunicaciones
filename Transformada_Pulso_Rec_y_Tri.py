# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:12:41 2024

@author: eneas
"""

import sk_dsp_comm.sigsys as ss
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

# Base de tiempo

Ts = .01
t = np.arange(-10,10,Ts)

# Definicion de señales

x = np.cos(2*np.pi*t)
x_rect_0 = ss.rect(t,1)
x_rect_1 = ss.rect(t+3,2)
x_tri = ss.tri(t,1.5)

# Graficos

plt.figure(10)
plt.subplot(311)
plt.plot(t,x)
plt.grid()
plt.ylabel(r'$cos(2pif_ct)$')
plt.xlabel(r'Time (s)')
plt.subplot(312)
plt.plot(t,x_rect_0,t,x_rect_1)
plt.grid()
plt.xlabel(r'Time (s)')
plt.ylabel(r'$\Pi((t-t_0)/\tau)$')
plt.subplot(313)
plt.plot(t,x_tri)
plt.grid()
plt.xlabel(r'Time (s)')
plt.ylabel(r'$\Lambda((t+t_0)/\tau)$')
plt.grid()
plt.draw()
#tight_layout()

#%% Hacemos las FFT

# definimos eje de frecuencia

f = t = np.linspace(-0.5,0.5,len(t))*(1/Ts)

# Utilizamos la fft 

X = np.fft.fft(x)
X_0 = np.fft.fft(x_rect_0)
X_1 = np.fft.fft(x_rect_1)
X_2 = np.fft.fft(x_tri)

# Graficos

plt.figure(20)
plt.plot(f,np.abs(np.fft.fftshift(X)))
plt.grid()
plt.xlim(-10, 10)
plt.draw()


plt.figure(30)
plt.plot(f,np.abs(np.fft.fftshift(X_0)))
plt.grid()
plt.xlim(-10, 10)
plt.draw()

plt.figure(40)
plt.plot(f,np.abs(np.fft.fftshift(X_1)),f,np.abs(np.fft.fftshift(X_0)))
plt.grid()
plt.xlim(-10, 10)
plt.draw()

plt.figure(50)
plt.plot(f,np.abs(np.fft.fftshift(X_2)))
plt.grid()
plt.xlim(-10, 10)
plt.draw()

