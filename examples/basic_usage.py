from src.hadamard import HadamardMatrix
from src.encoder import saveProperties
import numpy as np

base_matrix = np.array([[1, 1], [1, -1]])

def recurring_matrix(H):
    return np.block([[H, H], [H, -H]])

h3 = HadamardMatrix.generate(n=3, base_matrix=base_matrix, recurring_matrix=recurring_matrix)

filepath = saveProperties(h3)
print(f"Sauvegardé : {filepath}")