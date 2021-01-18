from Escenarios import build_city, generate_cars, generate_fc
from sklearn.cluster import KMeans
import numpy as np
import time


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


width = 1024
height = 720
walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(237, 237, 230))
cars = generate_cars(centers_street, 30, color=(100, 100, 10), mapSize=[width, height], radius=30)
fcs = generate_fc(centers_corner, 16, 200, color=(230, 50, 30, 120))

cluster(femtocells=fcs, users=cars)