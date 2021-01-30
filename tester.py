from escenarios import generate_fc, generate_cars, build_city


# ------------ Parámetros de simulación ----------------

n_experiments = 10  # número de experimentos
n_clusters = 5  # número de clusters
cluster = True  # clusters bandara
d2d = True  # D2D bandera
cars_number = [10*(i+1) for i in range(n_experiments)]  # número de autos
fcs_number = [5*(i+1) for i in range(n_experiments)]  # número de femtoceldas

radio_car = 30  # radio de los autos
radio_fc = 200  # radio de las femtoceldas


# Generar mapa
width = 1024
height = 720
edifices, centers_corner, centers_street = build_city(width=width, height=height, edificesColor=(237, 237, 230))

cars = generate_cars(init_positions=centers_street, n_cars=30, color=(100, 100, 10), map_size=[width, height],
                     radius_car=30, d2d=d2d)
fcs = generate_fc(init_positions=centers_corner, n_fc=16, color=(230, 50, 30, 120), radius_fc=200)



