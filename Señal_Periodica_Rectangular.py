# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:03:32 2024

@author: eneas
"""

import numpy as np
import matplotlib.pyplot as plt




# Caracteristicas de la señal periodica
T = 10
f0 = 1/T

# Caracteristicas de la funcion generatris
tau = 10/4
t0 = tau/2

A = 1


Ncof = 10
Xn = []
i = 0
for n in range(-Ncof, Ncof+1):
    Xnn = (A*tau/T)*np.sinc(n*f0*tau)*np.exp(-1j*2*np.pi*n*f0*t0)
    Xn.append(Xnn)

arreglo = np.array(Xn)    
    
x = np.linspace(-Ncof, Ncof,len(Xn))*f0

t = np.linspace(0, 100,400)
xa = []
sig = []

for n in range(-Ncof, Ncof+1):
    sig = np.exp(-1j*2*n*np.pi*f0*t)
    xa.append(sig)

arregloa = np.array(xa) 
Sa = []

resultado = arreglo[:, np.newaxis] * arregloa

suma_columnas = np.sum(resultado, axis=0)

fig, axs = plt.subplots(3, 1, layout='constrained')

axs[0].stem(x,np.abs(Xn))
axs[0].set_xlabel("Frecuencia")
axs[0].set_ylabel('$|X_{n}|$')
axs[0].grid()

axs[1].stem(x,np.unwrap(np.angle(Xn,deg=False),period=T))
axs[1].set_xlabel("Frecuencia")
axs[1].set_ylabel('$|X_{n}|$')
axs[1].grid()

   
axs[2].plot(t,suma_columnas)    
axs[2].set_xlabel("Tiempo")
axs[2].set_ylabel('$Señal(t)_{aproximada}$')
axs[2].grid()
  