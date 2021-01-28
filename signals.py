import numpy as np
# from random import uniform
# import matplotlib.pyplot as plt
# import time


def mean_signal(signals):
	if not isinstance(signals, np.ndarray):
		signals = np.array(signals)
	m, n = signals.shape
	result = [np.mean(signals[0:m, j]) for j in range(n)]
	return result


# N = 200
# # s1 = [uniform(0, 100) for i in range(N)]
# # s2 = [uniform(0, 100) for i in range(N)]
# t = np.linspace(0, 1, N)
# w = 2*np.pi*2
# NS = 10
# s = []
# for i in range(NS):
# 	x = np.sin(w*t + uniform(-np.pi, np.pi))
# 	s.append(x)
#
# t0 = time.time()
# sm = mean_signal(s)
# t1 = time.time()
# sm2 = np.array(s[0])
# for i in range(1,len(s)):
# 	sm2+=np.array(s[i])
# sm2= sm2/NS
#
# t2 = time.time()
# dt1 = t1 - t0
# dt2 = t2 - t1
# print("dt1: ", dt2)
# print("dt2: ", dt1)
# print(f"1 is {dt1/dt2} faster than 2 ")
#
#
# for i in range(len(s)):
# 	plt.plot(s[i], label="signal " + str(i))
#
# plt.plot(sm, label="signal mean", linewidth=2)
# plt.plot(sm2, label="signal mean 2", linewidth=2)
# plt.grid(True)
# plt.legend()
# plt.show()

