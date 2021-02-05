import pygame
import time
from cluster import Cluster


class Simulator:
    def __init__(self, width=1024, height=720, background=(255, 255, 255), edifices=None, cars=None,
                 fcs=None, clusters=False):
        pygame.init()
        # pygame.display.set_caption("Escenario de simulación")
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.background_color = background
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 30
        self.exit = False
        self.screen.fill(self.background_color)

        # MAPA
        self.edifices = edifices
        self.cars = cars
        self.fcs = fcs
        self.fcs.setFemtocellUsers(cars)
        self.fcs.setNeighbors()
        self.cars.setFemtocells(fcs)
        self.cars.setNeighbors()
        self.cars.setSubscribers(n_subscribers=len(fcs), fcs=fcs)
        self.cluster = Cluster(femtocells=self.fcs, users=self.cars, enable=clusters)

        pygame.display.update()

    def run(self):
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            dt = self.clock.get_time() / 1000

            self.screen.fill(self.background_color)
            self.surface.fill(self.background_color)
            # Dibujar
            self.fcs.draw(surface=self.surface)
            self.cars.draw(surface=self.surface)
            self.edifices.draw(self.surface)
            # Mover autos
            self.cars.move(edifices=self.edifices)
            #
            self.cars.updateLinks(surface=self.surface)
            self.fcs.updateLinks(surface=self.surface)
            # self.edifices.draw(surface=self.surface)
            # if data_car and data_fc:
            #     print("Saving...")
            #     # data = {"FCS": data_fc, "CARS": data_car}
            #     # np.save("results.npy", data)
            #     self.cars.clearResults()
            #     self.fcs.clearResults()
            self.clock.tick(self.ticks)
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()
            # time.sleep(.05)

        pygame.quit()
