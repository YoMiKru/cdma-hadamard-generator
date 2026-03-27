# cdma-hadamard-generator

Générateur de matrices de Hadamard pour systèmes CDMA.  
Les matrices \(H_n\) sont produites par récurrence à partir d'une base \(H_1\) et d'une règle configurable.  
Les paramètres de génération (base, récurrence, matrice finale, nombre d'utilisateurs) peuvent être exportés automatiquement en JSON.

---

## Utilisation

Il n’existe pas encore d’interface graphique.  
Vous pouvez consulter l’exemple fourni dans `examples/basic_usage.py`.  

Pour exécuter cet exemple depuis la racine du projet :  

```bash
python -m examples.basic_usage
```

## État du projet

Le projet est en cours de développement.
Si vous rencontrez des comportements inattendus, des erreurs ou des anomalies, vos retours sont les bienvenus.

## Fonctionnalités prévues
- Interface pour visualiser plus facilement les codes et les messages transformés.
- Amélioration de l’export JSON pour inclure toutes les informations sur la corrélation et l’orthogonalité.
- Visualisation des messages et des codes CDMA pour faciliter les tests et les simulations.