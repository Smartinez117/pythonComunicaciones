# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 12:45:28 2024

@author: eneas
"""

# Importar librerias basicas
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

#matplotlib inline
plt.style.use('bmh') # estilo de las graficas
from IPython.display import Latex # para visualizar ecuaciones en jupyter
from scipy import signal as sp


amplitud = 1
periodo = np.pi


t = np.arange(-1, 10, 0.001)
funcion = ((sp.square(2 * t)) * (amplitud / 2.0)) + (amplitud / 2.0)

plt.plot(t, funcion, lw=2)
plt.grid()
plt.annotate('Pi', xy = (np.pi, 1), xytext = (np.pi, 1.1))
plt.annotate('Pi/2', xy = (np.pi / 2.0, 1), xytext = (np.pi / 2.0, 1.1))
plt.ylabel('Amplitud')
plt.xlabel('Tiempo(t)')
plt.ylim(-1,2)
plt.xlim(-0.5, 4)
plt.show()


import matplotlib.pylab as plt

from sympy import *
#ademas importamos las variables simbolicas 'n' y 't'
from sympy.abc import t, n

ao = integrate(2 / pi, (t, 0, pi / 2))
#integramos la funcion (2/pi) cuya variable es 't'
#y limites de integracion entre 0 y pi/2
print('Coeficientes de la serie de Fourier en forma Trigonometrica')
print("\n"+"a0 = ")
pprint(ao)
#Usamos la funcion pprint para mostrar ao

an = integrate((2 / pi) * cos(2 * n * t), (t, 0, pi / 2))

an = integrate((2 / pi) * cos(2 * n * t), (t, 0, pi / 2))
#integramos la funcion (2/pi)*cos(2nt)
#Su variable es 't' y sus limites de integracion son 0 y pi/2

print ("\n"+"an = ")
pprint(an)
#Usamos la funcion pprint para mostrar an

bn = together(integrate((2 / pi) * sin(2 * n * t), (t, 0, pi / 2)))
#integramos la funcion (2/pi*cos(2nt)
#Su variable es 't' y sus limites de integracion
#son 0 y pi/2. Ademas usamos la funcion "together"
#para simplificar la expresion

print("\n"+"bn = ")
pprint(bn)
#Usamos la funcion pprint para mostrar bn

print("\n"+"f(x) = ")

armonicos = 10
serie = (ao/2)
for i in range(1, armonicos + 1):
    serie = serie + (an*cos(2*n*t)).subs(n, i)
for j in range(1, armonicos + 1):
    serie = serie + (bn*sin(2*n*t)).subs(n, j)

pprint(serie)
#Usando el modulo para graficas de sympy
plotting.plot(serie, ylim=(-0.5, 1.5), xlim=(-0.5,5));

points = [1,2,4,10,30,50]

for ii in points:
    armonicos = ii
    serie = (ao/2)
    for i in range(1, armonicos + 1):
        serie = serie + (an*cos(2*n*t)).subs(n, i)
    for j in range(1, armonicos + 1):
        serie = serie + (bn*sin(2*n*t)).subs(n, j)
    #Usando el modulo para graficas de sympy
    print(f'Numero de terminos = {ii}')
    sym.plotting.plot(serie, ylim=(-0.5, 1.5), xlim=(-0.5,5))