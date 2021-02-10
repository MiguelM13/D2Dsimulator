from escenarios import build_city, generate_cars, generate_fc
from simulator import Simulator
import time
import pygame
from cluster import Cluster

# ------------ Parámetros de simulación ----------------

n_experiments = 10  # número de experimentos
n_clusters = 5  # número de clusters
enable = True  # clusters bandera
d2d = True  # D2D bandera
n_cars = 50  # número de autos
n_fc = 15  # número de femtoceldas

n_cars = 50
n_fcs = 15
radio_car = 30  # radio de los autos
radio_fc = 50  # radio de las femtoceldas

T = 30 # seg
fps = 30 # 
delay = 1/fps
max_iters = T*fps
save = True


# Generar mapa
width = 1024
height = 620
edifices, fcs_positions, cars_positions = build_city(width=width, height=height, edificesColor=(100, 100, 100, 158))
cars = generate_cars(init_positions=cars_positions, n_cars=n_cars, color=(20, 160, 140, 100),
                     map_size=[width, height], radius_car=radio_car, d2d=d2d)
fcs = generate_fc(init_positions=fcs_positions, n_fc=n_fc, radius_fc=radio_fc, color=(243, 34, 90, 150))

# Simular
t0 = time.time()


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

#Para dibujar
size = (width, height)
surface = pygame.Surface(size, pygame.SRCALPHA, 32)
background_color=(255, 255, 255)
surface = pygame.Surface(size, pygame.SRCALPHA, 32)
screen = pygame.display.set_mode((width, height))
pygame.display.update()
screen.fill(background_color)
i = 0
run = True
while i <= max_iters:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	screen.fill(background_color)
	surface.fill(background_color)
	# Dibujar
	fcs.draw(surface=surface)
	cars.draw(surface=surface)
	edifices.draw(surface)
	# Mover autos
	cars.move(edifices=edifices)
	#
	cars.updateLinks(surface=surface)
	fcs.updateLinks(surface=surface)
	#Si habilita los clusters
	if enable:
		cluster.group(n_clusters=5)
		cluster.draw(surface)

	screen.blit(surface, (0, 0))
	pygame.display.flip()
	time.sleep(delay)

	if not run:
		break

	i +=1
pygame.quit()
t1 = time.time()
dt = t1 - t0

print("Eleapsed: ", t1 - t0)
