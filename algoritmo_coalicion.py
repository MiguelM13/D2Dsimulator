from escenarios import build_city, generate_cars, generate_fc
from cluster import Cluster
from itertools import combinations
import numpy as np
import time
import math
from math import factorial

"""Algoritmo de coalición 
1. Debo tener la lista de todos los usuarios
2. Leo la demanda (Ancho de banda de cada usuario
    Crear clusters
3. Defino la  función de coalición
4. Defino la función de Valor (Shapley)
5. Asigno recursos a Priori
6. 
"""


def binom(n, k):
    return math.factorial(n) // math.factorial(k) // math.factorial(n - k)


def nchoosek(arr, n):
    """It returns a list with combinations
    :param arr: array/list of elements
    :param n: number of combinations
    """
    return np.array(list(combinations(arr, n)))


def subcarriers_average(fcs=None, yf=1, bs=0.015):
    """It returns the average number of subcarriers required per femtocells
    :param fcs: list of femtocells
    :param yf: spectral efficency
    :param bs: bandwidth per subcarrier
    """
    FC = len(fcs)
    nfs = 0
    for fc in fcs:
        nfs += fc.rf_su/fc.yf
    nfs = nfs/(FC*bs)
    return nfs


def v(s=None, rm_pu=0.5, ym=1, rf_pu=0.5, yf=1, nfs=128, ns=256):
    """Coalition function
    :param s: coalition group or cluster (set of players)
    :param rm_pu: sum of data rate of public users served by MC m
    :param ym: spectral efficiency for MC
    :param rf_pu: sum of data rate of subscribers served by FC f
    :param yf: spectral efficiency for FC
    :param nfs: average number of subcarriers required per femtocells
    :param ns: number of subcarriers
    """
    num = 0
    den = 0
    S = len(s)
    if S >= 1:
        for k in range(S):
            num += rf_pu/yf
            den += rf_pu/yf
        den += rm_pu/ym
        result = (num/den)*(ns - nfs)
        return result
    else:
        return 0


def shapley_value(s=None, N=1, S=1):
    """It calcules de shapley value
    :param s: coalition
    :param N: number of players
    :param S: number of player in the coalition
    """
    value = 0
    f = factorial
    for user in s:
        value += (f(S-1)*f(N - S))/f(N)
        value *= v(s) - v(s - user)
    return value

def apply_shapley(s_dict=None):
    shapley_vector = []
    for s in s_dict.values():
        shap_val = shapley_value(s=s, N=n_cars, S=len(s))
        shapley_vector.append(shap_val)
    return shapley_vector

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
# Las femtocelda
fcs.setFemtocellUsers(cars)
# Las femtoceldas buscan vecinos
fcs.setNeighbors()
cars.setFemtocells(fcs)
# los usuarios registran posibles vecinos
cars.setNeighbors()
# Se subscriben los usuarios
cars.setSubscribers(n_subscribers=16, fcs=fcs)
# Se forman los grupos de coalición
cluster = Cluster(femtocells=fcs, users=cars, enable=clusters)
cluster.group(n_clusters=5)
s_dict = cluster.getCoalitions()
# Calculos los valores de shapley para cada coalición
shap_vector = apply_shapley(s_dict)
skey = list(s_dict.keys())
for i in range(len(shap_vector)):
    print(skey[i], " : ", shap_vector[i], "Mbps")

    
# print(shap_vector)
# print(sum(shap_vector))
# Simular
# simulator = Simulator(width=width, height=height, edifices=edifices, cars=cars, fcs=fcs, clusters=clusters)
# simulator.run()
