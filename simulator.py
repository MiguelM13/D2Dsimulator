import pygame
import time

class Simulator:
    def __init__(self, width=1024, height=720, background=(255, 255, 255), walls=None, cars=None,
                 fcs=None):
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
        self.walls = walls
        self.cars = cars
        self.fcs = fcs
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
                self.fcs.draw(self.surface)
                #self.fcs.draw(self.surface)
                #self.cars.draw(self.screen)
                self.cars.draw(self.surface)
                self.walls.draw(self.screen)
                self.cars.move(self.walls)
                self.cars.updateLinksWithOthersCars(self.surface)
                self.fcs.updateLinks(self.surface, self.cars)
                
                self.cars.updateTime(dt)
                self.clock.tick(self.ticks)
                self.screen.blit(self.surface, (0, 0))
                pygame.display.flip()

            else:
                time.sleep(.5)

        playBtn.setChecked(False)
        pygame.quit()
