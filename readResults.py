import numpy as np 
import xlsxwriter
import matplotlib.pyplot as plt
from signals import mean_signal


def get_signals(data=None, name=None):
	signals = []
	if data is not None:
		for ids in data:

			if name in data[ids]:
				if name == "Links":
					links = [len(i) for i in data[ids][name]]
					signals.append(links)
				else:
					signals.append(data[ids][name])
	return signals


def get_signal(data=None, name=None):
	if (data is not None) and (name is not None):
		return np.array(mean_signal(get_signals(data=data, name=name)))


def calculate_throughput(SNRI):
	T = []
	for i in range(len(SNRI)):
		throughput = np.log2(SNRI[i])
		T.append(throughput)
	return T


# Create a workbook and add a worksheet.
# workbook = xlsxwriter.Workbook('Results.xlsx')
# worksheet = workbook.add_worksheet()

data = np.load("results.npy", allow_pickle=True)[()]
# traffic = get_signals(data["FCS"], name="traffic")
# traffic_mean = mean_signal(traffic)
traffic = get_signal(data=data["FCS"], name="traffic")
Prx = get_signal(data=data["FCS"], name="Prx")
Bw = get_signal(data=data["FCS"], name="Bw")
links = get_signal(data=data["FCS"], name="Links") + 30
SNRI = 1000*get_signal(data=data["CARS"], name="SNRI") + 500
Tro = calculate_throughput(SNRI)

time = data["CARS"]["time"]

time2 = np.linspace(0, 20, len(Tro))
time3 = 0.5*time2
plt.plot(traffic)
plt.title("Tráfico medio")
plt.ylabel("Mbps")
plt.grid(True)

plt.figure()
plt.plot(Prx)
plt.title("Prx")
plt.grid(True)

# plt.figure()
# plt.plot(Bw)
# plt.title("Bw")
# plt.ylabel("Mbps")
# plt.grid(True)

plt.figure()
plt.plot(links)
plt.title("Links")
plt.grid(True)


plt.figure()
plt.plot(SNRI)
plt.title("SNRi")
plt.grid(True)

plt.figure()
plt.plot(Tro)
plt.title("Throughput")
plt.grid(True)


plt.figure()
plt.plot(time)
plt.plot(time2)
plt.title("Time")
plt.grid(True)


plt.show()

# for Id in data:
# 	if Id != "time":
# 		links = data[Id]["Links"]
# 		#print(Id, data[Id].keys())
# links = data["F5"]["Links"]
# traffic = data["F5"]["traffic"]
# t = data["time"]
# print(len(t), len(links))
# mlink = []
# tv = []
# for i in range(len(links)):
# 	if len(links[i]) > 0:
# 		mlink.append(len(links[i]))
# 		tv.append(t[i])
# 		# print(t[i], ":", len(links[i]))
#
# plt.plot(tv, mlink)
# plt.grid(True)
# plt.title("Promedio de enlaces por Femotcelda")
# plt.show()
# row = 5
# n_names = 3
# for Id in data:
# 	if Id != "time":
# 		# print("ID: ", Id)
# 		traffic = data[Id]["traffic"]
# 		prx = data[Id]["Prx"]
# 		worksheet.write(row, 0, Id)
# 		for col in range(len(traffic)):
# 			worksheet.write(row+1, 1, "Traffic (Mbps)")
# 			worksheet.write(row+2, 1, "Prx (dBm) ")
# 			worksheet.write(row+1, col+2, traffic[col])
# 			worksheet.write(row+2, col+2, prx[col])
# 		row += n_names
# 	else:
# 		time = data["time"]
# 		worksheet.write(0, 0, "Time (seg): ")
# 		for col in range(len(time)):
# 			worksheet.write(0, col+1, time[col])
#
# workbook.close()
# # plt.plot(traffic)
# # plt.grid(True)
# # plt.title("Tráfico")
# # plt.show()