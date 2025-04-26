import pygame
import sys
import random
import os
import json
import math
from enum import Enum

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Constantes do jogo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# Enums
class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3
    HIGH_SCORES = 4
    OPTIONS = 5

# Cores
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (50, 205, 50)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (100, 100, 100)
    DARK_GREEN = (0, 100, 0)
    LIGHT_GREEN = (144, 238, 144)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    CYAN = (0, 255, 255)
    
    BACKGROUND = (240, 248, 255)  # AliceBlue
    GRID_LIGHT = (220, 220, 220)
    GRID_DARK = (200, 200, 200)
    
    @staticmethod
    def get_random_color():
        return (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))

# Classe para carregar e gerenciar recursos
class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        
        # Caminhos para arquivos de recursos
        self.assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        
        # Criar diretório de assets se não existir
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)
            
        # Carregar fontes
        self.fonts["small"] = pygame.font.Font(None, 24)
        self.fonts["medium"] = pygame.font.Font(None, 36)
        self.fonts["large"] = pygame.font.Font(None, 72)
        
        # Tentar carregar sons
        try:
            self.sounds["eat"] = pygame.mixer.Sound(os.path.join(self.assets_dir, "eat.wav"))
            self.sounds["crash"] = pygame.mixer.Sound(os.path.join(self.assets_dir, "crash.wav"))
            self.sounds["powerup"] = pygame.mixer.Sound(os.path.join(self.assets_dir, "powerup.wav"))
        except:
            print("Alguns sons não puderam ser carregados. O jogo continuará sem áudio.")
    
    def get_font(self, size):
        return self.fonts.get(size, self.fonts["medium"])
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

# Classe para gerenciar as configurações do jogo
class GameSettings:
    def __init__(self):
        self.difficulty = 1  # 1-5, afeta a velocidade
        self.sound_enabled = True
        self.music_enabled = True
        self.grid_enabled = True
        self.enable_walls = True
        self.high_scores = []
        
        self.load_settings()
    
    def load_settings(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "settings.json"), "r") as f:
                data = json.load(f)
                self.difficulty = data.get("difficulty", 1)
                self.sound_enabled = data.get("sound_enabled", True)
                self.music_enabled = data.get("music_enabled", True)
                self.grid_enabled = data.get("grid_enabled", True)
                self.enable_walls = data.get("enable_walls", True)
                self.high_scores = data.get("high_scores", [])
        except:
            # Se o arquivo não existir ou estiver corrompido, use as configurações padrão
            pass
    
    def save_settings(self):
        data = {
            "difficulty": self.difficulty,
            "sound_enabled": self.sound_enabled,
            "music_enabled": self.music_enabled,
            "grid_enabled": self.grid_enabled,
            "enable_walls": self.enable_walls,
            "high_scores": self.high_scores
        }
        
        try:
            with open(os.path.join(os.path.dirname(__file__), "settings.json"), "w") as f:
                json.dump(data, f)
        except:
            print("Não foi possível salvar as configurações.")
    
    def add_score(self, name, score, level):
        self.high_scores.append({"name": name, "score": score, "level": level, "date": pygame.time.get_ticks()})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        if len(self.high_scores) > 10:  # Manter apenas os 10 melhores
            self.high_scores = self.high_scores[:10]
        self.save_settings()

