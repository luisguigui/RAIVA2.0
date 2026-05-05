"""
RAIVA 2.0 - CYBER EDITION
Desenvolvido por: LUIS GUILHERME G.B. E OTAVIO CESAR
"""

import tkinter as tk
import customtkinter as ctk
import random
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SAVE_FILE = "raiva_score.json"

# ============================================================
#  JOGO PRINCIPAL
# ============================================================

class FlappyCyber(ctk.CTk):

    # --------------------------------------------------------
    #  CONFIGURAÇÕES DE DIFICULDADE
    # --------------------------------------------------------

    DIFF_SETTINGS = {
        "Fácil":   {"speed": 4,  "gap": 130, "grav": 0.40, "color": "#00FF9C",
                    "desc": "Velocidade suave e vãos largos. Ideal para iniciantes."},
        "Normal":  {"speed": 6,  "gap": 110, "grav": 0.48, "color": "#00D4FF",
                    "desc": "O equilíbrio perfeito entre desafio e diversão."},
        "Médio":   {"speed": 8,  "gap": 95,  "grav": 0.55, "color": "#FFCC00",
                    "desc": "Os reflexos começam a ser testados com mais frequência."},
        "Difícil": {"speed": 10, "gap": 85,  "grav": 0.62, "color": "#FF8800",
                    "desc": "Para os veteranos. Cada vão é uma armadilha."},
        "Extremo": {"speed": 13, "gap": 75,  "grav": 0.75, "color": "#FF0055",
                    "desc": "Prepare-se para morrer. Muito. E chorar um pouco."},
    }

    # --------------------------------------------------------
    #  INICIALIZAÇÃO
    # --------------------------------------------------------

    def __init__(self):
        super().__init__()
        self.title("RAIVA 2.0 - CYBER EDITION")
        self.geometry("1150x750")
        self.resizable(False, False)

        # Estado: "menu" | "playing" | "paused" | "over"
        # Alterado para game_state para evitar conflito com o método interno do CTk
        self.game_state   = "menu"
        self.score        = 0
        self.best_score   = self._load_highscore()
        self.selected_diff = tk.StringVar(value="Normal")

        # Física
        self.bird_y  = 300
        self.bird_vy = 0
        self.pipes: list[dict] = []

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_canvas_area()
        self._bind_keys()
        self._draw_menu()

    # --------------------------------------------------------
    #  PERSISTÊNCIA
    # --------------------------------------------------------

    def _load_highscore(self) -> int:
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    return json.load(f).get("hs", 0)
            except Exception:
                return 0
        return 0

    def _save_highscore(self):
        with open(SAVE_FILE, "w") as f:
            json.dump({"hs": self.best_score}, f)

    # --------------------------------------------------------
    #  SIDEBAR
    # --------------------------------------------------------

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#0a0a0a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="RAIVA 2.0",
                     font=("Orbitron", 30, "bold"),
                     text_color="#00D4FF").pack(pady=(28, 4))
        ctk.CTkLabel(self.sidebar, text="CYBER EDITION",
                     font=("Consolas", 11),
                     text_color="#333333").pack(pady=(0, 16))

        # Painel de pontuação
        score_card = ctk.CTkFrame(self.sidebar, fg_color="#111111", corner_radius=12)
        score_card.pack(pady=(0, 10), padx=20, fill="x")

        ctk.CTkLabel(score_card, text="SCORE",
                     font=("Consolas", 11), text_color="#555555").pack(pady=(10, 0))
        self.score_label = ctk.CTkLabel(score_card, text="0",
                                        font=("Consolas", 42, "bold"),
                                        text_color="white")
        self.score_label.pack()

        ctk.CTkLabel(score_card, text="BEST",
                     font=("Consolas", 11), text_color="#555555").pack()
        self.best_label = ctk.CTkLabel(score_card,
                                       text=str(self.best_score),
                                       font=("Consolas", 20, "bold"),
                                       text_color="#00FF9C")
        self.best_label.pack(pady=(0, 10))

        # Dificuldade
        ctk.CTkLabel(self.sidebar, text="── DIFICULDADE ──",
                     font=("Consolas", 10), text_color="#444444").pack(pady=(8, 4))

        for diff, cfg in self.DIFF_SETTINGS.items():
            rb = ctk.CTkRadioButton(
                self.sidebar, text=diff,
                variable=self.selected_diff, value=diff,
                fg_color=cfg["color"], hover_color=cfg["color"],
                command=self._on_diff_change,
            )
            rb.pack(pady=4, padx=30, anchor="w")

        # Descrição da dificuldade
        self.desc_lbl = ctk.CTkLabel(
            self.sidebar,
            text=self.DIFF_SETTINGS["Normal"]["desc"],
            font=("Consolas", 10),
            text_color="#555555",
            wraplength=220, justify="center",
        )
        self.desc_lbl.pack(pady=(6, 0), padx=20)

        # Botão principal
        self.btn_play = ctk.CTkButton(
            self.sidebar, text="▶  START ENGINE",
            font=("Roboto", 15, "bold"),
            fg_color="#00D4FF", text_color="black",
            hover_color="#00a8c8",
            height=48, command=self._btn_action,
        )
        self.btn_play.pack(side="bottom", pady=(0, 16), padx=20, fill="x")

        ctk.CTkLabel(self.sidebar,
                     text="ESPAÇO = Pular   P = Pause   R = Restart",
                     font=("Consolas", 9), text_color="#333333",
                     wraplength=240).pack(side="bottom", pady=(0, 4))

    def _on_diff_change(self):
        diff = self.selected_diff.get()
        self.desc_lbl.configure(text=self.DIFF_SETTINGS[diff]["desc"])
        if self.game_state == "menu":
            self._draw_menu()

    # --------------------------------------------------------
    #  CANVAS
    # --------------------------------------------------------

    def _build_canvas_area(self):
        self.view = ctk.CTkFrame(self, fg_color="#050505")
        self.view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.canvas = tk.Canvas(self.view, width=800, height=600,
                                bg="#050505", highlightthickness=0)
        self.canvas.pack(expand=True)

    def _bind_keys(self):
        self.bind("<space>", self._on_space)
        self.bind("<p>",     self._on_pause)
        self.bind("<r>",     self._on_restart)

    # --------------------------------------------------------
    #  TELAS DE ESTADO
    # --------------------------------------------------------

    def _draw_menu(self):
        diff   = self.selected_diff.get()
        color  = self.DIFF_SETTINGS[diff]["color"]
        self.canvas.delete("all")
        self.canvas.configure(bg="#050505")

        cx = 400

        # Grade de fundo
        for x in range(0, 800, 40):
            self.canvas.create_line(x, 0, x, 600, fill="#0d0d0d")
        for y in range(0, 600, 40):
            self.canvas.create_line(0, y, 800, y, fill="#0d0d0d")

        # Título
        self.canvas.create_text(cx, 95,
                                text="RAIVA 2.0",
                                font=("Orbitron", 52, "bold"),
                                fill=color)
        self.canvas.create_text(cx, 145,
                                text="CYBER  EDITION",
                                font=("Consolas", 17),
                                fill="#ffffff")
        self.canvas.create_line(cx - 240, 168, cx + 240, 168,
                                fill=color, width=2)

        # Recorde
        self.canvas.create_text(cx, 192,
                                text=f"★  RECORDE: {self.best_score}  ★",
                                font=("Consolas", 15, "bold"),
                                fill="#ffff00")

        # Dificuldade ativa
        self.canvas.create_text(cx, 222,
                                text=f"DIFICULDADE → {diff}",
                                font=("Consolas", 12), fill=color)

        # Painel de controles
        self.canvas.create_rectangle(cx - 220, 248, cx + 220, 420,
                                     outline="#1a1a1a", fill="#0a0a0a")
        self.canvas.create_text(cx, 268,
                                text="CONTROLES",
                                font=("Consolas", 13, "bold"), fill=color)
        self.canvas.create_line(cx - 170, 283, cx + 170, 283,
                                fill="#1a1a1a")

        controls = [
            ("ESPAÇO",  "Pular / Iniciar"),
            ("P",       "Pausar o jogo"),
            ("R",       "Reiniciar"),
        ]
        y = 298
        for key, desc in controls:
            y += 34
            self.canvas.create_text(cx - 20, y, text=key,
                                    font=("Consolas", 13, "bold"),
                                    fill="white", anchor="e")
            self.canvas.create_text(cx, y, text="→",
                                    font=("Consolas", 12), fill=color)
            self.canvas.create_text(cx + 20, y, text=desc,
                                    font=("Consolas", 12), fill="#888888",
                                    anchor="w")

        # Botão start
        by = 500
        self.canvas.create_rectangle(cx - 200, by - 24, cx + 200, by + 24,
                                     outline=color, fill="#050505", width=2)
        self.canvas.create_text(cx, by,
                                text="▶  PRESSIONE ESPAÇO PARA INICIAR",
                                font=("Consolas", 13, "bold"), fill=color)

        # Pássaro decorativo
        self._draw_bird(cx, 455, color)

    def _draw_pause_overlay(self):
        diff  = self.selected_diff.get()
        color = self.DIFF_SETTINGS[diff]["color"]
        cx, cy = 400, 300

        self.canvas.create_rectangle(0, 0, 800, 600,
                                     fill="#000000", stipple="gray50",
                                     tags="overlay")
        self.canvas.create_rectangle(cx - 220, cy - 80, cx + 220, cy + 90,
                                     fill="#0a0a0a", outline=color,
                                     width=2, tags="overlay")
        self.canvas.create_text(cx, cy - 40,
                                text="⏸  PAUSADO",
                                font=("Orbitron", 30, "bold"),
                                fill=color, tags="overlay")
        self.canvas.create_line(cx - 180, cy - 5, cx + 180, cy - 5,
                                fill="#222222", tags="overlay")
        self.canvas.create_text(cx, cy + 28,
                                text="P  →  Retomar",
                                font=("Consolas", 15), fill="white",
                                tags="overlay")
        self.canvas.create_text(cx, cy + 60,
                                text="R  →  Reiniciar",
                                font=("Consolas", 14), fill="#777777",
                                tags="overlay")

    def _draw_game_full_screen(self):
        diff  = self.selected_diff.get()
        color = self.DIFF_SETTINGS[diff]["color"]
        cx, cy = 400, 300

        self.canvas.create_rectangle(0, 0, 800, 600,
                                     fill="#000000", stipple="gray50")
        self.canvas.create_rectangle(cx - 250, cy - 110, cx + 250, cy + 120,
                                     fill="#0d0000", outline="#FF0055", width=2)
        self.canvas.create_text(cx, cy - 72,
                                text="SYSTEM CRASHED",
                                font=("Orbitron", 32, "bold"),
                                fill="#FF0055")
        self.canvas.create_line(cx - 210, cy - 38, cx + 210, cy - 38,
                                fill="#440000")

        self.canvas.create_text(cx, cy - 8,
                                text=f"SCORE:  {self.score}",
                                font=("Consolas", 24, "bold"), fill="white")

        new_record = self.score > 0 and self.score == self.best_score
        if new_record:
            self.canvas.create_text(cx, cy + 30,
                                    text="★★  NOVO RECORDE!  ★★",
                                    font=("Consolas", 17, "bold"),
                                    fill="#ffff00")
        else:
            self.canvas.create_text(cx, cy + 30,
                                    text=f"RECORDE:  {self.best_score}",
                                    font=("Consolas", 16), fill="#888800")

        self.canvas.create_text(cx, cy + 82,
                                text="ESPAÇO → Reiniciar      R → Reiniciar",
                                font=("Consolas", 13), fill=color)

    # --------------------------------------------------------
    #  AÇÕES DOS CONTROLES
    # --------------------------------------------------------

    def _btn_action(self):
        if   self.game_state == "menu":    self._start_game()
        elif self.game_state == "playing": self._pause_game()
        elif self.game_state == "paused":  self._resume_game()
        elif self.game_state == "over":    self._restart()

    def _on_space(self, _=None):
        if self.game_state == "menu":
            self._start_game()
        elif self.game_state == "playing":
            self.bird_vy = -8.5
        elif self.game_state == "over":
            self._restart()
        elif self.game_state == "paused":
            self._resume_game()

    def _on_pause(self, _=None):
        if self.game_state == "playing":
            self._pause_game()
        elif self.game_state == "paused":
            self._resume_game()

    def _on_restart(self, _=None):
        if self.game_state in ("playing", "paused", "over"):
            self._restart()

    # --------------------------------------------------------
    #  ESTADO DO JOGO
    # --------------------------------------------------------

    def _start_game(self):
        self._reset_physics()
        self.game_state = "playing"
        self.btn_play.configure(text="⏸  PAUSE", fg_color="#333333",
                                text_color="white")
        self._game_loop()

    def _pause_game(self):
        self.game_state = "paused"
        self.btn_play.configure(text="▶  RETOMAR", fg_color="#00D4FF",
                                text_color="black")
        self._draw_pause_overlay()

    def _resume_game(self):
        self.game_state = "playing"
        self.btn_play.configure(text="⏸  PAUSE", fg_color="#333333",
                                text_color="white")
        self._game_loop()

    def _restart(self):
        self._reset_physics()
        self.game_state = "playing"
        self.btn_play.configure(text="⏸  PAUSE", fg_color="#333333",
                                text_color="white")
        self._game_loop()

    def _reset_physics(self):
        self.score   = 0
        self.bird_y  = 300
        self.bird_vy = 0
        self.pipes   = []
        self.score_label.configure(text="0")
        self._spawn_pipe()

    def _go_to_menu(self):
        self.game_state = "menu"
        self.btn_play.configure(text="▶  START ENGINE", fg_color="#00D4FF",
                                text_color="black")
        self._draw_menu()

    # --------------------------------------------------------
    #  SPAWN DE CANOS
    # --------------------------------------------------------

    def _spawn_pipe(self):
        gap_center = random.randint(150, 450)
        self.pipes.append({"x": 850, "gap_y": gap_center})

    # --------------------------------------------------------
    #  LOOP PRINCIPAL
    # --------------------------------------------------------

    def _game_loop(self):
        if self.game_state != "playing":
            return

        config = self.DIFF_SETTINGS[self.selected_diff.get()]

        # Física do pássaro
        self.bird_vy += config["grav"]
        self.bird_y  += self.bird_vy

        # Canos
        for p in self.pipes:
            p["x"] -= config["speed"]

        if self.pipes[-1]["x"] < 500:
            self._spawn_pipe()

        if self.pipes[0]["x"] < -100:
            self.pipes.pop(0)
            self.score += 1
            self.score_label.configure(text=str(self.score))
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_label.configure(text=str(self.best_score))
                self._save_highscore()

        # Colisão
        if (self.bird_y > 600 or self.bird_y < 0
                or self._check_collision(config["gap"])):
            self._end_game()
            return

        self._render_game(config)
        self.after(16, self._game_loop)

    # --------------------------------------------------------
    #  COLISÃO
    # --------------------------------------------------------

    def _check_collision(self, gap_size: int) -> bool:
        bx1, by1 = 145, self.bird_y - 15
        bx2, by2 = 175, self.bird_y + 15
        for p in self.pipes:
            if p["x"] < bx2 and p["x"] + 80 > bx1:
                if by1 < p["gap_y"] - gap_size or by2 > p["gap_y"] + gap_size:
                    return True
        return False

    # --------------------------------------------------------
    #  FIM DE JOGO
    # --------------------------------------------------------

    def _end_game(self):
        self.game_state = "over"
        self.btn_play.configure(text="⟳  REBOOT SYSTEM", fg_color="#FF0055",
                                text_color="white")
        self._draw_game_over_screen()

    # --------------------------------------------------------
    #  RENDERIZAÇÃO
    # --------------------------------------------------------

    def _render_game(self, config: dict):
        self.canvas.delete("all")
        self.canvas.configure(bg="#050505")

        diff_color = config["color"]

        # Grade de fundo sutil
        for x in range(0, 800, 40):
            self.canvas.create_line(x, 0, x, 600, fill="#0a0a0a")
        for y in range(0, 600, 40):
            self.canvas.create_line(0, y, 800, y, fill="#0a0a0a")

        # Canos
        for p in self.pipes:
            gap = config["gap"]
            # Superior
            self.canvas.create_rectangle(p["x"], 0, p["x"] + 80,
                                         p["gap_y"] - gap,
                                         fill="#111111", outline=diff_color, width=2)
            self.canvas.create_rectangle(p["x"] - 4, p["gap_y"] - gap - 14,
                                         p["x"] + 84, p["gap_y"] - gap,
                                         fill="#1a1a1a", outline=diff_color, width=1)
            # Inferior
            self.canvas.create_rectangle(p["x"], p["gap_y"] + gap,
                                         p["x"] + 80, 600,
                                         fill="#111111", outline=diff_color, width=2)
            self.canvas.create_rectangle(p["x"] - 4, p["gap_y"] + gap,
                                         p["x"] + 84, p["gap_y"] + gap + 14,
                                         fill="#1a1a1a", outline=diff_color, width=1)

        # Pássaro
        self._draw_bird(160, self.bird_y, diff_color)

        # Score HUD no canvas
        self.canvas.create_text(400, 20,
                                text=str(self.score),
                                font=("Consolas", 20, "bold"),
                                fill="white")

    def _draw_bird(self, x: float, y: float, color: str):
        # Glow
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                fill=color, outline="", stipple="gray50")
        # Corpo
        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15,
                                fill="white", outline=color, width=3)
        # Olho
        self.canvas.create_oval(x + 5, y - 8, x + 12, y - 2,
                                fill="black")
        # Bico
        self.canvas.create_polygon(x + 14, y, x + 22, y - 3, x + 22, y + 3,
                                   fill=color)


# ============================================================
#  ENTRADA
# ============================================================

if __name__ == "__main__":
    app = FlappyCyber()
    app.mainloop()
