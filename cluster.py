
class Cluster:
    def __init__(self, group=None):
        self.group = group
        self.groups = {}
        if self.group is not None:
            self.clustering()

    def clustering(self):
        """"""
        print("Aplicando el clustering....")

    def payoff(self):
        pass

    def function_v(self):
        pass

    def initial_number_of_carrier(self):
        """Numero de subportadoras requeridas por femtocelda
        Args:

        Returns:
        """
        pass

    def recompensa(self):
        """Recompensa de cualquier jugador (MC y FC)
        Args:
            B: Valores entre 0 y 1
        Returns:
            fiks:
        """
        pass

    def subportadoras_public_users(self):
        """Subportadoras disponibles+ para usuarios públicos
        Args:

        Returns:

        """
        pass
