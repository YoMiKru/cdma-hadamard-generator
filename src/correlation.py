import numpy as np
from src.hadamard import HadamardMatrix 

class Correlation:
    """Récupère les codes (ou colonnes) d'une matrice hadamard et test leur corrélation. Les codes non orthonnaux sont ignorés."""

    def __init__(self, hadamard_matrix):
        self.__hadamard_matrix:HadamardMatrix = hadamard_matrix

        self.__codes:list[np.array] = []
        self.__valid_codes:list[np.array] = []
        self.__invalid_codes:list[np.array] = []

        self.extractCodes()
        self.ValidCodes()

    @staticmethod
    def isOrthogonal(code:np.array) -> bool:
        """Vérifie l'orthogonalité des codes. Si la somme des valeurs d'un code est égal à 0 alors elle est orthogonal. Retourne un bool """
        sum:int = 0
        orthogonal:bool = False
        for n in code:
            sum += n

        if(sum == 0):
            orthogonal = True

        return orthogonal
    
    def ValidCodes(self):
        """Retourne une liste des codes """
        for c in self.__codes:
            if Correlation.isOrthogonal(c):
                self.__valid_codes.append(c)
            else:
                self.__invalid_codes.append(c)
    def extractCodes(self):
        """Récupère les codes, les colonnes de la matrices et les retournes sous forme de liste d'array"""
        for row in self.__hadamard_matrix:
            code = np.array([], dtype=int)
            for value in row:
                code = np.append(code, value)
                
            self.__codes.append(code)

    def getAllCodes(self) -> list[np.array]:
        """Retourne une liste de tout les codes possibles."""
        return(self.__codes)
    
    def getCode(self, index) -> np.array:
        """Retourne un code du numéro de l'index. (Index débute à 0)"""
        return(self.__codes[index])

    def getValidCodes(self) -> list[np.array]:
        """Retourne une liste des codes orthogonaux."""
        return(self.__valid_codes)

    def getInvalidCodes(self) -> list[np.array]:
        """Retourne une liste des codes non orthogonaux."""
        return(self.__invalid_codes)