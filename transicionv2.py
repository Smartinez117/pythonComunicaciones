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

# Modulación AM
def am_modulate(m_t, A_c):
    return A_c * (1 + m_t) * np.cos(2 * np.pi * f_c * t)

am_signal = am_modulate(m_t, A_c)

# Demodulación AM
def am_demodulate(am_signal):
    envelope = np.abs(am_signal)  # Obtener el envolvente
    b, a = fil.butter(5, 2000 / (Fs / 2), btype='low')  # Filtro pasa-bajo
    demodulated_signal = fil.filtfilt(b, a, envelope)
    return demodulated_signal - np.mean(demodulated_signal)  # Centrar en cero

am_demodulated = am_demodulate(am_signal)

# Modulación FM
def fm_modulate(m_t, f_c):
    k_f = 50  # Índice de modulación de frecuencia
    return np.cos(2 * np.pi * f_c * t + k_f * m_t)

fm_signal = fm_modulate(m_t, f_c)

# Demodulación FM
def fm_demodulate(fm_signal):
    analytic_signal = fil.hilbert(fm_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    demodulated_signal = np.diff(instantaneous_phase) * Fs / (2.0 * np.pi)
    return np.concatenate(([0], demodulated_signal))  # Agregar un cero al inicio

fm_demodulated = fm_demodulate(fm_signal)

# Modulación PM
def pm_modulate(m_t, f_c):
    k_p = np.pi / 2  # Índice de modulación de fase
    return np.cos(2 * np.pi * f_c * t + k_p * m_t)

pm_signal = pm_modulate(m_t, f_c)

# Demodulación PM (usando derivada del ángulo)
def pm_demodulate(pm_signal):
    analytic_signal = fil.hilbert(pm_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    demodulated_signal = np.diff(instantaneous_phase) * Fs / (np.pi / 2)  # Escalar por k_p
    return np.concatenate(([0], demodulated_signal))  # Agregar un cero al inicio

pm_demodulated = pm_demodulate(pm_signal)

# Función para graficar todas las señales en una sola figura
def plot_signals_am_fm_pm(m_t, am_signal, am_demodulated,
                           fm_signal, fm_demodulated,
                           pm_signal, pm_demodulated):
    plt.figure(figsize=(15, 12))

    # Gráficas para AM
    plt.subplot(321)  # Subplot para m(t)
    plt.plot(t, m_t)
    plt.title('Señal de Mensaje m(t)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid()

    plt.subplot(322)  # Subplot para AM Modulada
    plt.plot(t, am_signal)
    plt.title('Señal AM Modulada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid()

    plt.subplot(323)  # Subplot para AM Demodulada
    plt.plot(t, am_demodulated)
    plt.title('Señal Demodulada AM')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid()

    # Gráficas para FM
    plt.subplot(324)  # Subplot para FM Modulada
    plt.plot(t, fm_signal)
    plt.title('Señal FM Modulada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid()

    plt.subplot(325)  # Subplot para FM Demodulada
    plt.plot(t[:-1], fm_demodulated[:-1])  # Ajustar el tiempo para demodulación
    plt.title('Señal Demodulada FM')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid()

    # Gráficas para PM
    plt.subplot(326)  # Subplot para PM Modulada
    plt.plot(t, pm_signal)
    plt.title('Señal PM Modulada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid()

    # Ajustar el diseño y mostrar la figura completa
    plt.tight_layout()
    plt.show()

# Mostrar todas las señales en una sola figura ahora que tenemos los datos completos.
plot_signals_am_fm_pm(m_t=m_t,
                       am_signal=am_signal,
                       am_demodulated=am_demodulated,
                       fm_signal=fm_signal,
                       fm_demodulated=fm_demodulated,
                       pm_signal=pm_signal,
                       pm_demodulated=pm_demodulated)

# Reproducir las señales demoduladas (opcional)
sd.play(am_demodulated, Fs)
sd.wait()  