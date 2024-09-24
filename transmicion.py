import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as fil
import sounddevice as sd

# Parámetros de la simulación
Fs = 100000  # Frecuencia de muestreo
T = 1  # Duración en segundos
t = np.linspace(0, T, int(Fs * T), endpoint=False)  # Vector de tiempo

# Definir una señal de mensaje m(t)
f_m = 5  # Frecuencia de la señal de mensaje (Hz)
m_t = np.sin(2 * np.pi * f_m * t)  # Señal de mensaje

# Parámetros para la portadora
f_c = 1000  # Frecuencia de la portadora (Hz)
A_c = 1  # Amplitud de la portadora

# Función para graficar
def plot_signal(t, signal, title):
    plt.figure(figsize=(10, 4))
    plt.plot(t, signal)
    plt.title(title)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid()
    plt.tight_layout()
    plt.show()

# Mostrar la señal m(t)
plot_signal(t, m_t, 'Señal de Mensaje m(t)')

# Modulación AM
def am_modulate(m_t, A_c):
    return A_c * (1 + m_t) * np.cos(2 * np.pi * f_c * t)

am_signal = am_modulate(m_t, A_c)
plot_signal(t, am_signal, 'Señal AM Modulada')

# Demodulación AM
def am_demodulate(am_signal):
    envelope = np.abs(am_signal)  # Obtener el envolvente
    b, a = fil.butter(5, 2000 / (Fs / 2), btype='low')  # Filtro pasa-bajo
    demodulated_signal = fil.filtfilt(b, a, envelope)
    return demodulated_signal - np.mean(demodulated_signal)  # Centrar en cero

am_demodulated = am_demodulate(am_signal)
plot_signal(t, am_demodulated, 'Señal Demodulada AM')

# Modulación FM
def fm_modulate(m_t, f_c):
    k_f = 50  # Índice de modulación de frecuencia
    return np.cos(2 * np.pi * f_c * t + k_f * m_t)

fm_signal = fm_modulate(m_t, f_c)
plot_signal(t, fm_signal, 'Señal FM Modulada')

# Demodulación FM
def fm_demodulate(fm_signal):
    analytic_signal = fil.hilbert(fm_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    demodulated_signal = np.diff(instantaneous_phase) * Fs / (2.0 * np.pi)
    return np.concatenate(([0], demodulated_signal))  # Agregar un cero al inicio

fm_demodulated = fm_demodulate(fm_signal)
plot_signal(t[:-1], fm_demodulated[:-1], 'Señal Demodulada FM')

# Modulación PM
def pm_modulate(m_t, f_c):
    k_p = np.pi / 2  # Índice de modulación de fase
    return np.cos(2 * np.pi * f_c * t + k_p * m_t)

pm_signal = pm_modulate(m_t, f_c)
plot_signal(t, pm_signal, 'Señal PM Modulada')

# Demodulación PM (usando derivada del ángulo)
def pm_demodulate(pm_signal):
    analytic_signal = fil.hilbert(pm_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    demodulated_signal = np.diff(instantaneous_phase) * Fs / (np.pi / 2)  # Escalar por k_p
    return np.concatenate(([0], demodulated_signal))  # Agregar un cero al inicio

pm_demodulated = pm_demodulate(pm_signal)
plot_signal(t[:-1], pm_demodulated[:-1], 'Señal Demodulada PM')

# Reproducir las señales demoduladas (opcional)
sd.play(am_demodulated, Fs)
sd.wait()  