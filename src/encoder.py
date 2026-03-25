import json
from datetime import datetime
from src.hadamard import HadamardMatrix
import os

# Racine du projet (remonte d'un niveau depuis src/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

    folder = os.path.join(ROOT, "matrices_output")
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