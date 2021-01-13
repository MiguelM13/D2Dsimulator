import pygame
from pygame.math import Vector2
from random import randint, uniform
from algoritmos import *


class Wall(object):
    """Objeto pared
	Args:
	"""
    def __init__(self, x=0.0, y=0.0, width=10.0, height=10.0, color=(184, 146, 50, 128), Id="Wall"):
        self.position = Vector2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.rect = self.getRect()
        self.Id = Id

    def getRect(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def draw(self, surface):
        """Dibuja la pared sobre la superficie deseada
		Args:
			surface: objeto superficie
		"""
        if self.rect:
            pygame.draw.rect(surface, self.color, self.rect, 0)

    def random_position(self):
        self.position.x = randint(0, 800)
        self.position.y = randint(0, 600)


class Car(object):
	max_traffic = 100  # Mbps

	def __init__(self, x=0.0, y=0.0, inner_radius=3, radius=16, inner_color=(2, 2, 2), color=(52, 235, 222, 50),
				 Id="Car", mapSize=[1024, 768]):
		self.dt = 1/30
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

		# For record
		self.distanceFC = 0
		self.isConnected = False
		self.recording = False
		self.recordLimit = 500
		self.T = 15
		self.variables = {}
		self.variables["position"] = []
		self.variables["traffic"] = []
		self.variables["Prx"] = []
		self.variables["time"] = []

		self.links = []
		self.time = []
		self.trafficSignal = []
		self.PrxSignal = []
		self.traffic = 0 # Mbps
		self.Prx = -100 # dBm
		self.t = 0 # segs


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

	def WallsCollides(self, Walls):
		"""Dada una lista de paredes, verificar si el auto se chocó con alguna de ellas
		Args:
			Walls: Objeto Group (grupo/lista de objetos)
		"""
		# Extraer elementos del del grupo
		walls = Walls.elements
		self.wallNumbers = len(walls)
		# Verificar colisión para cada pared en la lista de paredes
		for Id in walls.keys():
			self.move(walls[Id])

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

		if distance.magnitude() <= rad_sum:
			return True
		else:
			return False

	def updatePosition(self):
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
		"""Genera un giro aleatorio cada cierto tiempo
		"""
		# Contador
		self.i += 1
		if self.i >= self.randomCounter:
			self.lastPosition = self.position
			self.lastDir = self.dir  # Guardar dirección anterior
			self.newDir = randint(1, 4)  # Cambiar dirección
			self.dir = self.newDir  # settear nueva dirección
			self.i = 0

	def positionLimits(self):
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

	def move(self, wall):
		"""Actualiza el estado del vehículo
		Args:
			wall: objeto pared
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
				#self.move(wall)
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
		if self.circleCollide(car):
			self.drawLink(surface, car, color=(200,100,50))
	

	def update_traffic(self):
		"""Actualiza el tráfico generado por cada auto"""
		self.traffic = uniform(0, self.max_traffic)*self.dt
		if len(self.trafficSignal) > self.recordLimit:
			# print('Trafico ', self.Id, ' :', self.trafficSignal)
			self.trafficSignal = []

	def clearVariables(self):
		self.t =0
		self.variables["position"] = []
		self.variables["traffic"] = []
		self.variables["Prx"] = []
		self.variables["time"] = []		

	def printVariables(self):
		print("--------------------------------------")
		print(self.Id)
		print("  **Tráfico: ", self.variables["traffic"][:5])
		print("")
		print(" **Prx: ", self.variables["Prx"][:5])
		print("")
		print(" **time: ", self.variables["time"][:5])
		print("")

	def updateVariables(self):
		"""Actualiza el valor de las variables"""
		self.traffic = uniform(0, self.max_traffic)*self.dt
		self.Prx = uniform(-75, 0)
		#self.variables["position"].append([self.position.x, self.position.y])
		self.variables["traffic"].append(self.traffic)
		self.variables["Prx"].append(self.Prx)
		if self.Id == "C1":
			print("{} Time:{:.2f} , {}".format(self.Id, self.t, len(self.variables["traffic"])))
		if self.t >= self.T :
			self.clearVariables()

	def updateTime(self, dt):
		self.t+=dt

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
			# self.listConnections.showElements()
		else:
			self.listConnections.delete(car)
		#self.listConnections.showElements()

	def drawLink(self, screen, car, color=(10,10, 50)):
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
		if not Id in self.dic:
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
		return None


class Group(object):
	"""Objeto Group, almacena en una lista diversos objetos"""

	def __init__(self, prefix="default"):
		self.elements = {}
		self.results = {}
		self.indx = 1
		self.prefix = prefix
		self.t = 0
		self.T = 10
		self.time = []

	def getElements(self):
		return self.elements

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
		""" Listar e imprimir elementos por consola """
		if self.elements:
			for Id in self.elements.keys():
				print(Id, ":", self.elements[Id])

	def move(self, walls=None):
		"""move objects"""
		if self.elements:
			for Id in self.elements.keys():
				if walls is not None:
					self.elements[Id].WallsCollides(walls)

	def updateLinks(self, surface, cars):
		""""""
		if self.elements:
			for Id in self.elements.keys():
				self.elements[Id].checkLinks(surface, cars)

	def updateLinksWithOthersCars(self, surface):
		if self.elements:
			for Id in self.elements.keys():
				self.elements[Id].carsLinks(surface, self.getElements())

	def clearResults(self):
		self.results = {}
		for Id in self.elements.keys():
			self.elements[Id].clearVariables()
		self.time = []

	def readResults(self):
		for Id in self.elements.keys():
			self.results[Id] = self.elements[Id].getResults()
		self.results["time"] = self.time
		np.save("results.npy", self.results)
		#self.printResults()
		print("Grabación Terminada!", len(self.time))

	def printResults(self):
		for Id in self.results:
			print("--------------------------------------")
			print(Id)
			print("  **Tráfico: ", self.results[Id]["traffic"][:5])
			print("")
			print(" **Prx: ", self.results[Id]["Prx"][:5])
			print("")
			print(" **time: ", self.results[Id]["time"][:5])
			print("")

	def updateTime(self, dt):
		self.time.append(self.t)
		self.t+=dt 
		for Id in self.elements.keys():
			self.elements[Id].updateTime(dt)

		if self.t >= self.T:
			self.readResults()
			self.clearResults()
			self.t = 0