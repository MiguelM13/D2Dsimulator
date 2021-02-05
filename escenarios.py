from objects import Edifice
from car import Car
from groups import Group
from femtocell import Femtocell
from simulator import Simulator
import random
from threading import Thread
import pygame
import numpy as np


def build_city(width=1280, height=720, edificesColor=(10, 200, 50)):
    """Contruye una ciudad con edificios
    Args:

    """
    # Para construir la Ciudad
    D = 8  # Separación entre calles (px)
    w = 51  # Ancho de los edificiós (px)
    h = 51  # Largo (altura rectangular) de los edificios (px)

    W = 1024  # Ancho del mapa (px)
    H = 720  # Largo del mapa (px)

    # Calcular número de edificios
    m = int(W / w)  # ¿Cuántos edificios caben a lo ancho del mapa?
    n = int(H / h)  # ¿Cuántos edificios caben a lo largo del mapa?
    edifices = Group(prefix="Edifice")  # Grupo de paredes

    centers_corner = []  # Esquina
    centers_street = []  # Centro calle
    offset_x = 5
    offset_y = 5
    rows = []
    # Contruir ciudad
    for i in range(m):
        for j in range(n):
            x = int(i * w + offset_x)
            y = int(j * h + offset_y)
            edifices.add(Edifice(x, y, w - D, h - D, color=edificesColor))
            rows.append([x + w, y + h])
            centers_street.append([x + w - int(D / 2), y + h - int(D / 2)])
        centers_corner.append(rows)
        rows = []
    # centers_corner = np.array(centers_corner, dtype='uint8')
    centers_corner = np.array(centers_corner)
    return edifices, centers_corner, centers_street


def generate_cars(init_positions=None, n_cars=None, color=(20, 160, 140, 100), radius_car=16, map_size=None, d2d=True):
    """Genera los autos
    :param init_positions: vector de posiciones iniciales
    :param n_cars: número de autos
    :param color: color de los autos
    :param radius_car: radio de los autos
    :param map_size: tamaño del mapa
    :param d2d: D2D flag
    :return:
    """
    if map_size is None:
        map_size = [1024, 720]
    cars = Group(prefix="C")  # Grupo de carros
    rand_centers = random.sample(init_positions, n_cars)
    i = 1
    for position in rand_centers:
        cars.add(Car(x=position[0], y=position[1], Id="C" + str(i), color=color, radius=radius_car, map_size=map_size,
                     d2d=d2d, indx=i))
        i += 1
    return cars


def generate_fc(init_positions=None, n_fc=None, radius_fc=None, color=(80, 120, 50, 128)):
    """Generar Femto celdas
    :param init_positions: posiciones iniciales
    :param n_fc: número de femtoceldas
    :param radius_fc: radio de femtocelda
    :param color: tuple color for femtocells
    :return:
    """
    if not isinstance(init_positions, np.ndarray):
        init_positions = np.array(init_positions)

    fcs = Group(prefix="F")  # Grupo de femtoceldas
    m, n, _ = init_positions.shape
    space_between_fc = 4
    indx = 0
    pos_y = [i for i in range(m) if i % 4 == 0]
    pos_x = [i + 1 for i in range(n) if i % 4 == 0]
    for i in pos_x:
        for j in pos_y:
            if indx < n_fc:
                position = init_positions[j +1, i]
                fcs.add(Femtocell(*position, radius=radius_fc, color=color, Id="FC" + str(indx + 1), indx=indx))
                indx += 1
    return fcs


def escenario_1(n_users=30, n_fc=16, radius_fc=100, radius_car=10, play_btn=None, d2d=False, clusters=False):
    """ Generar escenario 1
    :param n_users: número de usuarios
    :param n_fc: número de femtoceldas
    :param radius_fc: radio femtocelda
    :param radius_car: radio carro
    :param play_btn: boton play/pause
    :param d2d: d2d Flag
    :param clusters: clusters flag
    :return: 
    """
    width = 1024
    height = 720
    pygame.display.set_caption("ESCENARIO TODO EN COBERTURA")
    edifices, centers_corner, centers_street = build_city(width=width, height=height,
                                                          edificesColor=(100, 100, 100, 128))
    cars = generate_cars(centers_street, n_users, color=(40, 50, 180, 150), map_size=[width, height], radius_car=radius_car,
                         d2d=d2d)
    fcs = generate_fc(centers_corner, n_fc, radius_fc, color=(243, 34, 90, 150))
    simulador1 = Simulator(width=width, height=height, edifices=edifices, cars=cars, fcs=fcs, clusters=clusters)
    th1 = Thread(target=simulador1.run, args=(play_btn,))
    th1.start()


def escenario_2(n_users=30, n_fc=16, radius_fc=100, radius_car=10, play_btn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    pygame.display.set_caption("ESCENARIO COBERTURA PARCIAL")
    edifices, centers_corner, centers_street = build_city(width=width, height=height, edificesColor=(237, 237, 230))
    cars = generate_cars(centers_street, n_users, color=(100, 100, 10), map_size=[width, height], radius_car=radius_car,
                         d2d=d2d)
    fcs = generate_fc(centers_corner, n_fc, radius_fc, color=(100, 50, 30, 180))
    simulador2 = Simulator(width=width, height=height, edifices=edifices, cars=cars, fcs=fcs, clusters=clusters)
    th2 = Thread(target=simulador2.run, args=(play_btn,))
    th2.start()


def escenario_3(n_users=30, n_fc=16, radius_fc=100, radius_car=10, play_btn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    n_fc = 4
    pygame.display.set_caption("ESCENARIO FUERA DE COBERTURA")
    edifices, centers_corner, centers_street = build_city(width=width, height=height, edificesColor=(120, 80, 40))
    cars = generate_cars(centers_street, n_users, color=(100, 100, 10), map_size=[width, height], radius_car=radius_car,
                         d2d=d2d)
    fcs = generate_fc(centers_corner, n_fc, radius_fc, color=(50, 100, 180, 180))
    simulador3 = Simulator(width=width, height=height, edifices=edifices, cars=cars, fcs=fcs, clusters=clusters)
    th3 = Thread(target=simulador3.run, args=(play_btn,))
    th3.start()


def escenario_4(n_users=30, n_fc=16, radius_fc=100, radius_car=10, play_btn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    pygame.display.set_caption("ESCENARIO SIN D2D")
    n_fc = 1
    radius_fc = 2000 * 0.3
    edifices, centers_corner, centers_street = build_city(width=width, height=height, edificesColor=(181, 187, 196))
    cars = generate_cars(centers_street, n_users, color=(100, 100, 10), map_size=[width, height], d2d=d2d)
    fcs = generate_fc(centers_corner, n_fc, radius_fc, color=(189, 153, 177, 180))
    simulador4 = Simulator(width=width, height=height, edifices=edifices, cars=cars, fcs=fcs, clusters=clusters)
    th4 = Thread(target=simulador4.run, args=(play_btn,))
    th4.start()
