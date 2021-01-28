from Objects import Wall, Car, Group, Femtocell
from simulator import Simulator
import random
from threading import Thread
import pygame
import numpy as np
import time


def build_city(width=1280, height=720, wallsColor=(10,200,50)):
    """
    Args:

    """
    # Para construir la Ciudad
    D = 8 # Separación entre calles (px)
    w = 68  # Ancho de los edificiós (px)
    h = 45  # Largo (altura rectangular) de los edificios (px)

    W = width  # Ancho del mapa (px)
    H = height # Largo del mapa (px)

    # Calcular número de edificios
    m = int(W / w)  # ¿Cuántos edificios caben a lo ancho del mapa?
    n = int(H / h)  # ¿Cuántos edificios caben a lo largo del mapa?
    walls = Group(prefix="Wall")  # Grupo de paredes

    centers_corner = [] # Esquina
    centers_street = [] # Centro calle
    offset = 5
    rows = []
    # Contruir ciudad
    for i in range(m):
        for j in range(n):
            x = int(i * w + offset)
            y = int(j * h)
            walls.add(Wall(x, y, w - D, h - D, color=wallsColor))
            rows.append([x + w, y + h])
            centers_street.append([x + w - int(D / 2), y + h - int(D / 2)])
        centers_corner.append(rows)
        rows = []
    # centers_corner = np.array(centers_corner, dtype='uint8')
    centers_corner = np.array(centers_corner)
    return walls, centers_corner, centers_street


def generate_cars(init_positions, Ncars, color=(2, 2, 2), radius=16, mapSize=[1024, 720], d2d=True):
    """Esta"""
    cars = Group(prefix="C")  # Grupo de carros
    rand_centers = random.sample(init_positions, Ncars)
    i = 1
    for item in rand_centers:
        cars.add(Car(*item, Id="C"+str(i), color=color, radius=radius, mapSize=mapSize, d2d=d2d, indx=i))
        i += 1
    return cars


def generate_fc(positions, NFC, radioFC, color=(80, 120, 50, 128)):
    fcs = Group(prefix="F")  # Grupo de femtoceldas
    m, n, _ = positions.shape
    space_between_fc = 4
    indx = 0
    for i in range(m):
        for j in range(n):
            if i % space_between_fc == 0 and j % space_between_fc == 0:
                if indx < NFC:
                    position = positions[i][j]
                    fcs.add(Femtocell(*position, radius=radioFC, color=color, Id="FC" + str(indx + 1), indx=indx))
                    indx += 1
    return fcs


def escenario_1(Nusers=30, NFC=16, radioFC=100, radioCar=10, playBtn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    pygame.display.set_caption("ESCENARIO TODO EN COBERTURA")
    walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(100, 100, 100, 128))
    cars = generate_cars(centers_street, Nusers, color=(40, 50, 180, 100), mapSize=[width, height], radius=radioCar, d2d=d2d)
    fcs = generate_fc(centers_corner, NFC, radioFC, color=(230, 50, 30, 120))
    simulador1 = Simulator(width=width, height=height, walls=walls, cars=cars, fcs=fcs, clusters=clusters)
    th1 = Thread(target=simulador1.run, args=(playBtn,))
    th1.start()


def escenario_2(Nusers=30, NFC=16, radioFC=100, radioCar=10, playBtn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    pygame.display.set_caption("ESCENARIO COBERTURA PARCIAL")
    walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(237, 237, 230))
    cars = generate_cars(centers_street, Nusers, color=(100, 100, 10), mapSize=[width, height], radius=radioCar, d2d=d2d)
    fcs = generate_fc(centers_corner, NFC, radioFC, color=(100, 50, 30, 180))
    simulador2 = Simulator(width=width, height=height, walls=walls, cars=cars, fcs=fcs, clusters=clusters)
    th2 = Thread(target=simulador2.run, args=(playBtn,))
    th2.start()


def escenario_3(Nusers=30, NFC=16, radioFC=100, radioCar=10, playBtn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    NFC=4
    pygame.display.set_caption("ESCENARIO FUERA DE COBERTURA")
    walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(120, 80, 40))
    cars = generate_cars(centers_street, Nusers, color=(100, 100, 10), mapSize=[width, height], radius=radioCar, d2d=d2d)
    fcs = generate_fc(centers_corner, NFC, radioFC, color=(50, 100, 180, 180))
    simulador3 = Simulator(width=width, height=height, walls=walls, cars=cars, fcs=fcs, clusters=clusters)
    th3 = Thread(target=simulador3.run, args=(playBtn,))
    th3.start()


def escenario_4(Nusers=30, NFC=16, radioFC=100, radioCar=10, playBtn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    pygame.display.set_caption("ESCENARIO SIN D2D")
    NFC=1
    radioFC =2000*0.3
    walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(181, 187, 196))
    cars = generate_cars(centers_street, Nusers, color=(100, 100, 10), mapSize=[width, height], d2d=d2d)
    fcs = generate_fc(centers_corner, NFC, radioFC, color=(189, 153, 177, 180))
    simulador4 = Simulator(width=width, height=height, walls=walls, cars=cars, fcs=fcs, clusters=clusters)
    th4 = Thread(target=simulador4.run, args=(playBtn,))
    th4.start()


def escenario_5(Nusers=30, NFC=16, radioFC=100, radioCar=10, playBtn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    pygame.display.set_caption("ESCENARIO D2D CON CLUSTERS INCLUIDOS")
    walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(181, 187, 196))
    cars = generate_cars(centers_street, Nusers, color=(100, 100, 10), mapSize=[width, height], d2d=False)
    fcs = generate_fc(centers_corner, NFC, radioFC, color=(189, 163, 177, 180))
    simulador5 = Simulator(width=width, height=height, walls=walls, cars=cars, fcs=fcs, clusters=clusters)
    th5 = Thread(target=simulador5.run, args=(playBtn,))
    th5.start()


def escenario_6(Nusers=30, NFC=16, radioFC=100, radioCar=10, playBtn=None, d2d=False, clusters=False):
    width = 1024
    height = 720
    pygame.display.set_caption("ESCENARIO D2D SIN CLUSTERS")
    walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(181, 187, 196))
    cars = generate_cars(centers_street, Nusers, color=(100, 100, 10), mapSize=[width, height], d2d=d2d)
    fcs = generate_fc(centers_corner, NFC, radioFC, color=(189, 143, 177, 180))
    simulador6 = Simulator(width=width, height=height, walls=walls, cars=cars, fcs=fcs, clusters=clusters)
    th6 = Thread(target=simulador6.run, args=(playBtn,))
    th6.start()