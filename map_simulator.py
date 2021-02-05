from escenarios import build_city, generate_cars, generate_fc
from simulator import Simulator

# ------------ Parámetros de simulación ----------------

n_experiments = 10  # número de experimentos
n_clusters = 5  # número de clusters
clusters = True  # clusters bandera
d2d = True  # D2D bandera
n_cars = 50  # número de autos
n_fc = 15  # número de femtoceldas

factor = 1
radio_car = 30*factor  # radio de los autos
radio_fc = 100*factor  # radio de las femtoceldas

# Generar mapa
width = 1024
height = 620
edifices, fcs_positions, cars_positions = build_city(width=width, height=height, edificesColor=(100, 100, 100, 128))
cars = generate_cars(init_positions=cars_positions, n_cars=n_cars, color=(20, 160, 140, 100),
                     map_size=[width, height], radius_car=radio_car, d2d=d2d)
fcs = generate_fc(init_positions=fcs_positions, n_fc=n_fc, radius_fc=radio_fc, color=(243, 34, 90, 150))

# Simular
simulator = Simulator(width=width, height=height, edifices=edifices, cars=cars, fcs=fcs, clusters=clusters)
simulator.run()
