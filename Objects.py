import pygame
from pygame.math import Vector2
from random import randint, uniform
from algoritmos import *
import numpy as np


class Wall(object):
    """Objeto pared
    Args:
        x: posición en x
        y: y posición en y
        width: ancho de la pared/edificio
        height: Altura
        color:
    """

    def __init__(self, x=0.0, y=0.0, width=10.0, height=10.0, color=(184, 146, 50, 128), Id="Wall"):
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
        if self.rect:
            pygame.draw.rect(surface, self.color, self.rect, 0)

    def random_position(self):
        """Aleatoriza la posición de la pared"""
        self.position.x = randint(0, 800)
        self.position.y = randint(0, 600)


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
		mapSize: Dimensiones del mapa
		d2d: D2D bandera habilitar esta tecnología
	"""
    max_traffic = 1  # Mbps

    def __init__(self, x=0.0, y=0.0, inner_radius=3, radius=16, inner_color=(2, 2, 2), color=(52, 235, 222, 50),
                 Id="Car", mapSize=[1024, 768], d2d=True):
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
        self.stop = bool(randint(0, 1))
        self.turn = False
        self.wallNumbers = 0
        self.randomCounter = randint(50, 300)
        self.currentWall = 0
        self.i = 0
        self.collide = False
        self.speed = 1

        self.mapSize = mapSize
        pygame.font.init()
        try:
            self.font = pygame.font.Font(None, 30)
        except Exception as e:
            print(e)
        self.text_surface = self.font.render(self.Id, True, pygame.Color('dodgerblue1'))
        self.text_rect = self.text_surface.get_rect()
        self.listConnections = Register(Id=Id)
        self.femtoID = ""
        self.d2d = d2d
        # For record
        self.distanceFC = 0
        self.isConnected = False
        self.recording = False
        self.recordLimit = 500
        self.T = 25
        self.Bw = 5

        self.variables = {}
        self.variables["position"] = []
        self.variables["traffic"] = []
        self.variables["Prx"] = []
        self.variables["time"] = []
        self.variables["Bw"] = []
        self.variables["Links"] = []

        self.links = []
        self.time = []
        self.demandSignal = []
        self.PrxSignal = []
        self.demand = 0  # Mbps
        self.Prx = -100  # dBm
        self.t = 0  # segs

        self.Ptx = subcarrier_power(d=5.0)
        self.updateDemand(random=True)
        self.bw_assigned = 0
        self.ym = 2  # Eficiencia espectral MC
        self.yf = 6  # Eficiencia esoectral FC
        self.No = -174  # dBm/Hz
        self.fc = 2300  # MHz

        self.pm = 60  # dBm Potencia MC
        self.pf = 10  # dBm Potencia FC

        self.Nsc = 256  # Número de Subportadoras
        self.bwsc = 15 / 1000  # MHz Ancho de Banda por subportadora

        self.subscribed = False
        self.bits_mod = 1

    def setSubscription(self, ID=None):
        """Subscribe el usuario a la Femtocelda indicada en ID"""
        if ID is not None:
            self.femtoID = ID
            self.subscribed = True

    def clearSubscription(self):
        """Elimina la subscripción"""
        self.femtoID = ""
        self.subscribed = False

    def isSubscribed(self):
        """¿Está subscrito?"""
        return self.subscribed

    def getFemtoID(self):
        """Devuelve el ID de la femtocelda subscrita"""
        return self.femtoID

    def getBandwithSC(self):
        """Devuelve el ancho de banda por subportadora"""
        return self.bwsc

    def getPowerMC(self):
        """Devuelve la potencia de la Macrocelda"""
        return self.pm

    def getPowerFC(self):
        """Devuelve la potencia de la Femtocelda"""
        return self.pf

    def getNoise(self):
        """Devuelve el ruido"""
        return self.No

    def getSpectrumEfficiencyMC(self):
        """Devuelve la eficiencia espectral de Macrocelda"""
        return self.ym

    def getSpectrumEfficiencyFC(self):
        """Devuelve la eficiencia espectral de Femtocelda"""
        return self.yf

    def getPosition(self):
        """Devuelve la posición actual"""
        return self.position.x, self.position.y

    def getBandwidth(self):
        """Devuelve el ancho de banda requerido"""
        return self.Bw

    def getPower(self):
        """Devuelve la potencia de recepción"""
        return self.Prx

    def getDemand(self):
        """Devuelve el tràfico"""
        return self.demand

    def start_recording(self):
        self.recording = False

    def draw(self, surface):
        """Dibuja el punto (carro) sobre la superficie deseada
		Args:
			surface: objeto superficie
		"""
        # External radius
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        # Inner radius
        pygame.draw.circle(surface, self.inner_color, self.position, self.inner_radius)
        # Text
        surface.blit(self.text_surface, self.position)

    def wallCollide(self, wall):
        """Determina si hay colisión con alguna pared
		Args:
			wall: objeto pared
		"""
        r = self.radius  # radio actual
        rect = wall.rect  # rectangulo que conforma la pared
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

    def WallsCollides(self, Walls, stop=False):
        """Dada una lista de paredes, verificar si el auto se chocó con alguna de ellas
		Args:
			Walls: Objeto Group (grupo/lista de objetos)
			stop: Bandera para mover o detener
		"""
        # Extraer elementos del del grupo
        walls = Walls.elements
        self.wallNumbers = len(walls)
        # Verificar colisión para cada pared en la lista de paredes
        for Id in walls.keys():
            self.move(walls[Id], stop=stop)

    def circleCollide(self, circle):
        """Determina si hay una colisión con un objecto circular
		Args:
			circle: objeto circular

		"""
        r1 = self.radius  # radio del objecto actual
        r2 = circle.inner_radius  # radio del objecto a comparar
        pos1 = self.position
        pos2 = circle.position
        distance = pos2 - pos1
        rad_sum = r1 + r2
        self.distanceFC = distance.magnitude()
        if distance.magnitude() <= rad_sum:
            return True
        else:
            return False

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
        if self.position.x >= self.mapSize[0]:
            self.position.x = 1
            self.dir = 2

        if self.position.x <= 0:
            self.position.x = self.mapSize[0] - 1
            self.dir = 1

        if self.position.y >= self.mapSize[1]:
            self.position.y = 1
            self.dir = 4

        if self.position.y <= 0:
            self.position.y = self.mapSize[1] - 1
            self.dir = 3

    def move(self, wall, stop=False):
        """Actualiza el estado del vehículo
		Args:
			wall: objeto pared
			stop: Bandera para detener el auto
		"""
        if self.currentWall <= self.wallNumbers:
            collide = self.wallCollide(wall)
            # Si en alguna pared hubo colisión
            if collide:
                self.collide = collide
            self.currentWall += 1
        else:
            # Si se terminó la comprobación con todas las paredes
            self.currentWall = 0
            # Si no existe colisión con alguna mover libremente
            if not self.collide:
                self.dir = self.newDir
                # self.move(wall)
                # Generar giro aleatorio
                if not stop:
                    self.randomTurn()
            # Si existe colisión corregir movimiento
            else:
                self.position = self.lastPosition
                self.dir = self.lastDir
                if not stop:
                    self.updatePosition()
            # Limpiar estado de colisión
            self.collide = False
            # Verificar si el auto está en los límites del mapa
            self.positionLimits()
            self.updateVariables()

    def checkLinks(self, surface, Cars):
        cars = Cars.getElements()
        for Id in cars.keys():
            self.updateLink(surface, cars[Id])

    def carsLinks(self, surface, cars):
        for Id in cars.keys():
            if Id != self.Id:
                self.updateCarsLinks(surface, cars[Id])

    def updateCarsLinks(self, surface, car):
        """Verifica si existe enlace con otros autos"""
        if self.circleCollide(car) and self.d2d:
            self.drawLink(surface, car, color=(200, 100, 50))

    def clearVariables(self):
        """Limpiar variables"""
        self.t = 0
        self.variables["position"] = []
        self.variables["traffic"] = []
        self.variables["Prx"] = []
        self.variables["time"] = []
        self.variables["Bw"] = []
        self.variables["Links"] = []

    def printVariables(self):
        print("--------------------------------------")
        print(self.Id)
        print("  **Tráfico: ", self.variables["traffic"][:5])
        print("")
        print(" **Prx: ", self.variables["Prx"][:5])
        print("")
        print(" **time: ", self.variables["time"][:5])
        print("")

    def updatePrx(self):
        if self.isConnected:
            self.Prx = self.Ptx - propagation_losses(d=self.distanceFC, model="FC")
        else:
            self.Prx = uniform(-80, 0)

    def updateDemand(self, random=True):
        if random:
            self.demand = uniform(0, self.max_traffic)
        else:
            self.demand = self.max_traffic

    def updateVariables(self):
        """Actualiza el valor de las variables"""
        self.updateDemand()
        self.updatePrx()
        Bw = 5  #
        # self.variables["position"].append([self.position.x, self.position.y])
        self.variables["traffic"].append(self.demand)
        self.variables["Prx"].append(self.Prx)
        self.variables["Bw"].append(Bw)
        self.variables["Links"].append(self.listConnections.getData())
        if self.Id == "C1":
            # print("{} Time:{:.2f} , {}".format(self.Id, self.t, len(self.variables["traffic"])))
            pass
        if self.t >= self.T:
            self.clearVariables()

    def updateTime(self, dt):
        self.t += dt

    def getResults(self):
        return dict(self.variables)

    def updateLink(self, surface, car):
        """Verificar si existe enlace con algún objeto circular
		Args:
			surface: objeto superficie(sobre el que se dibujar)
			car: Objeto circular, con el que se enlazará
		"""
        # si está dentro del área de cobertura (si hay colisión) enlazar
        self.isConnected = self.circleCollide(car)
        if self.isConnected:
            self.drawLink(surface, car)
            self.listConnections.add(car)
        # self.listConnections.showElements() #muestra los autos conectados en la femtocelda
        else:
            self.listConnections.delete(car)

    # self.listConnections.showElements()

    def drawLink(self, screen, car, color=(10, 10, 50)):
        """Dibujar Enlace
		Args:
			screen: objeto superficie(sobre el que se dibujar)
			car: Objeto circular, con el que se enlazará
			color: color del enlace
		"""
        pygame.draw.line(screen, color, self.position, car.position, 2)

    def random_position(self):
        """Generar posición aleatoria"""
        self.position.x = randint(0, 800)
        self.position.y = randint(10, 600)


class Femtocell(Car):
    """Objeto Femtocelda Hereda del objeto carro métodos y atributos"""

    def __init__(self, x=0.0, y=0.0, radius=40, inner_radius=5, color=(100, 100, 58, 128),
                 inner_color=(10, 100, 58, 180), Id="Femtocell"):
        super().__init__(x=x, y=y, color=color, radius=radius, inner_radius=inner_radius, Id=Id)
        self.radius = radius
        self.inner_radius = inner_radius
        self.color = color
        self.inner_color = inner_color
        self.Id = Id
        pygame.font.init()
        try:
            self.font = pygame.font.Font(None, 30)
        except Exception as e:
            print(e)
        self.text_surface = self.font.render(self.Id, True, pygame.Color('dodgerblue1'))
        self.text_rect = self.text_surface.get_rect()

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


class Register(object):
    """Objeto registro, empleado para almacenar los enlaces"""

    def __init__(self, Id="R"):
        super().__init__()
        self.dic = {}
        self.Id = Id

    def add(self, element):
        """Añade un elemento al registro"""
        Id = element.Id
        if Id not in self.dic:
            self.dic[Id] = element

    def delete(self, element):
        """Elimina elemento del registro"""
        Id = element.Id
        if Id in self.dic:
            self.dic.pop(Id)

    def showElements(self):
        """Muestra los elementos"""
        print(self.Id, ": ", list(self.dic.keys()))

    def getData(self):
        return list(self.dic.keys())


class Group(object):
    """Objeto Group, almacena en una lista diversos objetos"""

    def __init__(self, prefix="default"):
        self.elements = {}
        self.results = {}
        self.indx = 1
        self.prefix = prefix
        self.t = 0
        self.T = 20
        self.time = []
        self.demandDict = {}

    def __getitem__(self, key):
        return self.elements[key]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def __len__(self):
        return len(self.elements)

    def getElements(self):
        """Retorna el diccionario con los elementos del grupo"""
        return self.elements

    def getPositionsDict(self):
        """Devuelve un diccinario con las posiciones de cada elemento"""
        return {ID: self.elements[ID].getPosition() for ID in self.elements}

    def add(self, item):
        """Añade un nuevo elemento a la lista"""
        Id = self.prefix + str(self.indx)
        self.elements[Id] = item
        self.indx += 1

    def draw(self, surface):
        """Dibujar elementos sobre la superficie
        Args:
            surface: objeto superficie
        """
        if self.elements:
            for Id in self.elements.keys():
                self.elements[Id].draw(surface)

    def printElements(self):
        """Listar e imprimir elementos por consola """
        if self.elements:
            for Id in self.elements.keys():
                print(Id, ":", self.elements[Id])

    def move(self, walls=None, stop=False):
        """move objects"""
        if self.elements:
            for Id in self.elements.keys():
                if walls is not None:
                    self.elements[Id].WallsCollides(walls, stop=stop)

    def updateLinks(self, surface, cars):
        """Actualiza los enlaces"""
        if self.elements:
            for Id in self.elements.keys():
                self.elements[Id].checkLinks(surface, cars)

    def updateLinksWithOthersCars(self, surface):
        """Actualiza los enlaces entre autos"""
        if self.elements:
            for Id in self.elements.keys():
                self.elements[Id].carsLinks(surface, self.getElements())

    def clearResults(self):
        """Limpia los resultados obtenidos"""
        self.results = {}
        for Id in self.elements.keys():
            self.elements[Id].clearVariables()
        self.time = []

    def readResults(self):
        """Lee los resultados del experimento"""
        for Id in self.elements.keys():
            self.results[Id] = self.elements[Id].getResults()
        self.results["time"] = self.time
        return dict(self.results)

    def printResults(self):
        """Imprime los resultados en un formato bonito"""
        for Id in self.results:
            print("--------------------------------------")
            print(Id)
            print("  **Tráfico: ", self.results[Id]["traffic"][:5])
            print("")
            print(" **Prx: ", self.results[Id]["Prx"][:5])
            print("")
            print(" **time: ", self.results[Id]["time"][:5])
            print("")

    def getData(self):
        """Devuelve los resultados obtenidos"""
        if self.t >= self.T:
            self.t = 0
            print("Grabacin terminada")
            return self.readResults()
        else:
            return None

    def updateTime(self, dt):
        """Actualiza el tiempo de ejecución
        Args:
            dt: Intervalo de tiempo transcurrido
        """
        self.time.append(self.t)
        self.t += dt
        for Id in self.elements.keys():
            self.elements[Id].updateTime(dt)

    def getCars(self):
        """Retorna los elementos del diccionario usando el nombre de Cars"""
        return self.elements

    def getFCs(self):
        """Retorna los elementos del diccionario usando el nombre de FC"""
        return self.elements

    def getItem(self, ID):
        """Devuelve un elemento del diccionario de objectos
        Args:
            ID: Identificador del elemento
        """
        return self.elements[ID]

    def updateDemandDict(self):
        self.demandDict = {ID: self.elements[ID].getDemand() for ID in self.elements}

    def getDemandDict(self):
        """Retorna un dicionario con el tráfico"""
        self.updateDemandDict()
        return self.demandDict

    def getTotalDemand(self):
        """Devuelve la demanda total"""
        return np.sum(list(self.demandDict.values()))

    def getNumberSCAverage(self):
        return 1