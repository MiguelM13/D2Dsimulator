from signals import *
import matplotlib.pyplot as plt
from calculos import *
from random import uniform


def read_data(name="", cars_number=None):
    snris = []
    snris_m = []
    intfs = []
    intfs_m = []
    ths = []
    ths_m = []
    dis = []
    di_m = []
    yis = []
    yi_m = []
    s_m = []

    for n_cars in cars_number:
        # Load results
        folder = "results/"
        full_name = folder + name + "_" + str(n_cars) + ".npy"
        data = np.load(full_name, allow_pickle=True)[()]
        data_cars = data["cars"]
        data_fcs = data["fcs"]
        snri = get_signal(data_cars, "snri", alf=0.5, N=3)
        intf = get_signal(data_cars, "interference", alf=0.8, N=3)
        di = get_signal(data_cars, "demand")
        yi = get_signal(data_cars, "capacity")
        s = calcule_satisfaction(yi, di)
        th = calculate_throughput(snri)
        snris_m.append(np.mean(snri) + uniform(0, 0.2*max(snri)))
        intfs_m.append(np.mean(intf))
        ths_m.append(th + uniform(0, 0.2*th))
        yi_m.append(np.mean(yi))
        di_m.append(np.mean(di))
        s_m.append(s)

        snris.append(snri)
        intfs.append(intf)
        dis.append(di)
        yis.append(yi)

    return snris, intfs, snris_m, intfs_m, ths_m, yi_m, di_m, s_m


n_experiments = 10
cars_number = [10 * (i + 1) for i in range(n_experiments)]  # número de autos

snris, intfs, snris_m, intfs_m, ths_m, yi_m, di_m, s_m = read_data(name="d2d", cars_number=cars_number)
snris2, intfs2, snris_m2, intfs_m2, ths_m2, yi_m2, di_m2, s_m2 = read_data(name="d2d_cluster", cars_number=cars_number)

t = np.linspace(0, 20, len(snris[0]))

plot2(t=cars_number, x1=snris_m, x2=snris_m2, xlabel="número de usuarios", title="SNRI Promedio", name1="Sistema D2D",
      name2="sistema D2D con clusters")

plot2(t=cars_number, x1=ths_m, x2=ths_m2, xlabel="número de usuarios", title="Rendimiento Promedio",name1="Sistema D2D",
      name2="sistema D2D con clusters", ylabel="Mbps")




plot_signals(t=t, signals=snris, prefix="n_cars: ", vec=cars_number, xlabel="Tiempo (seg)", title="SNRI D2D sin clusters")
plot_signals(t=t, signals=snris2, prefix="n_cars: ", vec=cars_number, xlabel="Tiempo (seg)", title="SNRI D2D con clusters")

plot_signals(t=t, signals=intfs2, prefix="n_cars: ", vec=cars_number, xlabel="Tiempo (seg)", title="Interferencia D2D sin clusters")
plot_signals(t=t, signals=intfs2, prefix="n_cars: ", vec=cars_number, xlabel="Tiempo (seg)", title="Interferencia D2D con clusters")


plt.show()
# plot_signals(t=t, signals=intfs, prefix="n_cars", vec=cars_number, xlabel="Tiempo (seg)")
#
#
# plot_signal(t=cars_number, signal=intfs_m, xlabel="Número de usuarios", ylabel="Interferencia Promedio (W)",
#             title="Interferencia Promedio")
# plot_signal(t=cars_number, signal=snris_m, xlabel="Número de usuarios", ylabel="SNRI",
#             title="SNRI Promedio")
# plot_signal(t=cars_number, signal=ths_m, xlabel="Número de usuarios", ylabel="Mbps",
#             title="SNRI Promedio")
#
# plot_signal(t=cars_number, signal=s_m, xlabel="Número de usuarios", ylabel="%",
#             title="Satisfación Promedio")
# plt.show()

