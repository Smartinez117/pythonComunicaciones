# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 12:41:13 2024
Este codigo permite graficar un coseno en funcion del tiempo, 
tambien permite cambiar las fase.

De este modo podemos entender que en el tiempo 
el coseno y el seno son la misma funcion.

Ademas se agraga una funcion exponencial decreciente, con constante
de tiempo tau que el usuario puede cambiar

Tambien se agrega la relacion de Euler

Una cuestion interesante es la que 
@author: eneas
"""


import numpy as np
import matplotlib.pyplot as plt

# Definicion de Parametros

Ts = 0.01;
fs = 1/Ts;

tiempo_inicial = 0
tiempo_final = 10

N = tiempo_final/Ts

# La función numpy.linspace genera un array NumPy formado por n números equiespaciados entre dos dados

t = np.linspace(0,10,int(N)) # TIEMPO

# Definicion de la Funcion temporal

Tc = 0.001
fc = 1/Tc
fase = np.pi/4

x = 1*np.cos(2*np.pi*(fc)*t - fase)
tau = 3
y = np.exp(-t/tau)
z = x * y


plt.ion()     # Perimte lberar el proceso una ves ejecutado el codigo
plt.plot(t,z,t,y)
plt.grid()
plt.show()




e_1 = (np.exp(1j*2*np.pi*fc*t) + np.exp(-1j*2*np.pi*fc*t))/2

plt.plot(t,(e_1))
plt.grid()
plt.show()