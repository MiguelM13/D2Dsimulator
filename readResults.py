import numpy as np 
import xlsxwriter
import matplotlib.pyplot as plt
# Create a workbook and add a worksheet.
# workbook = xlsxwriter.Workbook('Results.xlsx')
# worksheet = workbook.add_worksheet()

data = np.load("results.npy", allow_pickle=True)[()]
data = data["FCS"]
print(data.keys())
for Id in data:
	if Id != "time":
		links = data[Id]["Links"]
		#print(Id, data[Id].keys())
links = data["FC2"]["Links"]
traffic = data["FC2"]["traffic"]
t = data["time"]
print(len(t), len(links))
mlink = []
tv = []
for i in range(len(links)):
	if len(links[i]) > 0:
		mlink.append(len(links[i]))
		tv.append(t[i])
		print(t[i], ":", len(links[i]))

plt.plot(tv, mlink)
plt.figure()
plt.plot(traffic)
plt.show()
# row = 0
# n_variables = 3
# for Id in data:
# 	if Id != "time":
# 		print("ID: ", Id)
# 		traffic = data[Id]["traffic"]
# 		prx = data[Id]["Prx"]
# 		worksheet.write(row, 0, Id)
# 		for col in range(len(traffic[:100])):
# 			worksheet.write(row+1, 1, "Traffic")
# 			worksheet.write(row+2, 1, "Prx ")
# 			worksheet.write(row+1, col+2, traffic[col])
# 			worksheet.write(row+2, col+2, prx[col])
# 		row+=n_variables
# workbook.close()
#
# plt.plot(traffic)
# plt.grid(True)
# plt.title("Traffic")
# plt.show()