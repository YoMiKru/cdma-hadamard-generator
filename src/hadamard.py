import numpy as np
import re
import inspect

class HadamardMatrix:
    """Représente une matrice de Hadamard et ses paramètres de génération."""

    def __init__(self, data, n=None, base_matrix=None, recurring_matrix=None):
        self.__n = n
        self.__matrix = np.array(data, dtype=int)
        self.__base_matrix = np.array(base_matrix, dtype=int) if base_matrix is not None else None
        self.__recurring_matrix = recurring_matrix
        self.validate()

    def validate(self):
        if self.__matrix.ndim != 2:
            raise ValueError("Doit être une matrice 2D")
        if not np.isin(self.__matrix, [-1, 1]).all():
            raise ValueError("La matrice ne doit contenir que des valeurs -1 ou 1")

    @classmethod
    def generate(cls, n, base_matrix=None, recurring_matrix=None):
        """Génère la matrice de Hadamard d'ordre n par récurrence."""
        if n < 1:
            raise ValueError("n doit être >= 1")

        H = np.array(base_matrix, dtype=int) if base_matrix is not None else np.array([[1, 1], [1, -1]])

        if recurring_matrix is None:
            def recurring_matrix(H):
                return np.block([[H, H], [H, -H]])

        for _ in range(1, n):
            H = recurring_matrix(H)

        return cls(H, n=n, base_matrix=base_matrix, recurring_matrix=recurring_matrix)

    @property
    def matrix(self):
        return self.__matrix

    def getN(self):
        return self.__n

    def getNbColumns(self):
        """Retourne le nombre de colonnes"""
        return len(self.__matrix[0])

    def getBaseMatrix(self):
        """Retourne H1 sous forme de liste Python."""
        return self.__base_matrix.tolist() if self.__base_matrix is not None else None

    def getRecurringMatrix(self):
        """
        Extrait la règle de récurrence depuis le source de recurring_matrix.
        Retourne une liste de listes de {"sign": 1|-1} représentant les blocs.
        """
        default = [[{"sign": 1}, {"sign": 1}], [{"sign": 1}, {"sign": -1}]]

        if self.__recurring_matrix is None:
            return default

        try:
            source = inspect.getsource(self.__recurring_matrix)
            match = re.search(r'np\.block\((\[\[.*?\]\])\)', source)
            if match:
                raw = match.group(1)
                rows = re.findall(r'\[(.*?)\]', raw)
                return [
                    [{"sign": -1 if el.strip().startswith('-') else 1} for el in row.split(',')]
                    for row in rows
                ]
        except (OSError, TypeError):
            pass

        return default

    def __repr__(self):
        return str(self.__matrix)