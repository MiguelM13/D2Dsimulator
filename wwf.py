import numpy as np
from escenarios import build_city, generate_cars, generate_fc


def wwf_algorithm(users=None, femtocells=None, bw_cluster=10):
    """Algoritmo WWF
    Args:
        users: Conjunto de usuarios
        femtocells: Conjunto de femtoceldas
        bw_cluster: Ancho de banda del cluster
    Returns:
        users
    """
    # Obtener Demanda actual por cada usuario
    D = users.getDemandDict()
    # Obtener Demanda total
    total_demand = users.getTotalDemand()
    # Usuarios Locales
    users_locales = {ID: D[ID]/total_demand for ID in D}
    # Ordenar en forma ascendente el tráfico (menor a mayor)
    if len(users_locales) > 2:
        users_locales = dict(sorted(users_locales.items(), key=lambda x: x[1]))
    ids = list(users_locales.keys())
    i = 0
    bw = 0
    sum_bw = 0
    sum_w = 0
    print(ids)
    while i < len(users_locales) and sum_bw < bw_cluster:
        print(users[ids[i]].isSubscribed())
        print(users[ids[i]].femtoID)
        # Usuario Actual
        if users[ids[i]].isSubscribed():
            bw_actual = users[ids[i]].demand/femtocells[users[ids[i]].femtoID].bits_mod - users[ids[i]].bw_assigned/users_locales[ids[i]]
            for j in range(i, len(users)):
                sum_w += users_locales[ids[i]]
            bw_remain = (bw_cluster - sum_bw)/sum_w
            if bw_actual < bw_remain:
                bw = bw_actual
            else:
                bw = bw_remain
            j = i
            while j <= len(users_locales) and sum_bw < bw_cluster:
                if users[ids[j]].isSubscribed():
                    bw_prop = users_locales[ids[j]]*bw
                    users[ids[j]].bw_assigned = users[ids[j]].bw_assigned + bw_prop
                    sum_bw += bw_prop
                    if users[ids[j]].bw_assigned > users[ids[j]].demand/femtocells[users[ids[j]].femtoID].bits_mod:
                        break
                j += 1
                    # print(sum_bw)
            if users[ids[i]].bw_assigned > users[ids[i]].demand/femtocells[users[ids[i]].femtoBS].bits_mod:
                break
            i += 1




# ------------ Parámetros de simulación ----------------

n_experiments = 10  # número de experimentos
n_clusters = 5  # número de clusters
clusters = True  # clusters bandera
d2d = True  # D2D bandera
n_cars = 50  # número de autos
n_fc = 16  # número de femtoceldas

radio_car = 40  # radio de los autos
radio_fc = 80  # radio de las femtoceldas

# Generar mapa
width = 1024
height = 720
edifices, fcs_positions, cars_positions = build_city(width=width, height=height, edificesColor=(100, 100, 100, 128))
cars = generate_cars(init_positions=cars_positions, n_cars=n_cars, color=(20, 160, 140, 100),
                     map_size=[width, height], radius_car=radio_car, d2d=d2d)
fcs = generate_fc(init_positions=fcs_positions, n_fc=n_fc, radius_fc=radio_fc, color=(243, 34, 90, 150))

fcs.setFemtocellUsers(cars)
fcs.setNeighbors()
cars.setFemtocells(fcs)
cars.setNeighbors()
cars.setSubscribers(n_subscribers=16, fcs=fcs)

wwf_algorithm(users=cars, femtocells=fcs)
print(cars.getDemandDict())