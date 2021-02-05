from car import Car
import pygame


class Femtocell(Car):
    """Objeto Femtocelda Hereda del objeto carro métodos y atributos"""

    def __init__(self, x=0.0, y=0.0, radius=40, inner_radius=5, color=(100, 100, 58, 128),
                 inner_color=(10, 100, 58, 128), Id="Femtocell", indx=None, stop=True):
        super().__init__(x=x, y=y, color=color, radius=radius, inner_radius=inner_radius, Id=Id, indx=indx, stop=stop)
        self.radius = radius
        self.inner_radius = inner_radius
        self.color = color
        self.inner_color = inner_color
        self.Id = Id
        self.indx = indx
        self.stop = stop
        pygame.font.init()
        try:
            self.font = pygame.font.Font(None, 30)
        except Exception as e:
            print(e)
        self.textColor = (20, 210, 105)
        self.text_surface = self.font.render(self.Id, True, self.textColor)
        self.text_rect = self.text_surface.get_rect()
        self.kind = "fc"

    def draw(self, surface):
        """Se renueva la funcion dibujar, para dibujar dos circulos(centro y área de cobertura)
        Args:
            surface: objeto superficie
        """
        # External circle
        pygame.draw.circle(surface, self.color, self.position, self.radius, 0)
        # Inner circle
        pygame.draw.circle(surface, self.inner_color, self.position, self.inner_radius, 0)
        # Text
        surface.blit(self.text_surface, self.position)
