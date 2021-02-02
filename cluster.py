#from escenarios import generate_fc, generate_cars, build_city
import pygame
from pygame.math import Vector2
from sklearn.cluster import KMeans


class Coalition:
    def __init__(self, Id=None, centroid=None):
        self.Id = Id
        if centroid is not None:
            self.centroid = Vector2(centroid)
        self.users = {}
        self.radius = 150
        pygame.font.init()
        try:
            self.font = pygame.font.Font(None, 30)
        except Exception as e:
            print(e)
        self.text_surface = self.font.render(self.Id, True, (50, 50, 50, 50))
        self.color = [20, 90, 120, 95]
        self.inner_color = [20, 90, 120, 50]
        self.radius = 100
        self.inner_radius = 5

    def __len__(self):
        return len(self.users)

    def __sub__(self, user):
        new_users_dict = dict(self.users)
        new_users_dict.pop(user.Id)
        return new_users_dict

    def __iter__(self):
        return iter(self.users.values())

    def addUsers(self, users=None):
        if users is not None:
            for user in users.elements.values():
                if self.circleCollide(user):
                    self.users[user.Id] = user

    def getUsers(self):
        """Devuelve los usuarios"""
        return self.users

    def circleCollide(self, circle):
        """Determina si hay una colisión con un objecto circular
        Args:
            circle: objeto circular

        """
        r1 = self.radius  # radio del objecto actual
        r2 = circle.inner_radius  # radio del objecto a comparar
        pos1 = self.centroid
        pos2 = circle.position
        distance = pos2 - pos1
        rad_sum = r1 + r2
        if distance.magnitude() <= rad_sum:
            return True
        else:
            return False

    def draw(self, surface):
        pygame.draw.circle(surface, self.inner_color, self.centroid, self.inner_radius, 0)
        pygame.draw.circle(surface, self.color, self.centroid, self.radius, 0)
        surface.blit(self.text_surface, self.centroid)


class Cluster:
    def __init__(self, femtocells=None, users=None, prefix="cluster ", enable=True):
        self.femtocells = femtocells
        self.users = users
        self.groups = {}
        self.prefix = prefix

        # Kmeans
        self.centroids = None
        self.indx = 0
        self.enable = enable

    def isEnabled(self):
        return self.enable

    def isProcessing(self):
        self.indx += 1
        if self.indx <= 30:
            return False
        else:
            self.indx = 0
            return True

    def group(self, n_clusters=5):
        if self.femtocells is not None and self.users is not None:
            if self.isEnabled():
                users_positions = self.users.getSubsPositionsList()
                kmeans = KMeans(n_clusters=n_clusters).fit(users_positions)
                self.centroids = kmeans.cluster_centers_.T
                for i in range(n_clusters):
                    x = self.centroids[0][i]
                    y = self.centroids[1][i]
                    centroid = (x, y)
                    ids = "Cluster " + str(i+1)
                    self.groups[ids] = Coalition(Id=ids, centroid=centroid)
                    self.groups[ids].addUsers(users=self.users)
                self.printGroups()

    def draw(self, surface):
        if self.centroids is not None and self.isEnabled():
            for ID in self.groups:
                self.groups[ID].draw(surface)

    def printGroups(self):
        for group in self.groups.values():
            print(group.Id)
            for user in group.users.values():
                print(" -", user.Id)

    def getCoalitions(self):
        return self.groups

# width = 1024
# height = 720
# walls, centers_corner, centers_street = build_city(width=width, height=height, wallsColor=(237, 237, 230))
# cars = generate_cars(centers_street, 30, color=(100, 100, 10), mapSize=[width, height], radius=30)
# fcs = generate_fc(centers_corner, 16, 200, color=(230, 50, 30, 120))
#
# cluster = Cluster(femtocells=fcs, users=cars)
# cluster.kmeans(n_cluster=5)