import tkinter as tk
import customtkinter as ctk
import random

# --- Configurações Modernas ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FlappyCyber(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("RAIVA2.0 - CYBER EDITION")
        self.geometry("1150x750")
        self.resizable(False, False)

        # Configurações de Dificuldade (Velocidade, Gap, Gravidade, Cor)
        self.DIFF_SETTINGS = {
            "Fácil": {"speed": 4, "gap": 130, "grav": 0.40, "color": "#00FF9C"},
            "Normal": {"speed": 6, "gap": 110, "grav": 0.48, "color": "#00D4FF"},
            "Médio": {"speed": 8, "gap": 95, "grav": 0.55, "color": "#FFCC00"},
            "Difícil": {"speed": 10, "gap": 85, "grav": 0.62, "color": "#FF8800"},
            "Extremo": {"speed": 13, "gap": 75, "grav": 0.75, "color": "#FF0055"}
        }

        # Variáveis de Estado
        self.running = False
        self.game_over = False
        self.score = 0
        self.best_score = 0
        self.selected_diff = tk.StringVar(value="Normal")
        
        # Física e Objetos
        self.bird_y = 300
        self.bird_vy = 0
        self.pipes = []
        
        # --- Layout Grid ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (HUD) ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#0a0a0a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="RAIVA 2.0", font=("Orbitron", 32, "bold"), text_color="#00D4FF").pack(pady=30)
        
        # Painel de Pontuação
        self.score_card = ctk.CTkFrame(self.sidebar, fg_color="#161616", corner_radius=15)
        self.score_card.pack(pady=10, padx=20, fill="x")
        self.score_label = ctk.CTkLabel(self.score_card, text="0", font=("Consolas", 45, "bold"), text_color="white")
        self.score_label.pack(pady=5)
        
        self.best_label = ctk.CTkLabel(self.sidebar, text="BEST: 0", font=("Consolas", 16), text_color="#00FF9C")
        self.best_label.pack(pady=10)

        # --- Menu de Dificuldade ---
        ctk.CTkLabel(self.sidebar, text="SELECT DIFFICULTY", font=("Roboto", 12, "bold"), text_color="gray").pack(pady=(20, 10))
        
        for diff in self.DIFF_SETTINGS.keys():
            rb = ctk.CTkRadioButton(self.sidebar, text=diff, variable=self.selected_diff, value=diff,
                                    fg_color=self.DIFF_SETTINGS[diff]["color"], 
                                    hover_color=self.DIFF_SETTINGS[diff]["color"])
            rb.pack(pady=5, padx=30, anchor="w")

        self.btn_play = ctk.CTkButton(self.sidebar, text="START ENGINE", font=("Roboto", 16, "bold"), 
                                      fg_color="#00D4FF", text_color="black", height=45, command=self.start_game)
        self.btn_play.pack(pady=30, padx=20, fill="x")

        # --- Game View ---
        self.view = ctk.CTkFrame(self, fg_color="#050505")
        self.view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.canvas = tk.Canvas(self.view, width=800, height=600, bg="#050505", highlightthickness=0)
        self.canvas.pack(expand=True)

        # Binds
        self.bind("<space>", lambda e: self.on_action())
        self.bind("<r>", lambda e: self.reset())
        
        self.draw_menu()

    def draw_menu(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 250, text="SYSTEM READY", font=("Orbitron", 40, "bold"), fill="white")
        self.canvas.create_text(400, 310, text="CHOOSE DIFFICULTY AND PRESS [SPACE]", font=("Consolas", 14), fill="#00D4FF")

    def start_game(self):
        if not self.running:
            self.reset()
            self.running = True
            self.btn_play.configure(state="disabled", text="IN FLIGHT")
            # Bloquear seleção de dificuldade durante o jogo
            self.game_loop()

    def on_action(self):
        if self.game_over:
            self.reset()
            self.start_game()
        elif not self.running:
            self.start_game()
        
        settings = self.DIFF_SETTINGS[self.selected_diff.get()]
        self.bird_vy = -8.5 # Força do pulo constante ou pode escalar se quiser

    def reset(self):
        self.running = False
        self.game_over = False
        self.score = 0
        self.bird_y = 300
        self.bird_vy = 0
        self.pipes = []
        self.spawn_pipe()
        self.score_label.configure(text="0")
        self.btn_play.configure(state="normal", text="START ENGINE")

    def spawn_pipe(self):
        gap_center = random.randint(150, 450)
        self.pipes.append({'x': 850, 'gap_y': gap_center})

    def game_loop(self):
        if not self.running or self.game_over:
            return

        # Carregar configurações da dificuldade selecionada
        config = self.DIFF_SETTINGS[self.selected_diff.get()]

        # Física Aplicada
        self.bird_vy += config["grav"]
        self.bird_y += self.bird_vy

        # Movimentação dos Canos
        for p in self.pipes:
            p['x'] -= config["speed"]
        
        if self.pipes[-1]['x'] < 500:
            self.spawn_pipe()
        
        if self.pipes[0]['x'] < -100:
            self.pipes.pop(0)
            self.score += 1
            self.score_label.configure(text=str(self.score))
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_label.configure(text=f"BEST: {self.best_score}")

        # Colisões Dinâmicas (usa o gap da configuração)
        if self.bird_y > 600 or self.bird_y < 0 or self.check_collision(config["gap"]):
            self.end_game()
            return

        self.render(config)
        self.after(16, self.game_loop)

    def check_collision(self, gap_size):
        bx1, by1, bx2, by2 = 145, self.bird_y - 15, 175, self.bird_y + 15
        for p in self.pipes:
            if p['x'] < bx2 and p['x'] + 80 > bx1:
                # O pássaro morre se estiver acima ou abaixo do vão livre
                if by1 < p['gap_y'] - gap_size or by2 > p['gap_y'] + gap_size:
                    return True
        return False

    def render(self, config):
        self.canvas.delete("all")
        
        # Cor Neon baseada na dificuldade
        diff_color = config["color"]
        
        # Desenhar Canos
        for p in self.pipes:
            # Superior
            self.canvas.create_rectangle(p['x'], 0, p['x']+80, p['gap_y'] - config["gap"], 
                                         fill="#111", outline=diff_color, width=2)
            # Inferior
            self.canvas.create_rectangle(p['x'], p['gap_y'] + config["gap"], p['x']+80, 600, 
                                         fill="#111", outline=diff_color, width=2)

        # Desenhar Pássaro Hacker
        self.draw_hacker_bird(160, self.bird_y, diff_color)

    def draw_hacker_bird(self, x, y, color):
        # Glow Effect
        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="", stipple="gray50")
        # Corpo
        self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="white", outline=color, width=3)
        # Olho
        self.canvas.create_oval(x+5, y-8, x+12, y-2, fill="black")

    def end_game(self):
        self.running = False
        self.game_over = True
        self.btn_play.configure(state="normal", text="REBOOT SYSTEM")
        self.canvas.create_rectangle(0, 0, 800, 600, fill="#000000", stipple="gray50")
        self.canvas.create_text(400, 300, text="SYSTEM CRASHED", font=("Orbitron", 40, "bold"), fill="#FF0055")
        self.canvas.create_text(400, 360, text="PRESS [R] TO RECOVER", font=("Consolas", 16), fill="white")

if __name__ == "__main__":
    app = FlappyCyber()
    app.mainloop()