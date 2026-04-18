🚀 FlappyCyber — RAIVA 2.0 (Cyber Edition)
O FlappyCyber é um jogo de arcade inspirado no clássico Flappy Bird, mas com uma estética futurista "Cyberpunk". Desenvolvido em Python, o projeto foca-se na experiência do utilizador e na personalização da jogabilidade através de diferentes níveis de dificuldade.

🛠️ Tecnologias e Bibliotecas
Python 3.x

CustomTkinter: Utilizada para criar uma interface moderna com suporte nativo a Dark Mode.

Tkinter: Utilizado para a renderização do motor de jogo no Canvas.

Random: Para a geração dinâmica e imprevisível dos obstáculos.

🌟 Destaques do Projeto
Dificuldade Escalonável: O jogo oferece 5 modos (Fácil, Normal, Médio, Difícil e Extremo). Cada modo ajusta dinamicamente a gravidade, a velocidade dos canos e o espaço entre eles.

HUD Integrado: Uma barra lateral (Sidebar) profissional que exibe a pontuação atual, o recorde máximo (Best Score) e o seletor de dificuldades.

Estética Neon: O personagem e os obstáculos mudam de cor com base na dificuldade selecionada, criando uma experiência visual vibrante.

Motor de Física: Implementação de lógica de gravidade, aceleração de queda e deteção de colisões em tempo real.

🎮 Como Jogar
Instalação:
Certifica-te de ter o Python e a biblioteca customtkinter instalados:

Bash
pip install customtkinter
Execução:
Corre o script principal:

Bash
python flappy_cyber.py
Controlos:

ESPAÇO: Iniciar motor / Saltar.

R: Reiniciar o sistema após um Crash (Game Over).

🧠 Arquitetura de Código
O código foi estruturado de forma orientada a objetos (POO), onde a classe FlappyCyber gere:

Estado do Jogo: Controlo de estados (Running, Game Over).

Loop Principal: Processamento de física e renderização a ~60 FPS.

Deteção de Colisão: Cálculo preciso das coordenadas do "Pássaro Hacker" em relação aos obstáculos.
