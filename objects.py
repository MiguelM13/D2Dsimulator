from random import randint
import pygame
from pygame.math import Vector2


class Edifice(object):
    """Objeto Edificio
    Args:
        x: posición en x
        y: y posición en y
        width: ancho de la pared/edificio
        height: Altura
        color:
    """

    def __init__(self, x=0.0, y=0.0, width=10.0, height=10.0, color=(184, 146, 50, 128), Id="Edifice"):
        self.position = Vector2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.rect = self.getRect()
        self.Id = Id

    def getRect(self):
        """Devuelve un rectangulo que representa una pared"""
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def draw(self, surface):
        """Dibuja la pared sobre la superficie deseada
        Args:
            surface: objeto superficie
        """
        shape_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.color, shape_surf.get_rect())
        surface.blit(shape_surf, self.rect)


    def random_position(self):
        """Aleatoriza la posición de la pared"""
        self.position.x = randint(0, 800)
        self.position.y = randint(0, 600)


class Register(object):
    """Objeto registro, empleado para almacenar los enlaces"""

    def __init__(self, Id="R"):
        super().__init__()
        self.dic = {}
        self.Id = Id

    def add(self, element=None):
        """Añade un elemento al registro"""
        Id = element.Id
        if Id not in self.dic:
            self.dic[Id] = Id

    def delete(self, element=None):
        """Elimina elemento del registro"""
        Id = element.Id
        if Id in self.dic:
            self.dic.pop(Id)

    def showElements(self):
        """Muestra los elementos"""
        print(self.Id, ": ", list(self.dic.keys()))

    def getData(self):
        return list(self.dic.keys())

    def isIn(self, user):
        return user.Id in list(self.dic.keys())