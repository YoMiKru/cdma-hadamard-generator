from src.hadamard import HadamardMatrix
from src.encoder import saveProperties
from src.correlation import Correlation
import numpy as np

base_matrix = np.array([[1, 1], [1, -1]])

def recurring_matrix(H):
    return np.block([[H, H], [H, -H]])

"""def save():
    filepath = saveProperties(h3)
    print(f"Sauvegardé : {filepath}")"""

def show_orthonal(transformation:Correlation):
    for i, c in enumerate(transformation.getAllCodes()):
        print(f"Le code {i} {c} est {'orthogonal' if Correlation.isOrthogonal(c) else 'pas orthogonal'}")

running:bool = True
while running:

    """ Les variables h* désignent les variables HadamardMatrix
        Les variables t* désignent les variables en traitement (extraction des codes, corrélation...)"""

    h3 = HadamardMatrix.generate(n=3, base_matrix=base_matrix, recurring_matrix=recurring_matrix).matrix


    t3:Correlation = Correlation(h3)
    Correlation.testing(t3)


    do_show_orthogonal:bool = True
    if do_show_orthogonal:
        show_orthonal(t3)

    """do_save:bool = False
    if do_save:
        save()"""

    running = False