# Classe para o menu principal
class MainMenu:
    def __init__(self, screen, assets, settings):
        self.screen = screen
        self.assets = assets
        self.settings = settings
        self.selected_option = 0
        self.options = ["Jogar", "Opções", "Recordes", "Sair"]
        self.background_color = Colors.BACKGROUND
        
    def draw(self):
        self.screen.fill(self.background_color)
        
        # Título do jogo
        title_font = self.assets.get_font("large")
        title = title_font.render("Snake Game", True, Colors.DARK_GREEN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Opções do menu
        for i, option in enumerate(self.options):
            font = self.assets.get_font("medium")
            if i == self.selected_option:
                color = Colors.GREEN
                text = f"> {option} <"
            else:
                color = Colors.BLACK
                text = option
                
            rendered_text = font.render(text, True, color)
            self.screen.blit(rendered_text, (SCREEN_WIDTH // 2 - rendered_text.get_width() // 2, 250 + i * 50))
        
        # Rodapé
        footer_font = self.assets.get_font("small")
        footer = footer_font.render("© 2025 Marco - Portfólio", True, Colors.GREY)
        self.screen.blit(footer, (SCREEN_WIDTH - footer.get_width() - 10, SCREEN_HEIGHT - footer.get_height() - 10))
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None

# Classe para a comida
class Food:
    def __init__(self, assets):
        self.assets = assets
        self.position = (0, 0)
        self.color = Colors.RED
        self.spawn()
        
    def spawn(self, snake_positions=None, barriers=None):
        if snake_positions is None:
            snake_positions = []
        if barriers is None:
            barriers = []
        
        # Garantir que a comida não apareça onde a cobra ou barreiras estão
        valid_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) 
                           if (x, y) not in snake_positions and (x, y) not in barriers]
        
        if valid_positions:
            self.position = random.choice(valid_positions)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Desenhar um brilho para tornar a comida mais atrativa
        inner_rect = (self.position[0] * GRID_SIZE + 4, self.position[1] * GRID_SIZE + 4, GRID_SIZE - 8, GRID_SIZE - 8)
        pygame.draw.rect(screen, Colors.YELLOW, inner_rect)

# Classe para power-ups
class PowerUp:
    def __init__(self, assets):
        self.assets = assets
        self.position = (0, 0)
        self.active = False
        self.type = random.choice(["speed", "slow", "points", "invincible", "shrink"])
        self.color = self.get_color_for_type()
        self.spawn_time = 0
        self.duration = 10000  # 10 segundos em milissegundos
        
    def get_color_for_type(self):
        if self.type == "speed":
            return Colors.YELLOW
        elif self.type == "slow":
            return Colors.BLUE
        elif self.type == "points":
            return Colors.PURPLE
        elif self.type == "invincible":
            return Colors.CYAN
        elif self.type == "shrink":
            return Colors.ORANGE
        return Colors.WHITE
        
    def spawn(self, snake_positions=None, barriers=None, food_position=None):
        if snake_positions is None:
            snake_positions = []
        if barriers is None:
            barriers = []
        
        # Garantir que o power-up não apareça onde a cobra, barreiras ou comida estão
        forbidden_positions = snake_positions + barriers
        if food_position:
            forbidden_positions.append(food_position)
            
        valid_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) 
                           if (x, y) not in forbidden_positions]
        
        if valid_positions:
            self.position = random.choice(valid_positions)
            self.active = True
            self.spawn_time = pygame.time.get_ticks()
            self.type = random.choice(["speed", "slow", "points", "invincible", "shrink"])
            self.color = self.get_color_for_type()
    
    def should_despawn(self):
        if not self.active:
            return False
        return pygame.time.get_ticks() - self.spawn_time > self.duration
    
    def draw(self, screen):
        if self.active:
            # Desenhar o Power-Up com um efeito pulsante
            time_alive = pygame.time.get_ticks() - self.spawn_time
            pulse = abs(math.sin(time_alive / 300)) * 0.5 + 0.5  # Efeito de pulsação
            
            size_mod = int(GRID_SIZE * (0.8 + 0.2 * pulse))
            offset = (GRID_SIZE - size_mod) // 2
            
            rect = (self.position[0] * GRID_SIZE + offset, 
                    self.position[1] * GRID_SIZE + offset, 
                    size_mod, size_mod)
            
            pygame.draw.rect(screen, self.color, rect)
            
            # Ícone para o tipo de power-up
            inner_rect = (self.position[0] * GRID_SIZE + GRID_SIZE // 4, 
                          self.position[1] * GRID_SIZE + GRID_SIZE // 4, 
                          GRID_SIZE // 2, GRID_SIZE // 2)
            
            pygame.draw.rect(screen, Colors.WHITE, inner_rect)
            
            # Tempo restante como barra de progresso circular
            time_left = 1.0 - (pygame.time.get_ticks() - self.spawn_time) / self.duration
            pygame.draw.arc(screen, self.color, 
                           (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                           0, time_left * 2 * math.pi, 2)

# Classe para a cobra
class Snake:
    def __init__(self, assets):
        self.assets = assets
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.grow_pending = 0
        self.color = Colors.GREEN
        self.head_color = Colors.DARK_GREEN
        self.is_invincible = False
        self.invincibility_end = 0
        self.speed_modifier = 1.0
        self.speed_mod_end = 0
        
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.grow_pending = 0
        self.is_invincible = False
        self.invincibility_end = 0
        self.speed_modifier = 1.0
        self.speed_mod_end = 0
    
    def set_direction(self, direction):
        # Previne a cobra de virar diretamente para trás
        if (self.direction == Direction.RIGHT and direction == Direction.LEFT) or \
           (self.direction == Direction.LEFT and direction == Direction.RIGHT) or \
           (self.direction == Direction.UP and direction == Direction.DOWN) or \
           (self.direction == Direction.DOWN and direction == Direction.UP):
            return
        self.next_direction = direction
    
    def move(self):
        # Atualizar a direção
        self.direction = self.next_direction
        
        # Calcular nova posição da cabeça
        head_x, head_y = self.positions[0]
        dx, dy = self.direction.value
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        
        # Mover a cobra
        self.positions.insert(0, new_head)
        
        # Verificar se deve crescer
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
    
    def grow(self, amount=1):
        self.grow_pending += amount
    
    def shrink(self, amount=1):
        # Impedir que a cobra fique menor que um segmento
        if len(self.positions) > amount:
            for _ in range(amount):
                self.positions.pop()
    
    def check_collision_with_self(self):
        # Se a cobra está invencível, não há colisão com ela mesma
        if self.is_invincible:
            return False
            
        # Verificar se a cabeça colide com qualquer parte do corpo
        return self.positions[0] in self.positions[1:]
    
    def check_collision_with_walls(self, enable_walls):
        # Se as paredes estão desativadas ou a cobra está invencível, não há colisão
        if not enable_walls or self.is_invincible:
            return False
            
        head_x, head_y = self.positions[0]
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT
    
    def check_collision_with_barriers(self, barriers):
        # Se a cobra está invencível, não há colisão com barreiras
        if self.is_invincible:
            return False
            
        return self.positions[0] in barriers
    
    def apply_power_up(self, power_up_type):
        current_time = pygame.time.get_ticks()
        
        if power_up_type == "speed":
            self.speed_modifier = 1.5
            self.speed_mod_end = current_time + 5000  # 5 segundos
        elif power_up_type == "slow":
            self.speed_modifier = 0.5
            self.speed_mod_end = current_time + 5000  # 5 segundos
        elif power_up_type == "invincible":
            self.is_invincible = True
            self.invincibility_end = current_time + 5000  # 5 segundos
        elif power_up_type == "shrink":
            self.shrink(max(1, len(self.positions) // 2))  # Reduz pela metade
    
    def update_effects(self):
        current_time = pygame.time.get_ticks()
        
        # Verificar invencibilidade
        if self.is_invincible and current_time > self.invincibility_end:
            self.is_invincible = False
            
        # Verificar modificador de velocidade
        if current_time > self.speed_mod_end:
            self.speed_modifier = 1.0
    
    def draw(self, screen):
        # Desenhar corpo da cobra
        for i, (x, y) in enumerate(self.positions):
            # A cabeça da cobra tem uma cor diferente
            color = self.head_color if i == 0 else self.color
            
            # Se invencível, aplicar efeito visual
            if self.is_invincible:
                # Efeito pulsante quando invencível
                pulse = abs(math.sin(pygame.time.get_ticks() / 100))
                color = (int(color[0] * (0.5 + 0.5 * pulse)), 
                         int(color[1] * (0.5 + 0.5 * pulse)), 
                         int(color[2] * (0.5 + 0.5 * pulse)))
            
            # Desenhar segmento com borda para dar efeito 3D
            rect = (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, Colors.BLACK, rect)
            pygame.draw.rect(screen, color, (x * GRID_SIZE + 1, y * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2))
            
            # Desenhar os olhos na cabeça da cobra
            if i == 0:
                # Definir posição dos olhos baseada na direção
                if self.direction == Direction.RIGHT:
                    eye_positions = [(x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + 5), 
                                    (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + GRID_SIZE - 5)]
                elif self.direction == Direction.LEFT:
                    eye_positions = [(x * GRID_SIZE + 5, y * GRID_SIZE + 5), 
                                    (x * GRID_SIZE + 5, y * GRID_SIZE + GRID_SIZE - 5)]
                elif self.direction == Direction.UP:
                    eye_positions = [(x * GRID_SIZE + 5, y * GRID_SIZE + 5), 
                                    (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + 5)]
                else:  # DOWN
                    eye_positions = [(x * GRID_SIZE + 5, y * GRID_SIZE + GRID_SIZE - 5), 
                                    (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + GRID_SIZE - 5)]
                
                # Desenhar os olhos
                for eye_pos in eye_positions:
                    pygame.draw.circle(screen, Colors.WHITE, eye_pos, 2)

# Classe principal do jogo
class SnakeGame:
    def __init__(self):
        # Configuração da janela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game - Portfolio")
        
        # Inicialização de recursos e configurações
        self.assets = AssetManager()
        self.settings = GameSettings()
        self.clock = pygame.time.Clock()
        
        # Estado do jogo
        self.state = GameState.MENU
        self.menu = MainMenu(self.screen, self.assets, self.settings)
        
        # Elementos do jogo
        self.snake = Snake(self.assets)
        self.food = Food(self.assets)
        self.power_up = PowerUp(self.assets)
        self.barriers = []
        
        # Variáveis do jogo
        self.score = 0
        self.level = 1
        self.move_timer = 0
        self.move_delay = self.get_move_delay()
        self.power_up_timer = 0
        self.power_up_delay = 15000  # 15 segundos em milissegundos
        
        # Variáveis para menus
        self.selected_option = 0  # Opção selecionada nos menus de opções
        
    def get_move_delay(self):
        # Quanto maior o nível, menor o delay (mais rápido)
        base_delay = 150  # ms
        difficulty_factor = self.settings.difficulty * 10
        level_factor = min(self.level * 5, 50)  # Limita o fator de nível a no máximo 50 ms
        
        delay = base_delay - difficulty_factor - level_factor
        delay = max(50, delay)  # Garante um delay mínimo de 50ms
        
        # Aplicar o modificador de velocidade da cobra
        if hasattr(self.snake, 'speed_modifier'):
            return delay / self.snake.speed_modifier
        return delay
    
    def reset_game(self):
        self.snake.reset()
        self.barriers = []
        self.food.spawn(self.snake.positions, self.barriers)
        self.power_up.active = False
        self.score = 0
        self.level = 1
        self.move_delay = self.get_move_delay()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if self.state == GameState.MENU:
                option = self.menu.handle_event(event)
                if option == "Jogar":
                    self.state = GameState.PLAYING
                    self.reset_game()
                elif option == "Opções":
                    self.state = GameState.OPTIONS
                    self.selected_option = 0  # Opção selecionada no menu de opções
                elif option == "Recordes":
                    self.state = GameState.HIGH_SCORES
                elif option == "Sair":
                    return False
            
            elif self.state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.set_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.set_direction(Direction.RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.PAUSED
            
            elif self.state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        self.state = GameState.MENU
            
            elif self.state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_r:
                        self.state = GameState.PLAYING
                        self.reset_game()
            
            elif self.state == GameState.HIGH_SCORES:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        
            elif self.state == GameState.OPTIONS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                        self.settings.save_settings()
                    elif event.key == pygame.K_UP:
                        if hasattr(self, 'selected_option'):
                            self.selected_option = (self.selected_option - 1) % 4
                        else:
                            self.selected_option = 0
                    elif event.key == pygame.K_DOWN:
                        if hasattr(self, 'selected_option'):
                            self.selected_option = (self.selected_option + 1) % 4
                        else:
                            self.selected_option = 0
                    elif event.key == pygame.K_LEFT:
                        if hasattr(self, 'selected_option'):
                            if self.selected_option == 0:  # Dificuldade
                                self.settings.difficulty = max(1, self.settings.difficulty - 1)
                    elif event.key == pygame.K_RIGHT:
                        if hasattr(self, 'selected_option'):
                            if self.selected_option == 0:  # Dificuldade
                                self.settings.difficulty = min(5, self.settings.difficulty + 1)
                    elif event.key == pygame.K_RETURN:
                        if hasattr(self, 'selected_option'):
                            if self.selected_option == 1:  # Som
                                self.settings.sound_enabled = not self.settings.sound_enabled
                            elif self.selected_option == 2:  # Grade
                                self.settings.grid_enabled = not self.settings.grid_enabled
                            elif self.selected_option == 3:  # Paredes
                                self.settings.enable_walls = not self.settings.enable_walls
        
        return True
    
    def update(self):
        if self.state == GameState.PLAYING:
            current_time = pygame.time.get_ticks()
            
            # Atualizar efeitos da cobra
            self.snake.update_effects()
            
            # Movimentar a cobra com base no timer
            if current_time - self.move_timer > self.move_delay:
                self.snake.move()
                self.move_timer = current_time
                self.move_delay = self.get_move_delay()
                
                # Verificar colisões
                if self.snake.check_collision_with_self() or \
                   self.snake.check_collision_with_walls(self.settings.enable_walls) or \
                   self.snake.check_collision_with_barriers(self.barriers):
                    if self.settings.sound_enabled:
                        self.assets.play_sound("crash")
                    self.state = GameState.GAME_OVER
                    self.settings.add_score("Jogador", self.score, self.level)
                
                # Verificar se a cobra comeu a comida
                if self.snake.positions[0] == self.food.position:
                    if self.settings.sound_enabled:
                        self.assets.play_sound("eat")
                    self.snake.grow()
                    self.score += 10 * self.level
                    
                    # Aumentar o nível a cada 5 comidas
                    if self.score % (5 * 10 * self.level) == 0:
                        self.level += 1
                        # Adicionar uma barreira a cada novo nível
                        new_barrier = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                        while new_barrier in self.snake.positions or new_barrier == self.food.position:
                            new_barrier = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                        self.barriers.append(new_barrier)
                        
                    self.food.spawn(self.snake.positions, self.barriers)
                
                # Verificar se a cobra pegou um power-up
                if self.power_up.active and self.snake.positions[0] == self.power_up.position:
                    if self.settings.sound_enabled:
                        self.assets.play_sound("powerup")
                    
                    if self.power_up.type == "points":
                        self.score += 50  # Bônus de pontos
                    else:
                        self.snake.apply_power_up(self.power_up.type)
                    
                    self.power_up.active = False
            
            # Gerenciar power-ups
            if self.power_up.active and self.power_up.should_despawn():
                self.power_up.active = False
            
            if not self.power_up.active and current_time - self.power_up_timer > self.power_up_delay:
                self.power_up.spawn(self.snake.positions, self.barriers, self.food.position)
                self.power_up_timer = current_time
    
    def draw(self):
        # Limpar a tela
        self.screen.fill(Colors.BACKGROUND)
        
        # Desenhar grade se ativado
        if self.settings.grid_enabled:
            for x in range(GRID_WIDTH):
                for y in range(GRID_HEIGHT):
                    if (x + y) % 2 == 0:
                        pygame.draw.rect(self.screen, Colors.GRID_LIGHT, 
                                        (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    else:
                        pygame.draw.rect(self.screen, Colors.GRID_DARK, 
                                        (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Desenhar elementos do jogo de acordo com o estado
        if self.state == GameState.MENU:
            self.menu.draw()
        
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Desenhar barreiras
            for barrier in self.barriers:
                pygame.draw.rect(self.screen, Colors.GREY, 
                               (barrier[0] * GRID_SIZE, barrier[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            
            # Desenhar comida e power-up
            self.food.draw(self.screen)
            if self.power_up.active:
                self.power_up.draw(self.screen)
            
            # Desenhar cobra
            self.snake.draw(self.screen)
            
            # Desenhar informações do jogo
            score_text = self.assets.get_font("medium").render(f"Pontos: {self.score}", True, Colors.BLACK)
            self.screen.blit(score_text, (10, 10))
            
            level_text = self.assets.get_font("medium").render(f"Nível: {self.level}", True, Colors.BLACK)
            self.screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
            
            # Mostrar efeitos ativos
            effects_text = []
            if self.snake.is_invincible:
                effects_text.append("Invencível")
            if self.snake.speed_modifier > 1.0:
                effects_text.append("Velocidade+")
            elif self.snake.speed_modifier < 1.0:
                effects_text.append("Velocidade-")
                
            if effects_text:
                effect_str = ", ".join(effects_text)
                effect_render = self.assets.get_font("small").render(f"Efeitos: {effect_str}", True, Colors.BLUE)
                self.screen.blit(effect_render, (10, 50))
            
            # Mensagem adicional se pausado
            if self.state == GameState.PAUSED:
                pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pause_surface.fill((0, 0, 0, 128))
                self.screen.blit(pause_surface, (0, 0))
                
                pause_text = self.assets.get_font("large").render("PAUSADO", True, Colors.WHITE)
                self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                                             SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))
                
                instruction = self.assets.get_font("small").render("Pressione ESC para continuar ou Q para sair", 
                                                                True, Colors.WHITE)
                self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 
                                             SCREEN_HEIGHT // 2 + 50))
        
        elif self.state == GameState.GAME_OVER:
            game_over_text = self.assets.get_font("large").render("FIM DE JOGO", True, Colors.RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
            
            score_text = self.assets.get_font("medium").render(f"Pontuação: {self.score}", True, Colors.BLACK)
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 270))
            
            level_text = self.assets.get_font("medium").render(f"Nível alcançado: {self.level}", True, Colors.BLACK)
            self.screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 310))
            
            instruction = self.assets.get_font("small").render("Pressione ENTER para voltar ao menu ou R para jogar novamente", 
                                                           True, Colors.BLACK)
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 370))
        
        elif self.state == GameState.HIGH_SCORES:
            self.draw_high_scores()
        
        elif self.state == GameState.OPTIONS:
            self.draw_options()
        
        # Atualizar a tela
        pygame.display.flip()
    
    def draw_high_scores(self):
        self.screen.fill(Colors.BACKGROUND)
        
        title = self.assets.get_font("large").render("Recordes", True, Colors.DARK_GREEN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        if not self.settings.high_scores:
            no_scores = self.assets.get_font("medium").render("Nenhum recorde ainda!", True, Colors.GREY)
            self.screen.blit(no_scores, (SCREEN_WIDTH // 2 - no_scores.get_width() // 2, 250))
        else:
            # Cabeçalho da tabela
            header_y = 120
            header_font = self.assets.get_font("medium")
            
            rank_text = header_font.render("Rank", True, Colors.BLACK)
            self.screen.blit(rank_text, (100, header_y))
            
            name_text = header_font.render("Nome", True, Colors.BLACK)
            self.screen.blit(name_text, (200, header_y))
            
            score_text = header_font.render("Pontos", True, Colors.BLACK)
            self.screen.blit(score_text, (400, header_y))
            
            level_text = header_font.render("Nível", True, Colors.BLACK)
            self.screen.blit(level_text, (550, header_y))
            
            # Linhas da tabela
            line_y = header_y + 40
            for i, score in enumerate(self.settings.high_scores[:10]):
                row_font = self.assets.get_font("small")
                
                rank = row_font.render(f"{i+1}.", True, Colors.BLACK)
                self.screen.blit(rank, (100, line_y))
                
                name = row_font.render(score["name"], True, Colors.BLACK)
                self.screen.blit(name, (200, line_y))
                
                points = row_font.render(str(score["score"]), True, Colors.BLACK)
                self.screen.blit(points, (400, line_y))
                
                level = row_font.render(str(score["level"]), True, Colors.BLACK)
                self.screen.blit(level, (550, line_y))
                
                line_y += 30
        
        instruction = self.assets.get_font("small").render("Pressione ESC para voltar", True, Colors.BLACK)
        self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def draw_options(self):
        self.screen.fill(Colors.BACKGROUND)
        
        title = self.assets.get_font("large").render("Opções", True, Colors.DARK_GREEN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        options_y = 150
        options_spacing = 60
        options_font = self.assets.get_font("medium")
        
        # Lista de opções para facilitar a navegação
        options = [
            {"name": "Dificuldade", "value": str(self.settings.difficulty), "y": options_y},
            {"name": "Som", "value": "Ativado" if self.settings.sound_enabled else "Desativado", "y": options_y + options_spacing},
            {"name": "Grade", "value": "Ativada" if self.settings.grid_enabled else "Desativada", "y": options_y + options_spacing * 2},
            {"name": "Paredes", "value": "Ativadas" if self.settings.enable_walls else "Desativadas", "y": options_y + options_spacing * 3}
        ]
        
        # Verificar se selected_option está definido
        if not hasattr(self, 'selected_option'):
            self.selected_option = 0
        
        # Desenhar cada opção
        for i, option in enumerate(options):
            # Determinar a cor baseado na seleção
            color = Colors.GREEN if i == self.selected_option else Colors.BLACK
            
            # Texto da opção
            text = f"{option['name']}: {option['value']}"
            if i == self.selected_option:
                # Adicionar indicadores para a opção selecionada
                if i == 0:  # Dificuldade - pode ser ajustada com setas esquerda/direita
                    text = f"< {option['name']}: {option['value']} >"
                else:  # Toggle options - pressione Enter para alternar
                    text = f"> {option['name']}: {option['value']} <"
            
            option_text = options_font.render(text, True, color)
            self.screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, option["y"]))
        
        # Instruções
        instruction_y = options_y + options_spacing * 5
        controls = [
            "Setas Cima/Baixo: Navegar entre opções",
            "Setas Esquerda/Direita: Ajustar dificuldade",
            "Enter: Alternar opções",
            "ESC: Voltar e salvar"
        ]
        
        for i, ctrl in enumerate(controls):
            ctrl_text = self.assets.get_font("small").render(ctrl, True, Colors.BLACK)
            self.screen.blit(ctrl_text, (SCREEN_WIDTH // 2 - ctrl_text.get_width() // 2, instruction_y + i * 30))
        
        # Rodapé
        footer = self.assets.get_font("small").render("Pressione ESC para salvar e voltar", True, Colors.BLUE)
        self.screen.blit(footer, (SCREEN_WIDTH // 2 - footer.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    import math  # Importar aqui para evitar problemas
    game = SnakeGame()
    game.run()
