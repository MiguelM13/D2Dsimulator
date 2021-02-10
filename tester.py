from escenarios import generate_fc, generate_cars, build_city
import time
import numpy as np
from cluster import Cluster


def run_simulation(femtocells=None, users=None, edifices=None, max_iters=500, delay=0.0):
    """
    :param femtocells: cf
    :param users:
    :param edifices:
    :param max_iters:
    :param delay:
    """
    i = 0
    while i <= max_iters:
        users.move(edifices=edifices)
        femtocells.updateLinks()
        users.updateLinks()
        time.sleep(delay)
        i += 1
    data_users = users.getData()
    data_fcs = femtocells.getData()
    return data_users, data_fcs


def get_experiment_name(d2d=False, cluster=False):
    if d2d and cluster:
        return "d2d_cluster"
    if d2d and not cluster:
        return "d2d"
    if not d2d and cluster:
        return "cluster"
    if not d2d and not cluster:
        return "not_cluster_d2d"


# ------------ Parámetros de simulación ----------------
n_experiments = 10  # número de experimentos
n_clusters = 5  # número de clusters
enable = False  # clusters bandera
d2d = True  # D2D bandera
cars_number = [10 * (i + 1) for i in range(n_experiments)]  # número de autos
fcs_number = [5 * (i + 1) for i in range(n_experiments)]  # número de femtoceldas

n_cars = 20
n_fcs = 15
radio_car = 30  # radio de los autos
radio_fc = 200  # radio de las femtoceldas

delay = .0001
max_iters = 600
save = True

# Generar mapa
width = 1024
height = 620
tv = []
for n_cars in cars_number:
    t0 = time.time()
    edifices, centers_corner, centers_street = build_city(width=width, height=height, edificesColor=(237, 237, 230))

    cars = generate_cars(init_positions=centers_street, n_cars=n_cars, color=(100, 100, 10), map_size=[width, height],
                         radius_car=radio_car, d2d=d2d)
    fcs = generate_fc(init_positions=centers_corner, n_fc=n_fcs, color=(230, 50, 30, 120), radius_fc=200)
    # Las femtocelda
    fcs.setFemtocellUsers(cars)
    # Las femtoceldas buscan vecinos
    fcs.setNeighbors()
    cars.setFemtocells(fcs)
    # los usuarios registran posibles vecinos
    cars.setNeighbors()
    # Se subscriben los usuarios
    cars.setSubscribers(n_subscribers=15, fcs=fcs)
    # Se forman los grupos de coalición
    cluster = Cluster(femtocells=fcs, users=cars, enable=enable)

    #
    data_cars, data_fcs = run_simulation(femtocells=fcs, users=cars, edifices=edifices, max_iters=max_iters, delay=delay)
    t1 = time.time()
    dt = t1 - t0
    tv.append(dt)
    print("Elapsed: ", t1 - t0)
    data = {"cars": data_cars, "fcs": data_fcs}

    if save:
        folder = "results/"
        name = get_experiment_name(d2d=d2d, cluster=enable)
        full_name = folder + name + "_" + str(n_cars) + ".npy"
        np.save(full_name, data)

print("Tiempo Total: ", np.sum(tv))
