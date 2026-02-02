import pygame
import random
import sys
from solver import MinesweeperAI 

# --- CONFIGURATION INITIALE ---
print("--- CONFIGURATION DU DÉMINEUR ---")
try:
    ROWS = int(input("Nombre de lignes (défaut 10) : ") or 10)
    COLS = int(input("Nombre de colonnes (défaut 10) : ") or 10)
    
    total_cells = ROWS * COLS
    # Suggestion de difficulté (~15% de mines)
    recommended_mines = int(total_cells * 0.15)
    
    print(f"💡 Recommandation pour cette taille : {recommended_mines} mines.")
    user_mines = input(f"Nombre de mines (max {total_cells - 1}) : ")
    
    if not user_mines:
        MINES_COUNT = recommended_mines
    else:
        MINES_COUNT = int(user_mines)
    
    # Sécurité anti-blocage : maximum cases - 1
    if MINES_COUNT >= total_cells:
        print(f"⚠️ Trop de mines ! Ajustement automatique à {total_cells - 1}.")
        MINES_COUNT = total_cells - 1
    elif MINES_COUNT < 1:
        MINES_COUNT = 1

except ValueError:
    print("Entrée invalide, valeurs par défaut activées.")
    ROWS, COLS, MINES_COUNT = 10, 10, 15

# Paramètres visuels
TILE_SIZE = 50
INFO_HEIGHT = 110 
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE + INFO_HEIGHT

