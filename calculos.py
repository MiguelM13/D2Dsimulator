import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
from signals import *


def calculate_throughput(SNRI):
    throughput = 0
    for i in range(len(SNRI)):
        try:
            throughput += np.log2(1 + SNRI[i])
        except:
            throughput += 0
    return throughput


def channel_capacity_OFDMA(SINR=0, BWvec=None):
    """Calcular capacidad de canal
    SINR: Relación señal a ruido más interferencia
    BWvec: lista con anchos de banda asignados
    """
    s = 0
    yi = None
    if BWvec:
        # Tsc = len(BWvec)
        for bwscn in BWvec:
            s += bwscn
        yi = np.log2(1 + SINR) * s
    return yi


def calcule_satisfaction(Y, D):
    """Calcular satisfaccion
    Args:
        Y: Capacidad del canal de Shanon (vector/Lista)
        D: Demanda de usuario (vector/Lista)
    """
    n = len(Y)
    sat = 0
    for i in range(0, n):
        sat += Y[i] / D[i]
    sat = (100 / n) * sat
    return sat


def calculate_SNR(Psc=None, PLsc=None, No=-174):
    """Calcular el SNR de un cierto usuario i
    Args:
        SNRi: Relación señal-ruido para el usuario i
        Psc: (list) Potencia asignada a la subportadora SCn del usuario i
        PLsc: (list) Pérdida por trayectoria de la subportadora SC del usuario i
        No: Potencia de Ruido dBm/Hz
    Returns:
        SNR: Relación señal a ruido
    """
    SNR = 0
    if Psc and PLsc:
        # Número de subportadoras
        if len(Psc) == len(PLsc):
            Tsc = len(Psc)
            for n in range(Tsc):
                SNR += Psc[n] / (PLsc[n] * No)
        else:
            raise Exception('Psc and PLsc must have same dimension...')
    else:
        SNR = None
    return SNR


def calculate_interference_cotier(Pj=None, PLsc=56, No=-174):
    """Calcula la interferencia co-tier
    Args:
        Pj: (list) Potencia de subportadores iguales a usuario i
        PLsc: Pérdida por trayectoria de la subportadora SC del usuario i
        No: Potencia de Ruido dBm/Hz
    Returns:
        I: Interferencia co-tier
    """
    I = 0
    if Pj is not None and PLsc is not None:
        # Número de subportadoras
        if len(Pj) > 0:
            Tsc = len(Pj)
            for n in range(Tsc):
                if PLsc != 0:
                    I += Pj[n] / (PLsc * No)
                else:
                    I = 0
        else:
            raise Exception('Psc and PLsc must have same dimension...')
    else:
        I = None
    return I


def calculate_SINR(Psc=None, PLsc=None, I=None, No=-174):
    """Calcular el SNR de un cierto usuario i
    Args:
        SINR: Relación señal-ruido añadida interferencia para el usuario i
        Psc: (list) Potencia asignada a la subportadora SCn del usuario i
        PLsc: (list) Pérdida por trayectoria de la subportadora SC del usuario i
        No: Potencia de Ruido dBm/Hz
    Returns:
        SNR: Relación señal a ruido
    """
    SINR = 0
    if Psc is not None and PLsc is not None and I is not None:
        # Número de subportadoras
        if len(Psc) == len(PLsc):
            Tsc = len(Psc)
            for n in range(Tsc):
                if PLsc[n] != 0:
                    SINR += Psc[n] / (PLsc[n] * (No + I))
                else:
                    SINR = 0
        else:
            raise AssertionError('Psc and PLsc must have same dimension...')
    else:
        SINR = None
    return SINR


def propagation_losses(d=5.0, units="m", alpha=3, fc=2400, model="D2D"):
    """Cálculo de pérdidas de propagación
    Args:
        d: distancia en kilómetros (Km)
        units: Unidades "m" o "km"
        fc :Frecuencia de portadora (MHz)
        alpha: Factor de atenuación
        model: model of propagation losses
    Returns:
        PL: pèrdidas por propagación
    """
    if units == "m":
        d = d / 1000
    elif units == "km":
        pass
    else:
        raise AssertionError("Not valid units")
    # Macrocelda
    if d != 0:
        if model == "MC":
            PL = 10 * np.log10(d ** alpha) + 30 * np.log10(fc) + 49
        # Femtocelda
        if model == "FC":
            PL = 10 * np.log10(d ** alpha) + 37
        # D2D
        if model == "D2D":
            PL = 40 * np.log10(d) + 148
        return PL
    else:
        PL = 0
    return PL


def subcarrier_power(d=5.0, units="m", alpha=3, RSRP=-75, dB=True, model="D2D"):
    """Estima la potencia de la subportadora
    Args:
        d: distancia
        units: str, unidades "m" o "km"
        RSRP: Potencia recibida de señal de referencia -75dBm y -88dBm
        dB: si es True retorna Psc en dBm, sino retorna en mW
    Returns:
        Psc: Potencia de subportadora mW/dBm
    """
    PL = propagation_losses(d=d, units=units, alpha=alpha, model=model)
    Psc = RSRP + PL
    if not dB:
        Psc = 10 ** (Psc / 10)
    return Psc


def to_mw(dBm):
    return 10 ** (dBm / 10)


def interpolate_points(x=None, y=None):
    if x is None:
        x = [i for i in range(len(y))]
    y_inter = InterpolatedUnivariateSpline(x, y)
    return y_inter


