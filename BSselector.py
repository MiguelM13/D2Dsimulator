from Escenarios import build_city, generate_cars, generate_fc

def bs_selection(femtocells=None, users=None):
    fc_pos = femtocells.getPositionsDict()
    print(fc_pos)

width = 1024
height = 720
walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(237, 237, 230))
cars = generate_cars(centers_street, 30, color=(100, 100, 10), mapSize=[width, height], radius=30)
fcs = generate_fc(centers_corner, 16, 200, color=(230, 50, 30, 120))

bs_selection(femtocells=fcs)
#wwf_algorithm(users=cars, femtocells=fcs)
