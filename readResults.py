import numpy as np 
import xlsxwriter
import matplotlib.pyplot as plt
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Results.xlsx')
worksheet = workbook.add_worksheet()

data = np.load("results.npy", allow_pickle=True)[()]
data = data["FCS"]
print("Algo:", data.keys())
for Id in data:
	if Id != "time":
		links = data[Id]["Links"]
		#print(Id, data[Id].keys())
links = data["F5"]["Links"]
traffic = data["F5"]["traffic"]
t = data["time"]
print(len(t), len(links))
mlink = []
tv = []
for i in range(len(links)):
	if len(links[i]) > 0:
		mlink.append(len(links[i]))
		tv.append(t[i])
		# print(t[i], ":", len(links[i]))

plt.plot(tv, mlink)
plt.grid(True)
plt.title("Promedio de enlaces por Femotcelda")
plt.show()
row = 5
n_variables = 3
for Id in data:
	if Id != "time":
		# print("ID: ", Id)
		traffic = data[Id]["traffic"]
		prx = data[Id]["Prx"]
		worksheet.write(row, 0, Id)
		for col in range(len(traffic)):
			worksheet.write(row+1, 1, "Traffic (Mbps)")
			worksheet.write(row+2, 1, "Prx (dBm) ")
			worksheet.write(row+1, col+2, traffic[col])
			worksheet.write(row+2, col+2, prx[col])
		row+=n_variables
	else:
		time = data["time"]
		worksheet.write(0, 0, "Time (seg): ")
		for col in range(len(time)):
			worksheet.write(0, col+1, time[col])

workbook.close()
# plt.plot(traffic)
# plt.grid(True)
# plt.title("Tráfico")
# plt.show()