# Couleurs
WHITE, BLACK, GRAY_COV, GRAY_REV = (255,255,255), (0,0,0), (192,192,192), (220,220,220)
RED, BLUE, GREEN, YELLOW = (255,0,0), (0,0,255), (0,128,0), (200,200,0)

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
        self.mine_probability = None 

    def draw(self, surf, font, p_font):
        rect = pygame.Rect(self.y * TILE_SIZE, self.x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if self.is_revealed:
            pygame.draw.rect(surf, GRAY_REV, rect)
            pygame.draw.rect(surf, (100,100,100), rect, 1)
            if self.is_mine: 
                pygame.draw.circle(surf, RED, rect.center, TILE_SIZE//4)
            elif self.neighbor_mines > 0:
                txt = font.render(str(self.neighbor_mines), True, BLACK)
                surf.blit(txt, txt.get_rect(center=rect.center))
        else:
            pygame.draw.rect(surf, GRAY_COV, rect)
            pygame.draw.rect(surf, WHITE, rect, 1)
            
            # Retour à l'affichage "F" pour les drapeaux
            if self.is_flagged:
                f_txt = font.render("F", True, RED)
                surf.blit(f_txt, f_txt.get_rect(center=rect.center))
            elif self.mine_probability is not None:
                p = self.mine_probability
                color = GREEN if p < 20 else (YELLOW if p < 50 else RED)
                p_txt = p_font.render(f"{int(p)}%", True, color)
                surf.blit(p_txt, p_txt.get_rect(center=rect.center))

class MinesweeperGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Démineur IA")
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.p_font = pygame.font.SysFont('Arial', 14, bold=True)
        self.ai = MinesweeperAI()
        self.ai_active = False
        self.last_msg = "Prêt"
        self.start_new_game()

    def start_new_game(self):
        self.grid = [[Cell(x, y) for y in range(COLS)] for x in range(ROWS)]
        self.game_over = self.won = False
        self.first_click = True
        self.last_msg = "Premier clic libre !"

    def update_analysis(self):
        if self.first_click or self.game_over: return
        probs = self.ai.compute_probabilities(self.grid, ROWS, COLS)
        for row in self.grid:
            for cell in row:
                cell.mine_probability = probs.get((cell.x, cell.y))

    def handle_click(self, pos, btn):
        if self.game_over: return
        x, y = pos[1] // TILE_SIZE, pos[0] // TILE_SIZE
        if x >= ROWS: return
        
        if btn == 3: # Clic Droit : Drapeau
            self.grid[x][y].is_flagged = not self.grid[x][y].is_flagged
        elif btn == 1: # Clic Gauche : Révéler
            if self.first_click:
                self.place_mines(x, y); self.first_click = False
            self.reveal_cell(x, y)
        
        self.check_win()
        self.update_analysis()

    def place_mines(self, sx, sy):
        pos = [(x,y) for x in range(ROWS) for y in range(COLS) if (x,y)!=(sx,sy)]
        for x, y in random.sample(pos, MINES_COUNT): self.grid[x][y].is_mine = True
        for x in range(ROWS):
            for y in range(COLS):
                if not self.grid[x][y].is_mine:
                    self.grid[x][y].neighbor_mines = sum(1 for n in self.get_neighbors(x,y) if n.is_mine)

    def get_neighbors(self, x, y):
        res = []
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < ROWS and 0 <= ny < COLS and (dx!=0 or dy!=0): res.append(self.grid[nx][ny])
        return res

    def reveal_cell(self, x, y):
        c = self.grid[x][y]
        if c.is_revealed or c.is_flagged: return
        c.is_revealed = True
        if c.is_mine: self.game_over = True; self.last_msg = "BOOM !"
        elif c.neighbor_mines == 0:
            for n in self.get_neighbors(x,y): self.reveal_cell(n.x, n.y)

    def ai_step(self):
        if self.game_over or self.first_click: return
        res = self.ai.get_next_move(self.grid, ROWS, COLS)
        if res:
            x, y, action, msg = res
            if self.ai_active and "RISQUÉ" in msg:
                self.ai_active = False
                self.last_msg = f"STOP : {msg}"
                return 

            self.last_msg = f"IA: {msg}"
            if action == 'reveal': self.reveal_cell(x, y)
            else: self.grid[x][y].is_flagged = True
            self.check_win()
            self.update_analysis()

    def check_win(self):
        rev = sum(1 for r in self.grid for c in r if c.is_revealed)
        if rev == (ROWS * COLS) - MINES_COUNT: 
            self.won = self.game_over = True
            self.last_msg = "GAGNÉ !"

    def draw(self):
        self.screen.fill(GRAY_COV)
        for r in self.grid:
            for c in r: c.draw(self.screen, self.font, self.p_font)
        
        # Zone d'information HUD
        pygame.draw.rect(self.screen, BLACK, (0, ROWS*TILE_SIZE, WIDTH, INFO_HEIGHT))
        
        # Message principal
        col = GREEN if self.ai_active else WHITE
        if "STOP" in self.last_msg: col = YELLOW
        t = self.font.render(self.last_msg, True, col)
        self.screen.blit(t, (10, ROWS*TILE_SIZE + 10))
        
        # Compteur de mines restantes
        flags_count = sum(1 for r in self.grid for c in r if c.is_flagged)
        mines_left = max(0, MINES_COUNT - flags_count)
        t_mines = self.font.render(f"F: {mines_left}", True, RED)
        self.screen.blit(t_mines, (WIDTH - 100, ROWS*TILE_SIZE + 10))
        
        # Légende des contrôles
        hud_color = GRAY_REV
        ctrl1 = "Clic G: Révéler | Clic D: Drapeau | R: Reset"
        ctrl2 = f"A: IA Auto ({'ON' if self.ai_active else 'OFF'}) | Espace: Prochain coup"
        self.screen.blit(self.p_font.render(ctrl1, True, hud_color), (10, ROWS*TILE_SIZE + 50))
        self.screen.blit(self.p_font.render(ctrl2, True, hud_color), (10, ROWS*TILE_SIZE + 75))
        
        pygame.display.flip()

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN: self.handle_click(e.pos, e.button)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_a: self.ai_active = not self.ai_active
                    if e.key == pygame.K_SPACE: self.ai_step()
                    if e.key == pygame.K_r: self.start_new_game()
            if self.ai_active and not self.game_over: 
                self.ai_step()
                pygame.time.delay(150)
            self.draw()

if __name__ == "__main__":
    game = MinesweeperGame(); game.run()