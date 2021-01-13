import numpy as np 
import xlsxwriter
import matplotlib.pyplot as plt
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Results.xlsx')
worksheet = workbook.add_worksheet()

data = np.load("results.npy", allow_pickle=True)[()]


row = 0
n_variables
for Id in data:
	if Id != "time":
		print("ID: ", Id)
		traffic = data[Id]["traffic"]
		prx = data[Id]["Prx"]
		worksheet.write(row,0, Id)
		for col in range(len(traffic[:100])):
			worksheet.write(row+1, 1, "Traffic")
			worksheet.write(row+2, 1, "Prx ")
			worksheet.write(row+1, col+2, traffic[col])
			worksheet.write(row+2, col+2, prx[col])
		row+=n_variables
workbook.close()

plt.plot(traffic)
plt.grid(True)
plt.title("Traffic")
plt.show()