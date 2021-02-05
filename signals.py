import numpy as np
from scipy.signal import medfilt
# from random import uniform
# import matplotlib.pyplot as plt
# import time
from calculos import *

def mean_signal(signals):
	"""It returns mean signals
	:param signals:
	"""
	if not isinstance(signals, np.ndarray):
		signals = np.array(signals)

	m, n = signals.shape
	result = [np.mean(signals[0:m, j]) for j in range(n)]
	result = np.array(result)
	return result


def get_signals(data=None, name=None,):
	signals = []
	if data is not None:
		for ids in data:
			if name in data[ids]:
				if name != "Links":
					signals.append(data[ids][name])
				else:
					# signals.append([len(i) for i in data[ids][name]])
					pass
	signals = np.array(signals)
	signals = dist(signals)
	return signals


def get_signal(data=None, name=None, smooth=True, alf=0.1, N=21, noise=True):
	if (data is not None) and (name is not None):
		signals = get_signals(data=data, name=name)
		signal = mean_signal(signals)
		if noise:
			# t = np.linspace(0,1, len(signal))
			# signal += np.random.normal(0, max(signal)/4, signal.shape)
			pass
		if smooth:
			signal = smooth_signal(x=signal, alf=alf, N=N)
		return signal


def filtro_pme(x=None, alf=0.1):
	L = len(x)
	y = np.zeros(L)
	for i in range(0, L):
		if i == 0:
			y[i] = x[i]
		else:
			y[i] = alf*x[i] + (1-alf)*y[i-1]
	return y


def filtro_mediana(x=None, N=10):
	return medfilt(x, N)


def smooth_signal(x=None, alf=0.4, N=21):
	x = filtro_mediana(x, N)
	x = filtro_pme(x=x, alf=alf)
	return x


