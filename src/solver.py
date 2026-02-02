import random

# --- Imports ---
try:
    from constraint import Problem, ExactSumConstraint
    HAS_CONSTRAINT = True
except ImportError:
    HAS_CONSTRAINT = False

try:
    from ortools.sat.python import cp_model
    HAS_ORTOOLS = True
except ImportError:
    HAS_ORTOOLS = False

try:
    from z3 import *
    HAS_Z3 = True
except ImportError:
    HAS_Z3 = False

class MinesweeperAI:
    def __init__(self, solver_type="ortools"):
        if solver_type == "ortools" and not HAS_ORTOOLS:
            solver_type = "python-constraint"
        elif solver_type == "z3" and not HAS_Z3:
            solver_type = "python-constraint"
            
        self.solver_type = solver_type
        self.moves_queue = [] 
        self.latest_probabilities = {} 

    def compute_probabilities(self, grid, rows, cols):
        """Calcule uniquement les probabilités sans décider de coup."""
        self.latest_probabilities = {}
        variables = set()
        constraints_data = []

        for x in range(rows):
            for y in range(cols):
                cell = grid[x][y]
                if cell.is_revealed and cell.neighbor_mines > 0:
                    unknown_neighbors = []
                    known_mines = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0: continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < rows and 0 <= ny < cols:
                                n_cell = grid[nx][ny]
                                if not n_cell.is_revealed:
                                    if n_cell.is_flagged: known_mines += 1
                                    else: unknown_neighbors.append((nx, ny))
                    if unknown_neighbors:
                        variables.update(unknown_neighbors)
                        constraints_data.append((unknown_neighbors, cell.neighbor_mines - known_mines))

        if not variables: return {}

        solutions = []
        if self.solver_type == "python-constraint":
            solutions = self._solve_python_constraint(variables, constraints_data)
        elif self.solver_type == "ortools":
            solutions = self._solve_ortools(variables, constraints_data)
        elif self.solver_type == "z3":
            solutions = self._solve_z3(variables, constraints_data)

        if solutions:
            total_solutions = len(solutions)
            for var in variables:
                mine_count = sum(1 for sol in solutions if sol.get(var) == 1)
                self.latest_probabilities[var] = (mine_count / total_solutions) * 100
        
        return self.latest_probabilities

    def get_next_move(self, grid, rows, cols):
        """Cherche un coup à jouer en utilisant les probabilités déjà calculées."""
        # On s'assure d'avoir les données fraîches
        probs = self.compute_probabilities(grid, rows, cols)
        
        if not probs: return None

        # 1. Priorité aux certitudes
        for (x, y), prob in probs.items():
            if prob == 0:
                return (x, y, 'reveal', "Coup SÛR (0%)")
            if prob == 100 and not grid[x][y].is_flagged:
                return (x, y, 'flag', "Bombe CERTAINE (100%)")

        # 2. Si rien de sûr, on propose le meilleur pari
        best_var = min(probs, key=probs.get)
        risk = probs[best_var]
        return (best_var[0], best_var[1], 'reveal', f"PARI RISQUÉ ({risk:.1f}%)")

    # --- Méthodes de résolution ---
    def _solve_python_constraint(self, v, c):
        p = Problem()
        for var in v: p.addVariable(var, [0, 1])
        for neighbors, val in c: p.addConstraint(ExactSumConstraint(val), neighbors)
        return p.getSolutions()

    def _solve_ortools(self, v, c):
        model = cp_model.CpModel()
        vars_dict = {coord: model.NewBoolVar(f'v_{coord}') for coord in v}
        for neighbors, val in c: model.Add(sum(vars_dict[n] for n in neighbors) == val)
        solver = cp_model.CpSolver()
        class Collector(cp_model.CpSolverSolutionCallback):
            def __init__(self, d): super().__init__(); self.d = d; self.solutions = []
            def on_solution_callback(self): self.solutions.append({c: self.Value(v) for c, v in self.d.items()})
        coll = Collector(vars_dict); solver.SearchForAllSolutions(model, coll)
        return coll.solutions

    def _solve_z3(self, v, c):
        s = Solver()
        z_v = {coord: Int(f'v_{coord}') for coord in v}
        for var in z_v.values(): s.add(var >= 0, var <= 1)
        for neighbors, val in c: s.add(Sum([z_v[n] for n in neighbors]) == val)
        sol = []
        while s.check() == sat and len(sol) < 100:
            m = s.model(); current = {coord: m[var].as_long() for coord, var in z_v.items()}
            sol.append(current); s.add(Or([var != m[var] for var in z_v.values()]))
        return sol