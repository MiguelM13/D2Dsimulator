import numpy as np


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

    def getPositionsList(self):
        """Devuelve una lista con las posiciones"""
        return [element.getPosition() for element in self.elements.values()]

    def add(self, item=None):
        """Añade un nuevo elemento a la lista"""
        Id = self.prefix + str(self.indx)
        self.elements[Id] = item
        self.indx += 1

    def printElements(self):
        """Listar e imprimir elementos por consola """
        if self.elements:
            for Id in self.elements.keys():
                print(Id, ":", self.elements[Id])

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
            print("Grabación terminada")
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

    def keys(self):
        """Devuelve las llaves del diccionario"""
        return self.elements.keys()

    def getSubsPositionsList(self):
        """Retorna las posiciones de los subscriptores"""
        return [element.getPosition() for element in self.elements.values() if element.isSubscribed()]

    def setSubscribers(self, n_subscribers=16, fcs=None, subs_per_fc=1):
        """Asignar como subscriptor"""
        cars = self.elements
        if fcs is not None:
            cars_ids = list(cars.keys())
            fcs_ids = list(fcs.keys())
            iters = n_subscribers * subs_per_fc
            j = 0
            aux = 0
            if n_subscribers <= iters:
                for i in range(iters):
                    cars[cars_ids[i]].setSubscription(femtoID=fcs_ids[j], femtoIndx=fcs[fcs_ids[j]].subsCount)
                    fcs[fcs_ids[j]].addSub()
                    aux += 1
                    if aux >= subs_per_fc:
                        j += 1
                        aux = 0
            else:
                raise Exception('Error while setting subscribers')

    def setNeighbors(self):
        """Pasa la lista de usuarios vecinos a cada usuario"""
        for element in self.elements.values():
            element.setNeighbors(self.elements)

    def setUsers(self):
        """Pasa la lista de usuarios a cada elemento (Femtocelda)"""
        for element in self.elements.values():
            element.setUsers(self.elements)

    def setFemtocellUsers(self, users=None):
        """Pasa a cada femtocelda una lista de los usuarios"""
        for element in self.elements.values():
            element.setFemtocellUsers(users.elements)

    def setFemtocells(self, femtocells=None):
        """Pasa a cada usuario una lista de femtoceldas"""
        for element in self.elements.values():
            element.setFemtocells(self.elements)

    def draw(self, surface=None):
        """Dibujar elementos sobre la superficie
        Args:
            surface: objeto superficie
        """
        if self.elements is not None:
            for element in self.elements.values():
                element.draw(surface)

    def move(self, edifices=None):
        """ Mover
        Args:
            edifices: lista de edificios
        """
        if self.elements is not None:
            for element in self.elements.values():
                element.getAroundTown(edifices=edifices)

    def updateLinks(self, surface=None):
        if self.elements is not None:
            for element in self.elements.values():
                if element.kind == "car":  # Si es usuario
                    element.connectWithNeighbors(surface=surface)  # conectar con otros usuarios
                if element.kind == "fc":  # Si es femtocelda
                    element.connectWithUsers(surface=surface)  # conectar con usuarios

    def update(self, surface=None, edifices=None, draw=True):
        for element in self.elements.values():
            # Dibujar elementos en el mapa
            if draw and (surface is not None):
                element.draw(surface=surface)
            # Mover auto por la ciudad
            element.getAroundTown(edifices=edifices)
            # Actualizar Enlaces
            if element.kind == "car":  # Si es usuario
                element.connectWithNeighbors(surface=surface)  # conectar con otros usuarios
            if element.kind == "fc":  # Si es femtocelda
                element.connectWithUsers(surface=surface)  # conectar con usuarios