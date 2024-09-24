import scipy.io.wavfile as wav
import scipy.signal as fil
import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Cambia el backend si es necesario
matplotlib.use('TkAgg')

file_name = 'C:/Users/Usuario/Desktop/comunicaciones/Script PythonMatlab-20240818/a.wav'

signal, Fs = sf.read(file_name)

# Toma solo un canal (por ejemplo, el izquierdo)
signal = signal[0:200000, 0]  # Selecciona solo el primer canal

L = signal.size
Ts = 1/Fs;
fs = 1/Ts;
t = np.linspace(0,L-1,L)*Ts  # Vector de tiempo ajustado

fc = 10e3;   # Configurable
Tc = 1/fc;

Am = np.abs(np.min(signal))  # Muestro este valor

mn = signal/Am

f = np.linspace(-0.5,0.5,len(t))*(1/Ts)
X = np.fft.fft(mn)

# Crear una figura para todas las gráficas
plt.figure(figsize=(12, 10))

# Graficar la señal normalizada y su espectro
plt.subplot(321)  # 3 filas, 2 columnas, primer subplot
plt.plot(t, mn)
plt.title('Señal Normalizada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()

plt.subplot(322)  # Segundo subplot
plt.plot(f, np.abs(np.fft.fftshift(X)))
plt.title('Espectro de la Señal Normalizada')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid()

# Resto del código sin cambios...
kr = 3
Ac = kr*Am      # Configurable

ka = Am/Ac      # Indice de Modulacion
y = fil.hilbert(mn)
# oscilador
c = 1*np.exp(1j*2*np.pi*(fc)*t)
# señal AM
xc = np.real(Ac*(y)*c)

Xc = np.fft.fft(xc)

# Graficar la señal AM y su espectro
plt.subplot(323)  # Tercer subplot
plt.plot(t, xc)
plt.title('Señal AM')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()

plt.subplot(324)  # Cuarto subplot
plt.plot(f, np.abs(np.fft.fftshift(Xc)))
plt.title('Espectro de la Señal AM')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid()

# Demodulacion sincronica
fcd = fc # configurable
osr = np.cos(2*np.pi*(fcd)*t);
sr = xc*osr;
Sc = np.fft.fft(sr)

# Graficar la señal demodulada y su espectro
plt.subplot(325)  # Quinto subplot
plt.plot(t, sr)
plt.title('Señal Demodulada')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()

plt.subplot(326)  # Sexto subplot
plt.plot(f, np.abs(np.fft.fftshift(Sc)))
plt.title('Espectro de la Señal Demodulada')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid()

# Mostrar todas las gráficas juntas al final
plt.tight_layout()  # Ajusta los subplots para que no se superpongan
plt.show()  # Mostrar la figura

# Filtro Pasa Bajo
wp = 5e3
ws = 10e3
gpass = 1
gstop = 40
system = fil.iirdesign(wp, ws, gpass, gstop, fs=Fs)
mrc = fil.lfilter(system[0], system[1], sr)

Vm0 = np.mean(mrc);
mr = mrc - Vm0      # mensaje recibido

Mr = np.fft.fft(mr)

# Graficar el mensaje recibido y su espectro en una nueva figura
plt.figure(figsize=(12, 5))
plt.subplot(211)
plt.plot(t,mr)
plt.title('Mensaje Recibido')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid()

plt.subplot(212)
plt.plot(f,np.abs(np.fft.fftshift(Mr)))
plt.title('Espectro del Mensaje Recibido')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.grid()

# Mostrar la figura del mensaje recibido y su espectro
plt.tight_layout()
plt.show()  

# Reproducir el mensaje recibido al final del procesamiento.
sd.play(mr, Fs)  
sd.wait()  # Espera a que termine la reproducción antes de continuar.