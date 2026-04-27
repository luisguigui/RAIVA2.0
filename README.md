# RAIVA 2.0 - CYBER EDITION 🎮

![Versão](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Status](https://img.shields.io/badge/status-Ativo-success.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

Um jogo dinâmico de **"Flappy Bird"** com temática cyberpunk, desenvolvido em Python com interface moderna usando **CustomTkinter**. O jogo oferece 5 níveis de dificuldade ajustáveis com física realista e gameplay desafiador.

## 📋 Sumário

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Como Jogar](#-como-jogar)
- [Arquitetura do Código](#-arquitetura-do-código)
- [Configuração de Dificuldades](#-configuração-de-dificuldades)
- [API e Métodos](#-api-e-métodos)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Características

### 🎨 Interface Moderna
- **Tema Cyberpunk**: Dark mode com cores neon vibrantes
- **Sidebar intuitiva**: Controle de dificuldade e visualização de pontuação em tempo real
- **HUD dinâmico**: Best score, score atual e status do jogo
- **Animações fluidas**: 60 FPS de renderização (16ms por frame)

### 🎯 Gameplay Dinâmico
- **5 níveis de dificuldade**: Fácil, Normal, Médio, Difícil e Extremo
- **Física realista**: Gravidade, velocidade de queda e aceleração simuladas
- **Colisão precisa**: Sistema de hitbox dinâmico baseado no gap dos canos
- **Geração procedural**: Canos gerados aleatoriamente com altura variável

### 🎮 Controles Responsivos
- **[ESPAÇO]**: Fazer o pássaro pular / Iniciar jogo / Reiniciar após falha
- **[R]**: Recuperar sistema (reiniciar jogo)
- **Mouse**: Selecionar dificuldade e iniciar jogo

### 📊 Sistema de Pontuação
- Score contabilizado ao passar por cada cano
- Melhor pontuação armazenada durante a sessão
- Feedback visual com atualização em tempo real

---

## 🔧 Requisitos

### Dependências
```bash
- Python 3.8+
- tkinter (geralmente incluído com Python)
- customtkinter >= 5.0
```

### Sistema Operacional
✅ Windows  
✅ macOS  
✅ Linux

---

## 📦 Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/lgguigui/RAIVA2.0.git
cd RAIVA2.0
```

### 2. Criar ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install customtkinter
```

### 4. Executar o jogo
```bash
python RAIVA2.py
```

---

## 🎮 Como Jogar

### Fluxo do Jogo

1. **Menu Inicial**
   - Selecione uma dificuldade usando os radio buttons
   - Clique em **"START ENGINE"** ou pressione **[ESPAÇO]**

2. **Durante o Jogo**
   - Pressione **[ESPAÇO]** para fazer o pássaro pular
   - Evite os canos superior e inferior
   - Cada cano que passar vale **+1 ponto**

3. **Game Over**
   - O jogo termina ao colidir com canos ou sair da tela
   - Pressione **[ESPAÇO]** ou clique em **"REBOOT SYSTEM"** para reiniciar
   - Pressione **[R]** para recuperar o sistema

### Dificuldades

| Nível | Velocidade | Gap | Gravidade | Cor |
|-------|-----------|-----|-----------|-----|
| **Fácil** | 4 px/frame | 130 px | 0.40 | 🟢 Verde |
| **Normal** | 6 px/frame | 110 px | 0.48 | 🔵 Azul |
| **Médio** | 8 px/frame | 95 px | 0.55 | 🟡 Amarelo |
| **Difícil** | 10 px/frame | 85 px | 0.62 | 🟠 Laranja |
| **Extremo** | 13 px/frame | 75 px | 0.75 | 🔴 Vermelho |

---

## 🏗️ Arquitetura do Código

### Estrutura de Diretórios
```
RAIVA2.0/
├── RAIVA2.py                 # Arquivo principal
├── README.md                 # Documentação
└── requirements.txt          # Dependências
```

### Hierarquia de Classes

```
FlappyCyber (ctk.CTk)
├── Inicialização
│   ├── Configurações de UI
│   ├── Setup de Dificuldades
│   └── Binds de Teclado
├── Gerenciamento de Estado
│   ├── running
│   ├── game_over
│   ├── score
│   └── physics
├── Lógica de Gameplay
│   ├── game_loop()
│   ├── spawn_pipe()
│   └── check_collision()
└── Renderização
    ├── render()
    └── draw_hacker_bird()
```

---

## 📖 Arquitetura do Código

### 1. **Inicialização e Configuração**

#### `__init__(self)`
Configuração inicial da aplicação:
- **Tema**: Dark mode com cores azul/ciano
- **Resolução**: 1150x750 px (sem resize)
- **Grid Layout**: Sidebar (280px) + Canvas (870px)
- **Dificuldades**: Dicionário com 5 níveis pré-configurados

```python
self.DIFF_SETTINGS = {
    "Fácil": {"speed": 4, "gap": 130, "grav": 0.40, "color": "#00FF9C"},
    # ...
}
```

**Parâmetros de Dificuldade:**
- `speed`: Pixels por frame que os canos se movem
- `gap`: Espaço livre entre cano superior e inferior
- `grav`: Aceleração gravitacional aplicada ao pássaro
- `color`: Cor neon para visual da dificuldade

### 2. **Sistema de Física**

#### Gravidade e Velocidade Vertical
```python
self.bird_vy += config["grav"]  # Aplicar gravidade
self.bird_y += self.bird_vy      # Atualizar posição
```

**Mecânica de Pulo:**
- Quando o jogador pressiona [ESPAÇO], `bird_vy = -8.5` (velocidade negativa = sobe)
- A gravidade aumenta a velocidade a cada frame (cai cada vez mais rápido)
- Resultado: Movimento natural e realista

### 3. **Gerenciamento de Canos**

#### `spawn_pipe()`
Cria um novo cano com posição aleatória:
```python
gap_center = random.randint(150, 450)  # Centro do gap varia
self.pipes.append({'x': 850, 'gap_y': gap_center})
```

- **x**: Posição horizontal (sempre começa no bordo direito)
- **gap_y**: Altura do centro do vão livre

#### Lógica no `game_loop()`
```python
for p in self.pipes:
    p['x'] -= config["speed"]           # Move para esquerda
if self.pipes[-1]['x'] < 500:
    self.spawn_pipe()                   # Novo cano se necessário
if self.pipes[0]['x'] < -100:
    self.pipes.pop(0)                   # Remove cano fora de tela
    self.score += 1                     # +1 ponto ao passar
```

### 4. **Sistema de Colisão**

#### `check_collision(gap_size)`
Detecta colisão entre pássaro e canos usando hitbox:

```python
# Hitbox do pássaro (retângulo)
bx1, by1, bx2, by2 = 145, self.bird_y - 15, 175, self.bird_y + 15

for p in self.pipes:
    # Verifica se está na faixa horizontal do cano
    if p['x'] < bx2 and p['x'] + 80 > bx1:
        # Verifica se está acima ou abaixo do gap
        if by1 < p['gap_y'] - gap_size or by2 > p['gap_y'] + gap_size:
            return True
```

**Lógica:**
1. Define bounding box do pássaro (30px de altura × 30px de largura)
2. Para cada cano, verifica se horizontalmente se sobrepõem
3. Se sim, verifica se o pássaro está fora do gap livre
4. Qualquer colisão = Game Over

### 5. **Loop de Jogo**

#### `game_loop()`
Executado a cada 16ms (~60 FPS):

```python
def game_loop(self):
    if not self.running or self.game_over:
        return
    
    config = self.DIFF_SETTINGS[self.selected_diff.get()]
    
    # 1. Atualizar Física
    self.bird_vy += config["grav"]
    self.bird_y += self.bird_vy
    
    # 2. Movimentar Canos
    for p in self.pipes:
        p['x'] -= config["speed"]
    
    # 3. Gerenciar Canos (spawn, remove, score)
    # ...
    
    # 4. Checar Colisão
    if self.bird_y > 600 or self.bird_y < 0 or self.check_collision(config["gap"]):
        self.end_game()
        return
    
    # 5. Renderizar
    self.render(config)
    
    # 6. Agendar próximo frame
    self.after(16, self.game_loop)
```

### 6. **Renderização**

#### `render(config)`
Limpa canvas e desenha todos os objetos:

```python
self.canvas.delete("all")

# Desenhar Canos com cor dinâmica
for p in self.pipes:
    self.canvas.create_rectangle(
        p['x'], 0, 
        p['x']+80, p['gap_y'] - config["gap"], 
        fill="#111", outline=config["color"], width=2
    )
```

#### `draw_hacker_bird(x, y, color)`
Desenha o pássaro com efeito neon:
1. Glow effect (oval com stipple)
2. Corpo branco com outline colorido
3. Olho preto para expressão

### 7. **Gerenciamento de Estado**

#### `start_game()`
- Reseta variáveis
- Ativa flag `running = True`
- Desabilita seleção de dificuldade
- Inicia `game_loop()`

#### `reset()`
- Limpa estado para novo jogo
- Reseta score, posição, velocidade
- Spawn do primeiro cano

#### `end_game()`
- Para loop de jogo
- Exibe "SYSTEM CRASHED"
- Mostra instruções para recuperar

---

## ⚙️ Configuração de Dificuldades

### Entendendo os Parâmetros

**`speed`**: Controla a velocidade horizontal dos canos
- Valores maiores = canos se movem mais rápido
- Aumenta a dificuldade significativamente

**`gap`**: Espaço livre entre canos (em pixels)
- Valores menores = espaço mais apertado
- Requer precisão maior do jogador

**`grav`**: Aceleração gravitacional
- Valores maiores = pássaro cai mais rápido
- Afeta o controle e timing do pulo

**`color`**: Feedback visual da dificuldade
- Cada nível tem cor única para identificação rápida

### Customização

Para adicionar nova dificuldade, edite `DIFF_SETTINGS`:

```python
self.DIFF_SETTINGS = {
    "Personalizado": {"speed": 12, "gap": 80, "grav": 0.70, "color": "#FF00FF"}
}
```

---

## 📚 API e Métodos

### Métodos Públicos

| Método | Descrição | Exemplo |
|--------|-----------|---------|
| `start_game()` | Inicia nova partida | Botão START ENGINE |
| `reset()` | Reseta estado do jogo | Chamado ao iniciar |
| `on_action()` | Pulo do pássaro | [ESPAÇO] |
| `end_game()` | Finaliza partida | Colisão detectada |

### Variáveis de Estado

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `running` | bool | Jogo em progresso? |
| `game_over` | bool | Partida finalizada? |
| `score` | int | Pontos atuais |
| `best_score` | int | Melhor pontuação da sessão |
| `bird_y` | float | Posição Y do pássaro |
| `bird_vy` | float | Velocidade vertical do pássaro |
| `pipes` | list | Lista de canos ativos |

### Estrutura de Cano

```python
pipe = {
    'x': 850,           # Posição horizontal
    'gap_y': 300        # Centro do vão livre
}
```

---

## 🐛 Troubleshooting

### CustomTkinter não encontrado
```bash
pip install --upgrade customtkinter
```

### Jogo muito lento
- Verifique processamento de fundo
- Reduza outras aplicações
- CustomTkinter pode ter overhead em sistemas lentos

### Pulo não funciona
- Certifique-se que a janela está em foco
- [ESPAÇO] só funciona durante o jogo

### Score não persiste entre sessões
- O jogo salva apenas durante a sessão
- Para persistência de dados, implemente `.json` ou database

---

## 🚀 Possíveis Melhorias Futuras

- [ ] Persistência de high score em arquivo/banco de dados
- [ ] Sons e efeitos sonoros
- [ ] Animações de partículas ao colidir
- [ ] Power-ups (escudo, slow motion)
- [ ] Leaderboard online
- [ ] Múltiplos temas de skin
- [ ] Modo multiplayer local
- [ ] Replay system

---

## 📄 Licença

MIT License - Sinta-se livre para usar, modificar e distribuir este projeto!

---
