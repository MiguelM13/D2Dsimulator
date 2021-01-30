import pygame
from pygame.math import Vector2
from random import randint, uniform
from objects import Register
from calculos import *
from buffer import Buffer


class Car(object):
    """Objecto carro
    Args:
        x: posición en x
        y: posición en y
        inner_radius: radio interior
        radius: radio externo
        inner_color: color interno
        color: color externo
        Id: Identifcador del auto
        map_size: Dimensiones del mapa
        d2d: D2D bandera habilitar esta tecnología
    """
    max_demand = 1  # Mbps

    def __init__(self, x=0.0, y=0.0, inner_radius=3, radius=16, inner_color=(2, 2, 2, 128), color=(52, 235, 222, 128),
                 Id="Car", indx=None, map_size=None, d2d=True, stop=False):
        if map_size is None:
            map_size = [1024, 768]
        self.kind = "car"
        self.indx = indx
        self.dt = 1 / 30
        self.position = Vector2(x, y)
        self.lastPosition = self.position
        self.inner_radius = inner_radius
        self.radius = radius
        self.inner_color = inner_color
        self.color = color
        self.link_color = (20, 50, 100)
        self.Id = Id
        self.dir = randint(1, 4)
        self.lastDir = self.dir
        self.newDir = self.dir
        self.dic = {1: "Derecha", 2: "Izquierda", 3: "Arriba", 4: "Abajo"}
        self.stop = stop
        self.turn = False
        self.edificeNumbers = 0
        self.randomCounter = randint(50, 300)
        self.currentEdifice = 0
        self.i = 0
        self.collide = False
        self.speed = 1.25

        self.map_size = map_size
        pygame.font.init()
        try:
            self.font = pygame.font.Font(None, 30)
        except Exception as e:
            print(e)
        self.text_surface = self.font.render(self.Id, True, pygame.Color('dodgerblue1'))
        self.text_rect = self.text_surface.get_rect()
        self.connectionsList = Register(Id=Id)
        self.femtoID = ""
        self.femtoIndx = None
        self.d2d = d2d
        # For record
        self.distanceFC = 0
        self.isConnected = False
        self.recording = False
        self.recordLimit = 500
        self.T = 25
        self.Bw = 5

        self.buffer = Buffer(position=(0, 0), demand=0, prx=0, snri=0, interference=0)

        self.demand = 0  # Mbps
        self.prx = -100  # dBm
        self.t = 0  # segs
        self.snri = 0  #
        self.interference = 0  #

        self.Ptx = subcarrier_power(d=5.0, dB=True)
        self.updateDemand(random=False)
        self.bw_assigned = 0
        self.ym = 2  # Eficiencia espectral MC
        self.yf = 6  # Eficiencia esoectral FC
        self.No = -174  # dBm/Hz
        self.fc = 2300  # MHz

        self.pm = 60  # dBm Potencia MC
        self.pf = 10  # dBm Potencia FC

        self.Nsc = 256  # Número de Subportadoras
        self.bwsc = 15 / 1000  # MHz Ancho de Banda por subportadora
        self.bits_mod = 6
        self.subscribed = False
        self.subscriptorColorText = (200, 150, 150)
        self.subscriptorColor = (250, 200, 20, 100)
        self.subsCount = 1

        self.fcs = {}
        self.users = {}
        self.neighbors = {}
        self.maxTime = 100

    def isConnectedWith(self, user=None):
        r1 = self.radius  # radio del objecto actual
        r2 = user.inner_radius  # radio del objecto a comparar
        pos1 = self.position
        pos2 = user.position
        distance = pos2 - pos1
        rad_sum = r1 + r2
        self.distanceFC = distance.magnitude()
        if distance.magnitude() <= rad_sum:
            return True
        else:
            return False

    def connectWithNeighbors(self, surface=None):
        """El objeto actual se conectará con otros usuarios si d2d es True"""
        if self.d2d:
            for neighbor in self.neighbors.values():
                if self.isConnectedWith(user=neighbor):
                    self.drawLink(surface=surface, user=neighbor, color=(243, 122, 8))
                    self.connectionsList.add(element=neighbor)
                else:
                    self.connectionsList.delete(element=neighbor)

    def connectWithUsers(self, surface=None):
        """El objeto actual se enlazará con aquellos objetos en su área de cobertura"""
        for user in self.users.values():
            if self.isConnectedWith(user=user):
                self.drawLink(surface=surface, user=user)

    def setNeighbors(self, neighbors=None):
        """Guarda la lista de usuarios vecinos"""
        for neighbor in neighbors.values():
            if neighbor.Id != self.Id:
                self.neighbors[neighbor.Id] = neighbor

    def setFemtocells(self, fcs):
        """Guarda la lista de femtoceldas"""
        for fc in fcs.values():
            if fc.Id != self.Id:
                self.fcs[fc.Id] = fc

    def setUsers(self, users=None):
        """Guarda la lista de usuarios (Usado por femtocelda)"""
        self.users = users

    def setFemtocellUsers(self, users=None):
        self.users = users

    def setSubscription(self, femtoID=None, femtoIndx=None):
        """Subscribe el usuario a la Femtocelda indicada en ID"""
        if femtoID is not None:
            self.femtoID = femtoID
            self.subscribed = True
            self.femtoIndx = femtoIndx
            if self.femtoIndx:
                self.Id = self.femtoID + " / S" + str(self.femtoIndx)
                self.text_surface = self.font.render(self.Id, True, self.subscriptorColorText)
                self.color = self.subscriptorColor

    def clearSubscription(self):
        """Elimina la subscripción"""
        self.femtoID = ""
        self.subscribed = False
        self.femtoIndx = None
        self.Id = "C " + self.indx

    def isSubscribed(self):
        """¿Está subscrito?"""
        return self.subscribed

    def getFemtoID(self):
        """Devuelve el ID de la femtocelda subscrita"""
        return self.femtoID

    def getPosition(self):
        """Devuelve la posición actual"""
        return self.position.x, self.position.y

    def getDemand(self):
        """Devuelve el tràfico"""
        return self.demand

    def draw(self, surface):
        """Dibuja el punto (carro) sobre la superficie deseada
        Args:
            surface: objeto superficie
        """
        # External radius
        rect = pygame.Rect(self.position, (0, 0)).inflate((self.radius*2, self.radius*2))
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (self.radius, self.radius), self.radius)
        surface.blit(surf, rect)

        # Inner radius
        rect = pygame.Rect(self.position, (0, 0)).inflate((self.inner_radius*2, self.inner_radius*2))
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.circle(surf, self.inner_color, (self.inner_radius, self.inner_radius), self.inner_radius)
        surface.blit(surf, rect)

        # Text
        surface.blit(self.text_surface, self.position)

    def edificeCollide(self, edifice=None):
        """Determina si hay colisión con alguna pared
        Args:
            edifice: objeto edifiio
        """
        r = self.radius  # radio actual
        rect = edifice.rect  # rectangulo que conforma la pared
        circle_distance_x = abs(self.position.x - rect.centerx)
        circle_distance_y = abs(self.position.y - rect.centery)
        if circle_distance_x > rect.w / 2.0 + r or circle_distance_y > rect.h / 2.0 + r:
            return False
        if circle_distance_x <= rect.w / 2.0 or circle_distance_y <= rect.h / 2.0:
            return True
        corner_x = circle_distance_x - rect.w / 2.0
        corner_y = circle_distance_y - rect.h / 2.0
        corner_distance_sq = corner_x ** 2.0 + corner_y ** 2.0
        return corner_distance_sq <= r ** 2.0

    def getAroundTown(self, edifices=None):
        """Dada una lista de edificios, verificar si el auto se chocó con alguna de ellas
        Args:
            edifices: Objeto Group (grupo/lista de objetos)
        """
        # Extraer elementos del del grupo
        edifices = edifices.elements
        self.edificeNumbers = len(edifices)
        # Verificar colisión para cada pared en la lista de paredes
        for edifice in edifices.values():
            self.move(edifice)

    def updatePosition(self):
        """Actualiza la posición del auto"""
        # Derecha
        if self.dir == 1:
            self.position.x += self.speed
        # Izquierda
        if self.dir == 2:
            self.position.x -= self.speed
        # Abajo
        if self.dir == 3:
            self.position.y -= self.speed
        # Arriba
        if self.dir == 4:
            self.position.y += self.speed

    def randomTurn(self):
        """Genera un giro aleatorio cada cierto tiempo"""
        # Contador
        self.i += 1
        if self.i >= self.randomCounter:
            self.lastPosition = self.position
            self.lastDir = self.dir  # Guardar dirección anterior
            self.newDir = randint(1, 4)  # Cambiar dirección
            self.dir = self.newDir  # settear nueva dirección
            self.i = 0

    def positionLimits(self):
        """Verifica que el auto no haya salido de los límites del mapa"""
        if self.position.x >= self.map_size[0]:
            self.position.x = 1
            self.dir = 2

        if self.position.x <= 0:
            self.position.x = self.map_size[0] - 1
            self.dir = 1

        if self.position.y >= self.map_size[1]:
            self.position.y = 1
            self.dir = 4

        if self.position.y <= 0:
            self.position.y = self.map_size[1] - 1
            self.dir = 3

    def move(self, edifice=None):
        """Actualiza el estado del vehículo
        Args:
            edifice: objeto edificio
        """
        if not self.stop:
            if self.currentEdifice <= self.edificeNumbers:
                collide = self.edificeCollide(edifice)
                # Si en alguna pared hubo colisión
                if collide:
                    self.collide = collide
                self.currentEdifice += 1
            else:
                # Si se terminó la comprobación con todas las paredes
                self.currentEdifice = 0
                # Si no existe colisión con alguna mover libremente
                if not self.collide:
                    self.dir = self.newDir
                    # Generar giro aleatorio
                    self.randomTurn()
                # Si existe colisión corregir movimiento
                else:
                    self.position = self.lastPosition
                    self.dir = self.lastDir
                    self.updatePosition()
                # Limpiar estado de colisión
                self.collide = False
                # Verificar si el auto está en los límites del mapa
                self.positionLimits()
                self.updateVariables()

    def isLinkedWith(self, user):
        """Verificar si existe enlace con"""
        return self.connectionsList.isIn(user)

    def clearVariables(self):
        """Limpiar variables"""
        self.buffer.clear()
        
    def updatePrx(self):
        if self.isConnected:
            self.prx = self.Ptx - propagation_losses(d=self.distanceFC, model="FC")
        else:
            self.prx = uniform(-80, 0)

    def updateDemand(self, random=True):
        if random:
            self.demand = uniform(0, self.max_demand)
        else:
            self.demand = self.max_demand

    def updatesnri(self):
        PLvec = []
        Pscvec = []
        distance = 0
        for car in self.neighbors.values():
            if car.Id != self.Id:
                vec_dist = self.position - car.position
                distance = vec_dist.magnitude()
                if self.Id == "C19" and car.Id == "C20":
                    pass
                PL = propagation_losses(d=distance)
                PLvec.append(PL)
                Pscvec.append(car.Ptx)

        l1 = len(PLvec)
        l2 = len(Pscvec)
        if l1 > 0 and l2 > 0:
            self.interference = calculate_interference_cotier(Pj=Pscvec, PLsc=PLvec)
            self.snri = calculate_SINR(Psc=Pscvec, PLsc=PLvec, I=self.interference)

    def updateVariables(self):
        """Actualiza el valor de las variables"""
        self.updateDemand(random=False)
        self.updatePrx()
        self.updatesnri()
        position = (self.position.x, self.position.y)
        self.buffer.record(position=position, demand=self.demand, prx=self.prx, snri=self.snri,
                           interference=self.interference)

        if self.buffer.get_time_count() > 10:
            self.buffer.stop()
            if self.Id == "C19":
                # self.buffer.print_data()
                pass
            self.buffer.clear()

    def getResults(self):
        return None

    def drawLink(self, surface=None, user=None, color=(10, 10, 50)):
        """Dibujar Enlace
        Args:
            surface: objeto superficie(sobre el que se dibujar)
            user: Objeto circular, con el que se enlazará
            color: color del enlace
        """
        pygame.draw.line(surface, color, self.position, user.position, 2)

    def addSub(self):
        self.subsCount += 1

    def deleteSub(self):
        self.subsCount -= 1
        if self.subsCount < 0:
            self.subsCount = 0
