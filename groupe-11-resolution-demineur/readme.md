Equipe: Sébastien Fermigier
        Brieuc MOLKO
        Kimi HO

### 11. Résolution automatique du puzzle du Démineur

**Description du problème et contexte**
Le jeu du Démineur se résout automatiquement en modélisant le problème sous forme de CSP. Chaque case inconnue de la grille est représentée par une variable booléenne indiquant la présence ou non d'une mine. Pour chaque case ouverte, le chiffre affiché impose que le nombre de mines dans son voisinage corresponde exactement à cette valeur. La propagation de contraintes permet de déduire systématiquement quelles cases sont sûres et lesquelles contiennent une mine, bien que le problème soit NP-complet dans sa version générale.

**Références multiples**
- **Article de référence** : Bayer & Snyder (2013), [A Constraint-Based Approach to Solving Minesweeper](https://digitalcommons.unl.edu/cseconfwork/170/) - Modélisation CSP complète
- **Complexité** : [Minesweeper is NP-complete](https://www.cs.princeton.edu/~wayne/cs423/lectures/np-complete) (Princeton, 2013) - Preuve de difficulté
- **Implémentation** : [GitHub - Minesweeper_CSP](https://github.com/jgesc/Minesweeper_CSP) - Solveur en programmation par contraintes
- **Tutoriel** : Documentation sur la modélisation avec contraintes de somme sur voisinages

**Approches suggérées**
- Définir une variable booléenne par case inconnue (mine présente ou non)
- Ajouter une contrainte d'égalité sur la somme des variables de voisinage pour chaque case ouverte
- Appliquer la propagation (arc-consistency) pour réduire drastiquement l'espace de recherche
- Utiliser le backtracking intelligent pour les configurations ambiguës

**Technologies pertinentes**
- Python avec python-constraint pour une implémentation rapide
- OR-Tools CP-SAT pour la résolution efficace avec propagation avancée
- Z3 SMT solver comme alternative pour les contraintes de somme
- Interface graphique avec Pygame ou Tkinter pour la visualisation interactive

---

## Installation

1. Prérequis : Assurez-vous d'avoir Python 3.7+ installé sur votre machine.
2. Installer les dépendances : Ouvrez un terminal dans le dossier du projet et lancez : pip install -r requirements.txt