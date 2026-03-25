import os
import json
from datetime import datetime
import numpy as np
import inspect
import re


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

    def getNbUser(self):
        """Retourne le nombre d'utilisateurs (= nombre de colonnes)."""
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


class CompactArrayEncoder(json.JSONEncoder):
    """
    Encodeur JSON personnalisé : garde les tableaux de nombres et d'objets
    sur une seule ligne pour un fichier lisible.
    """

    def encode(self, obj):
        if isinstance(obj, dict):
            items = [f'    {json.dumps(k)}: {self._encode_value(v)}' for k, v in obj.items()]
            return '{\n' + ',\n'.join(items) + '\n}'
        return super().encode(obj)

    def _encode_value(self, v):
        # Tableau 1D de nombres → une ligne
        if isinstance(v, list) and all(isinstance(i, (int, float)) for i in v):
            return json.dumps(v)
        # Tableau 2D (nombres ou objets) → une ligne par ligne
        if isinstance(v, list) and all(isinstance(i, list) for i in v):
            rows = ', '.join(
                '[' + ', '.join(json.dumps(cell) for cell in row) + ']'
                for row in v
            )
            return f'[{rows}]'
        return json.dumps(v, ensure_ascii=False)


def _recurring_matrix_to_readable(recurring_matrix_machine):
    """Convertit la représentation machine de recurring_matrix en string lisible humain."""
    rows = [
        '[' + ', '.join('-Hn' if cell["sign"] == -1 else 'Hn' for cell in row) + ']'
        for row in recurring_matrix_machine
    ]
    return f'[{", ".join(rows)}]'


def saveProperties(matrix_obj):
    """
    Sauvegarde la matrice de Hadamard et ses paramètres dans un fichier JSON.
    Retourne le chemin du fichier créé.
    """
    if not isinstance(matrix_obj, HadamardMatrix):
        raise ValueError("Vous devez passer un objet HadamardMatrix")

    folder = os.path.join(os.path.dirname(__file__), "matrices_output")
    os.makedirs(folder, exist_ok=True)

    recurring_matrix_machine = matrix_obj.getRecurringMatrix()

    content = {
        "timestamp": datetime.now().isoformat(),
        "n": matrix_obj.getN(),
        "base_matrix": matrix_obj.getBaseMatrix(),
        "recurring_matrix_readable": _recurring_matrix_to_readable(recurring_matrix_machine),
        "recurring_matrix": recurring_matrix_machine,
        "matrix_finale": [row.tolist() for row in matrix_obj.matrix],
        "nb_user": matrix_obj.getNbUser()
    }

    filename = f"matrix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as f:
        f.write(CompactArrayEncoder().encode(content))

    return filepath


if __name__ == "__main__":
    base_matrix = np.array([[1, 1], [1, -1]])

    def recurring_matrix(H):
        return np.block([[H, H], [H, -H]])

    h3 = HadamardMatrix.generate(n=3, base_matrix=base_matrix, recurring_matrix=recurring_matrix)

    filepath = saveProperties(h3)
    print(f"Sauvegardé : {filepath}")