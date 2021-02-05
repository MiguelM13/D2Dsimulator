from random import randint
import pygame
from pygame.math import Vector2


class Subcarrier(object):
    def __init__(self, Id="subcarrier"):
        self.Id = Id
        self.used = False
        self.user1 = None
        self.user2 = None
        self.bw = 0.015  # MHz

    def isUsed(self):
        """¿Está en uso esta portadora?"""
        return self.used

    def setLink(self, user1=None, user2=None):
        """Guardar Link"""
        if (user1 is not None) and (user2 is not None):
            self.user1 = user1
            self.user2 = user2
            self.used = True

    def removeLink(self):
        """Elimina el enlace"""
        self.user1 = None
        self.user2 = None
        self.used = False

    def getUsersLinked(self):
        """Devolver usuarios enlazados"""
        return self.user1, self.user2


class Subcarries(object):
    def __init__(self, n_subcarriers=256, prefix="subcarrier "):
        self.n_subcarriers = n_subcarriers
        self.subcarriers = {prefix+str(i+1): Subcarrier(Id=prefix+str(i+1)) for i in range(n_subcarriers)}
        self.names = list(self.subcarriers.keys())
        self.indx = 0

    def __len__(self):
        return len(self.subcarriers)

    def getUsedCarriers(self):
        """Devuelve las subportadoras en uso"""
        usedSubcarriers = []
        for subcarrier in self.subcarriers.values():
            if subcarrier.isUsed():
                usedSubcarriers.append(subcarrier)
        return usedSubcarriers

    def getSubcarrierOf(self, user1, user2):
        if (user1 is not None) and (user2 is not None):
            for subcarrier in self.subcarriers.values():
                linked_user1, linked_user2 = subcarrier.getUsersLinked()
                if linked_user1 == user1 and linked_user2 == user2:
                    return subcarrier.Id
        return None

    def setLink(self, user1=None, user2=None):
        """Establece enlace entre dos usuarios"""
        for subcarrier in self.subcarriers.values():
            if not subcarrier.isUsed():
                subcarrier.setLink(user1, user2)
                break

    def removeLink(self, user1=None, user2=None):
        if (user1 is not None) and (user2 is not None):
            subcarrierID = self.getSubcarrierOf(user1, user2)
            if subcarrierID is not None:
                self.subcarriers[subcarrierID].removeLink()


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
        return user.Id in self.dic