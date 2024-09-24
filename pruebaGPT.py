import scipy.signal as fil
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
Fs = 44100  # Frecuencia de muestreo (44.1 kHz, típico para audio)
duration = 5  # Duración de la señal en segundos
t = np.linspace(0, duration, int(Fs * duration), endpoint=False)  # Vector de tiempo

# Generación de una señal de prueba (por ejemplo, una onda sinusoidal)
frequency = 1000  # Frecuencia de la señal sinusoidal (1 kHz)
Am = 0.5  # Amplitud de la señal
signal = Am * np.sin(2 * np.pi * frequency * t)  # Señal sinusoidal

# Procesamiento de la señal
L = signal.size
Ts = 1 / Fs
fc = 10e3  # Frecuencia de la portadora (10 kHz)
Tc = 1 / fc

mn = signal / Am  # Normalización de la señal

f = np.linspace(-0.5, 0.5, len(t)) * (1 / Ts)
X = np.fft.fft(mn)

# Plot de la señal original y su transformada
plt.figure(10)
plt.subplot(211)
plt.plot(t, mn)
plt.grid()
plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(X)))
plt.grid()
plt.show()

# Modulacion BLU
kr = 3
Ac = kr * Am  # Amplitud de la portadora

ka = Am / Ac  # Índice de Modulación
y = fil.hilbert(mn)
# Oscilador
c = 1 * np.exp(1j * 2 * np.pi * (fc) * t)
# Señal AM
xc = np.real(Ac * (y) * c)

Xc = np.fft.fft(xc)

# Plot de la señal modulada y su espectro
plt.figure(20)
plt.subplot(211)
plt.plot(t, xc)
plt.grid()
plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(Xc)))
plt.grid()
plt.show()

# Demodulación síncrona
fcd = fc  # Frecuencia de demodulación (igual a la portadora)
osr = np.cos(2 * np.pi * (fcd) * t)
sr = xc * osr
Sc = np.fft.fft(sr)

# Plot de la señal demodulada y su espectro
plt.figure(30)
plt.subplot(211)
plt.plot(t, sr)
plt.grid()
plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(Sc)))
plt.grid()
plt.show()

# Filtro Pasa Bajo para recuperar la señal original
wp = 5e3 / (Fs / 2)  # Frecuencia de paso normalizada
ws = 10e3 / (Fs / 2)  # Frecuencia de corte normalizada
gpass = 1  # Atenuación máxima en la banda de paso (dB)
gstop = 40  # Atenuación mínima en la banda de corte (dB)
system = fil.iirdesign(wp, ws, gpass, gstop)
w, h = fil.freqz(*system)

mrc = fil.lfilter(system[0], system[1], sr)

Vm0 = np.mean(mrc)

mr = mrc - Vm0  # Mensaje recuperado

Mr = np.fft.fft(mr)

# Plot de la señal recuperada y su espectro
plt.figure(40)
plt.subplot(211)
plt.plot(t, mr)
plt.grid()
plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(Mr)))
plt.grid()
plt.show()

# Reproducción de la señal recuperada
sd.play(mr, Fs)
