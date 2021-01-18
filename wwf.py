import numpy as np
from Escenarios import build_city, generate_cars, generate_fc


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
    while i < len(users_locales) and sum_bw < bw_cluster:
        # Usuario Actual
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
            bw_prop = users_locales[ids[j]]*bw
            users[ids[j]].bw_assigned = users[ids[j]].bw_assigned + bw_prop
            sum_bw += bw_prop
            if users[ids[j]].bw_assigned > users[ids[j]].demand/femtocells[users[ids[j]].femtoID].bits_mod:
                break
            j += 1
        if users[ids[i]].bw_assigned > users[ids[i]].demand/femtocells[users[ids[i]].femtoBS].bits_mod:
            break
        i += 1




width = 1024
height = 720
walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(237, 237, 230))
cars = generate_cars(centers_street, 30, color=(100, 100, 10), mapSize=[width, height], radius=30)
fcs = generate_fc(centers_corner, 16, 200, color=(230, 50, 30, 120))
wwf_algorithm(users=cars, femtocells=fcs)
