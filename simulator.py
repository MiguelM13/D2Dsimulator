import pygame
import time
import numpy as np
from cluster import Cluster


class Simulator:
    def __init__(self, width=1024, height=720, background=(255, 255, 255), walls=None, cars=None,
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
        self.ticks = 25
        self.exit = False
        self.screen.fill(self.background_color)
        self.walls = walls
        self.cars = cars
        self.fcs = fcs
        self.cars.setUsers()
        self.cars.setSubscribers(n_subscribers=16, fcs=fcs)
        self.cluster = Cluster(femtocells=self.fcs, users=self.cars, enable=clusters)

        pygame.display.update()

    def run(self, playBtn):
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            if not playBtn.isChecked():
                dt = self.clock.get_time() / 1000

                self.surface.fill(self.background_color)
                self.screen.fill(self.background_color)

                # Dibujar y actualizar grupos de objetos
                self.walls.draw(self.surface)
                self.cluster.draw(self.surface)
                self.fcs.draw(self.surface)
                self.cars.draw(self.surface)
                self.walls.draw(self.screen)

                # Cluster
                self.cluster.kmeans(n_cluster=5)


                # Move
                self.cars.move(self.walls)
                self.fcs.move(self.walls, stop=True)
                # Updates Links
                self.cars.updateLinksWithOthersCars(self.surface)
                self.fcs.updateLinks(self.surface, self.cars)
                
                self.cars.updateTime(dt)
                self.fcs.updateTime(dt)

                data_car = self.cars.getData()
                data_fc = self.fcs.getData()

                if data_car and data_fc:
                    print("Saving...")
                    # data = {"FCS": data_fc, "CARS": data_car}
                    # np.save("results.npy", data)
                    self.cars.clearResults()
                    self.fcs.clearResults()

                self.clock.tick(self.ticks)
                self.screen.blit(self.surface, (0, 0))
                pygame.display.flip()
                time.sleep(.01)
            else:
                time.sleep(.5)

        playBtn.setChecked(False)
        pygame.quit()
