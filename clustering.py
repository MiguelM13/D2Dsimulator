from Escenarios import build_city, generate_cars, generate_fc
from sklearn.cluster import KMeans
import numpy as np
import time
import matplotlib.pyplot as plt


def generate_circle(R, N, dcx, dcy):
    """Generar circulo
    R: Radio del círculo
    N: número de muestras
    dcx: Offset en el eje x (Origen eje x)
    dcy: Offset en el eje y (Origen eje y)
    """
    # Ecuación parámetrica de la circunferencia
    theta = np.linspace(0, 2 * np.pi, N)
    x = R * np.cos(theta) + dcx
    y = R * np.sin(theta) + dcy
    return x, y


def cluster(femtocells=None, users=None):
    t0 = time.time()
    fc_pos = femtocells.getPositionsDict()
    points = np.array(list(fc_pos.values()))
    kmeans = KMeans(n_clusters=5).fit(points)
    centroids = kmeans.cluster_centers_.T
    print(centroids)
    t1 = time.time()
    dt = t1 - t0
    print(dt)
    return points, centroids


# width = 1024
# height = 720
# walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(237, 237, 230))
# cars = generate_cars(centers_street, 30, color=(100, 100, 10), mapSize=[width, height], radius=30)
# fcs = genera+te_fc(centers_corner, 16, 200, color=(230, 50, 30, 120))
#
# p, centroids = cluster(femtocells=fcs, users=cars)
# pc = np.array(list(cars.getPositionsDict().values()))
#
# xc = []
# yc = []
#
# for x, y in pc:
#     xc.append(x)
#     yc.append(y)
#
#
# xs = []
# ys = []
# for x, y in p:
#     xs.append(x)
#     ys.append(y)
#
# R = 150
# samples = 100
# print(centroids.shape)
# n = len(centroids[0])
# for i in range(n):
#     dcx = centroids[0][i]# centroide coordenada eje x
#     dcy = centroids[1][i]# centroide coordenada eje y
#     print("DC: ", dcx, dcy)
#     x, y = generate_circle(R, samples, dcx, dcy)# Generar circunferencia con origen en el centroide
#     plt.plot(x,y,'--', label="Cluster "+str(i+1))# Gráficar circulo
#     plt.fill(x,y,alpha=0.2)# Pintar el área del circulo
#     plt.text(dcx,dcy+5,"Cluster "+str(i+1),fontsize=13)#Etiquetar femtocelda
#
# plt.plot(xs, ys, 'o')
# plt.plot(xc, yc, 'x')
# plt.plot(centroids[0], centroids[1], 'x')
# plt.grid(True)
# plt.legend()
# plt.show()
#
