import numpy as np
from src.hadamard import HadamardMatrix 

class Correlation:
    """Récupère les codes (colonnes) d'une matrice de Hadamard et teste leur orthogonalité."""

    def __init__(self, hadamard_matrix, check_orthogonality: bool = True):
        # accepte soit l'objet soit directement la matrice numpy
        if isinstance(hadamard_matrix, HadamardMatrix):
            self.__hadamard_matrix = hadamard_matrix.matrix
        else:
            self.__hadamard_matrix = np.array(hadamard_matrix)

        self.__codes: list[np.array] = []
        self.__valid_codes: list[np.array] = []
        self.__invalid_codes: list[np.array] = []

        self.extractCodes()

        if(check_orthogonality):
            self.classify_codes()
        else:
            self.__valid_codes = self.__codes.copy()
            self.__invalid_codes = []

    @staticmethod
    def isBalanced(code: np.array) -> bool:
        """Vérifie si un code est équilibré (+1 et -1 en même nombre)."""
        return np.sum(code) == 0

    @staticmethod
    def isOrthogonal(code1: np.array, code2: np.array) -> bool:
        """Vérifie si deux codes sont orthogonaux."""
        return np.dot(code1, code2) == 0
    
    def check_all_orthogonal(self) -> bool:
        """Vérifie si toutes les paires de codes sont orthogonales."""
        n = len(self.__codes)

        for i in range(n):
            for j in range(i + 1, n):
                if not Correlation.isOrthogonal(self.__codes[i], self.__codes[j]):
                    print(f"Codes {i} et {j} non orthogonaux")
                    return False

        return True

    def classify_codes(self):
        """Classe les codes en valides (orthogonaux avec tous) et invalides."""
        n = len(self.__codes)
        self.__valid_codes = []
        self.__invalid_codes = []

        for i in range(n):
            is_valid = True

            for j in range(n):
                if i != j:
                    if not Correlation.isOrthogonal(self.__codes[i], self.__codes[j]):
                        is_valid = False
                        break

            if is_valid:
                self.__valid_codes.append(self.__codes[i])
            else:
                self.__invalid_codes.append(self.__codes[i])

    def extractCodes(self):
        """Récupère les colonnes de la matrice (codes CDMA)."""
        self.__codes = [
            self.__hadamard_matrix[:, i]
            for i in range(self.__hadamard_matrix.shape[1])
        ]
    

    def getAllCodes(self) -> list[np.array]:
        return self.__codes
    
    def getCode(self, index) -> np.array:
        return self.__codes[index]

    def getValidCodes(self) -> list[np.array]:
        return self.__valid_codes

    def getInvalidCodes(self) -> list[np.array]:
        return self.__invalid_codes