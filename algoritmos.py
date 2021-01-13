import numpy as np


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


def calculate_SINR(Pi_SCn, PLi_SCn, No, Ii, Tsc):
    """ Lol
    Args:
        SINRi: Relación señal-ruido más Interferencia para el usuario i
        Pi_SCn: Potencia asignada a la subportadora SCn del usuario i
        PLi_SCn: Pérdida por trayectoria de la subportadora SC del usuario i
        No: Potencia de Ruido
        Ii: Interferencia entre nivel (co - tier) en el usuario i
        Tsc: Tsc: Total de subportadoras
    """
    SINRi = 0
    for n in range(1, Tsc + 1):
        SINRi += Pi_SCn / (PLi_SCn * (No + Ii))
    return SINRi


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
            raise AssertionError('Psc and PLsc must have same dimension...')
    else:
        SNR = None
    return SNR


def calculate_interference_cotier(Pj=None, PLsc=1, No=-174):
    """Calcula la interferencia co-tier
    Args:
        Psc: (list) Potencia asignada a la subportadora SCn del usuario i
        PLsc: (list) Pérdida por trayectoria de la subportadora SC del usuario i
        No: Potencia de Ruido dBm/Hz
    Returns:
        I: Interferencia co-tier
    """
    I = 0
    if Pj and PLsc:
        # Número de subportadoras
        if len(Pj) > 0:
            Tsc = len(Pj)
            for n in range(Tsc):
                I += Pj[n] / (PLsc * No)
        else:
            raise AssertionError('Psc and PLsc must have same dimension...')
    else:
        I = None
    return I


# def calculate_SINR(Psc=None, PLsc=None, I=None, No=-174):
#     """Calcular el SNR de un cierto usuario i
#     Args:
#         SNRi: Relación señal-ruido para el usuario i
#         Psc: (list) Potencia asignada a la subportadora SCn del usuario i
#         PLsc: (list) Pérdida por trayectoria de la subportadora SC del usuario i
#         No: Potencia de Ruido dBm/Hz
#     Returns:
#         SNR: Relación señal a ruido
#     """
#     SINR = 0
#     if Psc and PLsc and I:
#         # Número de subportadoras
#         if len(Psc) == len(PLsc):
#             Tsc = len(Psc)
#             for n in range(Tsc):
#                 SINR += Psc[n] / (PLsc[n] * (No + I))
#         else:
#             raise AssertionError('Psc and PLsc must have same dimension...')
#     else:
#         SINR = None
#     return SINR


def propagation_losses(d=5.0, units="m", alf=3, fc=2400, model="D2D"):
    """Cálculo de pérdidas de propagación
    Args:
        d: distancia en kilómetros (Km)
        units: Unidades "m" o "km"
        fc :Frecuencia de portadora (MHz)
        alf: Factor de atenuación
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
    if model == "MC":
        PL = 10 * np.log10(d ** alf) + 30 * np.log10(fc) + 49
    # Femtocelda
    if model == "FC":
        PL = 10 * np.log10(d ** alf) + 37
    # D2D
    if model == "D2D":
        PL = 40 * np.log10(d) + 148

    return PL


def subcarrier_power(d=5.0, units="m", alf=3, RSRP=-75, dB=True):
    """Estima la potencia de la subportadora
    Args:
        d: distancia
        units: str, unidades "m" o "km"
        RSRP: Potencia recibida de señal de referencia -75dBm y -88dBm
        dB: si es True retorna Psc en dBm, sino retorna en mW
    Returns:
        Psc: Potencia de subportadora mW/dBm
    """
    PL = propagation_losses(d=d, units=units, alf=alf)
    Psc = RSRP + PL
    if not dB:
        Psc = 10 ** (Psc / 10)
    return Psc

# PL = propagation_losses(d=5.0, units="m", alf=3, fc=2400, model="D2D")
# Pw = subcarrier_power(d=5.0)
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
