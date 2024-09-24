# -*- coding: utf-8 -*-
"""
Modificado para leer archivos MP3 y convertirlos a WAV usando pydub sin necesidad de FFmpeg en tiempo de ejecución.

@author: eneas (modificado por ChatGPT)
"""

from pydub import AudioSegment  # Para manejar archivos MP3
import scipy.signal as fil      # Módulo para procesamiento de señales
import sounddevice as sd        # Módulo para reproducción de audio
import numpy as np              # Módulo para operaciones matemáticas
import matplotlib.pyplot as plt # Módulo para generar gráficos

# ========================================================================
# Selección del archivo de audio (MP3 o WAV)
# ========================================================================
file_name = input('"C:/Users/Usuario/Music/vlc-record-2024-09-16-13h11m58s-Eternal Struggle.mp3-.mp3"')

# Verificar si el archivo es MP3 o WAV
if file_name.endswith('.mp3'):
    # Usar pydub para convertir el MP3 a WAV en memoria
    audio = AudioSegment.from_mp3(file_name)
    signal = np.array(audio.get_array_of_samples())  # Convertir a array numpy
    Fs = audio.frame_rate  # Obtener la frecuencia de muestreo
    print(f"Archivo MP3 detectado. Frecuencia de muestreo: {Fs} Hz")
else:
    import soundfile as sf  # Importar si es necesario leer WAV directamente
    print(f"Archivo en formato WAV: {file_name}")
    signal, Fs = sf.read(file_name)  # Leer archivo WAV

# ========================================================================
# Recortamos la señal para análisis, opcional según el tamaño del archivo
# ========================================================================
# Si se quiere usar toda la señal, elimina el siguiente recorte:
signal = signal[0:200000]  # Aquí se corta el archivo si es muy largo

# ========================================================================
# Definición de parámetros y configuración de tiempo
# ========================================================================
L = signal.size          # Longitud de la señal
Ts = 1/Fs                # Período de muestreo
t = np.linspace(0, L-1, L) * Ts  # Vector de tiempo basado en la longitud

# ========================================================================
# Configuración de la portadora y normalización de la señal
# ========================================================================
fc = 10e3  # Frecuencia de la portadora (10 kHz)
Am = np.abs(np.min(signal))  # Amplitud máxima de la señal
mn = signal / Am  # Señal normalizada

# ========================================================================
# Transformada de Fourier de la señal de mensaje
# ========================================================================
f = np.linspace(-0.5, 0.5, len(t)) * (1 / Ts)  # Vector de frecuencias
X = np.fft.fft(mn)  # Transformada de Fourier de la señal de mensaje

# ========================================================================
# Gráficos: Señal en el dominio del tiempo y su espectro de frecuencias
# ========================================================================
plt.figure(10)
plt.subplot(211)
plt.plot(t, mn)
plt.title("Señal de mensaje (normalizada)")
plt.grid()

plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(X)))
plt.title("Espectro de la señal de mensaje")
plt.grid()
plt.show()

# ========================================================================
# Modulación en banda lateral única (BLU)
# ========================================================================
kr = 3
Ac = kr * Am  # Amplitud de la portadora
ka = Am / Ac  # Índice de modulación
y = fil.hilbert(mn)  # Generación de la señal de hilbert para BLU

# Oscilador portadora
c = 1 * np.exp(1j * 2 * np.pi * (fc) * t)

# Señal modulada AM (banda lateral única)
xc = np.real(Ac * (y) * c)

# Transformada de Fourier de la señal modulada
Xc = np.fft.fft(xc)

# ========================================================================
# Gráficos: Señal modulada y su espectro de frecuencias
# ========================================================================
plt.figure(20)
plt.subplot(211)
plt.plot(t, xc)
plt.title("Señal modulada en BLU")
plt.grid()

plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(Xc)))
plt.title("Espectro de la señal modulada")
plt.grid()
plt.show()

# ========================================================================
# Demodulación síncrona de la señal
# ========================================================================
fcd = fc  # Frecuencia de demodulación (igual a la portadora)
osr = np.cos(2 * np.pi * (fcd) * t)  # Oscilador local para demodulación

# Multiplicación de la señal modulada por el oscilador (demodulación)
sr = xc * osr
Sc = np.fft.fft(sr)  # Transformada de Fourier de la señal demodulada

# ========================================================================
# Gráficos: Señal demodulada y su espectro de frecuencias
# ========================================================================
plt.figure(30)
plt.subplot(211)
plt.plot(t, sr)
plt.title("Señal demodulada")
plt.grid()

plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(Sc)))
plt.title("Espectro de la señal demodulada")
plt.grid()
plt.show()

# ========================================================================
# Filtro Pasa Bajo para recuperar la señal original
# ========================================================================
# Diseño de un filtro IIR pasa bajo
wp = 5e3  # Frecuencia de paso
ws = 10e3 # Frecuencia de corte
gpass = 1  # Atenuación máxima en la banda de paso (dB)
gstop = 40 # Atenuación mínima en la banda de corte (dB)
system = fil.iirdesign(wp, ws, gpass, gstop, fs=Fs)  # Diseño del filtro

# Aplicación del filtro a la señal demodulada
mrc = fil.lfilter(system[0], system[1], sr)

# Remover DC (desplazamiento de la señal)
Vm0 = np.mean(mrc)
mr = mrc - Vm0  # Señal recuperada

# Transformada de Fourier de la señal recuperada
Mr = np.fft.fft(mr)

# ========================================================================
# Gráficos: Señal recuperada y su espectro de frecuencias
# ========================================================================
plt.figure(40)
plt.subplot(211)
plt.plot(t, mr)
plt.title("Señal recuperada")
plt.grid()

plt.subplot(212)
plt.plot(f, np.abs(np.fft.fftshift(Mr)))
plt.title("Espectro de la señal recuperada")
plt.grid()
plt.show()

# ========================================================================
# Reproducción de la señal recuperada
# ========================================================================
sd.play(mr, Fs)  # Reproducción del audio recuperado