def plot_signals(t=None, signals=None, prefix="", vec=None, xlabel="", ylabel="", title="", grid=True, legend=True):
    plt.figure()
    i = 0
    for signal in signals:
        if vec is None:
            if t is None:
                plt.plot(signal, label=prefix+str(i))
            else:
                plt.plot(t, signal, label=prefix+str(i))
        else:
            if t is None:
                plt.plot(signal, label=prefix + str(vec[i]))
            else:
                plt.plot(t, signal, label=prefix + str(vec[i]))
        i += 1
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(grid)
    if legend:
        plt.legend()


def plot_signal(signal=None, xlabel="", ylabel="", title="", grid=True, t=None):
    plt.figure()
    if t is None:
        plt.plot(signal)
    else:
        plt.plot(t, signal)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(grid)


def plot2(t=None, x1=None, x2=None, name1="", name2="", xlabel="", ylabel="", legend=True, title=""):
    plt.figure()
    if t is None:
        plt.plot(x1, label=name1)
        plt.plot(x2, label=name2)
    else:
        plt.plot(t, x1, label=name1)
        plt.plot(t, x2, label=name2)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if legend:
        plt.legend()
    plt.grid(True)
    plt.title(title)


def throuhgput_signals(signals):
    th = []
    for signal in signals:
        th.append(calculate_throughput(signal))
    return th


def dist(signals):
    values = [1, 3, 7, 8, 9]
    values_norm = np.array(values)/np.max(values)
    s = []
    i = 0
    for signal in signals:
        if i in values:
            norm = np.array(signal)/np.max(signal)
            new = norm + i/np.max(values) - 0.1
            new = np.max(signal)*new
        else:
            new = np.array(signal)
        s.append(new)
        i += 1
    return s


# N = 600
# t = np.linspace(0, 1, N)
# n = 10
# offset = [i+1 for i in range(n)]
# signals = [0.01*np.sin(2*np.pi*2*t) + 0.01*offset[i] for i in range(n)]
# th = throuhgput_signals(signals)
# s2 = dist(signals)
# plot_signals(signals)
# plot_signals(s2)
# th2 = throuhgput_signals(s2)
# plt.figure()
# plt.plot(th)
# plt.plot(th2)
# plt.show()


# N = 50
# t = np.linspace(-3, 3, N)
# y = 0.1 * np.random.randn(N)
# y1 = interpolate_points(x=t, y=y)
# t2 = np.linspace(-3, 3, 1000)
# plt.plot(t, y)
# plt.plot(t2, y1(t2))
# plt.show()
# n = 10
# i = 0
# m = 100
# th_d2d = []
# for j in range(m):
#     if np.random.uniform(0, 100) > 60:
#         i = j - 0.5*np.random.uniform(-2, 2)
#     else:
#         i = j + 2*np.random.uniform(-2, 2)
#     th_d2d.append(i)
#
# x = np.linspace(0, 1, m)
# th_d2d = np.array(th_d2d)
# th = th_d2d - 0.005*(0.05*x - 10)*(2*x - 30)*(x - 50)*(x + 0)
# snri_d2d = [16.37, 27.45, 41.17, 48.38, 61.87, 65.05, 73.36, 82.15, 87.98, 92.51, 103.36]
# snri = [12.18, 20.36, 29.64, 43.4, 50.366, 51.82, 62.36, 67.681, 72.36, 78.2, 86.15]
# snri_d2d = 0.000125*np.array(snri_d2d)
# snri = 0.000125*np.array(snri)
# n_users = [10*(i + 1) for i in range(len(snri_d2d))]
# snri_int = interpolate_points(x=n_users, y=snri)
# snri_int_d2d = interpolate_points(x=n_users, y=snri_d2d)
#
# th_d2d = calculate_throughput(snri_d2d)
# th = calculate_throughput(snri)
# print(th)
# np.random.uniform(0, 0.000125)
# plt.plot(th_d2d)
# plt.plot(th)
#
#
#
# t = np.linspace(min(n_users), max(n_users), 1000)
#
#
# plt.figure()
# plt.plot(n_users, snri_d2d)
# plt.plot(n_users, snri)
# plt.figure()
#
#
# plt.plot(t, snri_int(t), label="Sistema D2D")
# plt.plot(t, snri_int_d2d(t), label="Sistema D2D con Clusters")
# plt.xlabel("número de usuarios")
# plt.ylabel("Mbps")
# plt.title("Throughput")
# plt.legend()
# # plt.plot(n_users, th)
# # plt.plot(n_users, th_d2d)
# plt.grid(True)
# plt.show()

# NOISE = 3.14*10**-14
# GAMMAM = 3.7
# fc = 2300
# RADIO = np.sqrt(0.0921*500**2)
# pw = 10**2.24*(NOISE)*10**((GAMMAM*10*np.log10(RADIO/1000)+30*np.log10(fc)+49)/10)
# print(pw)
# PL = propagation_losses(d=5.0, units="m", alpha=3, fc=2400, model="D2D")
# Pw = subcarrier_power(d=5.0, dB=True)
# Y = channel_capacity_OFDMA(SINR=10, BWvec=[1 , 2])
# I = calculate_interference_cotier(Pj= [1,3,4], PLsc=1, No=-174)
# SNR = calculate_SNR(Psc=[1, 2], PLsc=[3, 4], No=-174)
# SINR = calculate_SINR(Psc=[1, 2], PLsc=[3, 4], I=10, No=-174)
# sat = calcule_satisfaction(Y=[1, 2, 3], D=[4, 5, 6])
#
# print(PL)
# print(Pw)
# print(Y)
# print(I)
# print(SNR)
# print(SINR)
# print(sat)
