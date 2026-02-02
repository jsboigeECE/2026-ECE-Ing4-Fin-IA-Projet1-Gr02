# Architecture Technique

## Modélisation CSP
Chaque case $(i, j)$ est une variable $X_{i,j} \in \{0, 1\}$.
Une case révélée avec le chiffre $N$ impose la contrainte : $\sum_{v \in Voisins} X_v = N$.

## Modules
- **Model** : Gestion de l'état du jeu.
- **Solver** : Moteur d'inférence.
- **GUI** : Visualisation Pygame.