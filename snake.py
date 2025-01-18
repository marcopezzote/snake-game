import pygame
import random
from pygame.locals import *

# Inicialização do Pygame
pygame.init()

# Definições da tela
WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600
BEGIN_POS_X = WINDOWS_WIDTH / 2
BEGIN_POS_Y = WINDOWS_HEIGHT / 2
BLOCK = 10
FPS = 15

# Cores
PASTEL_GREEN = (152, 251, 152)  # Tom pastel de verde
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)  # Cor para o ponto alvo
DARK_BROWN = (139, 69, 19)  # Cor mais forte para as barreiras
YELLOW = (255, 255, 0)  # Cor para a pontuação
SNAKE_COLOR = (53, 59, 72)  # Cor da cobra
CINZA = (105, 105, 105)  # Cor para a barreira

# Tela
window = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption("Jogo da Cobra")

# Função para mostrar o placar
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def message(msg, color, x_offset=0, y_offset=0):
    mesg = font_style.render(msg, True, color)
    mesg_width = mesg.get_width()
    mesg_height = mesg.get_height()
    window.blit(mesg, [(WINDOWS_WIDTH - mesg_width) / 2 + x_offset, 
                       (WINDOWS_HEIGHT - mesg_height) / 3 + y_offset])

def your_score(score):
    value = score_font.render("Pontuação: " + str(score), True, DARK_BROWN)
    window.blit(value, [(WINDOWS_WIDTH - value.get_width()) / 2, 0])

# Função para o jogo principal
def gameLoop():
    # Posições iniciais da cobra
    snake_pos = [(BEGIN_POS_X, BEGIN_POS_Y)]
    snake_dir = 'RIGHT'
    snake_length = 1

    # Posições da comida
    food_pos = (random.randrange(1, (WINDOWS_WIDTH // BLOCK)) * BLOCK,
                random.randrange(1, (WINDOWS_HEIGHT // BLOCK)) * BLOCK)
    food_spawn = True

    # Barreiras
    barriers = []

    # Posições e direção iniciais
    x_change = BLOCK
    y_change = 0

    # Game Over flag
    game_over = False

    # Game Loop
    while not game_over:

        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            if event.type == KEYDOWN:
                if event.key == K_LEFT and snake_dir != 'RIGHT':
                    x_change = -BLOCK
                    y_change = 0
                    snake_dir = 'LEFT'
                elif event.key == K_RIGHT and snake_dir != 'LEFT':
                    x_change = BLOCK
                    y_change = 0
                    snake_dir = 'RIGHT'
                elif event.key == K_UP and snake_dir != 'DOWN':
                    y_change = -BLOCK
                    x_change = 0
                    snake_dir = 'UP'
                elif event.key == K_DOWN and snake_dir != 'UP':
                    y_change = BLOCK
                    x_change = 0
                    snake_dir = 'DOWN'

        # Movimento da cobra
        head_x = snake_pos[0][0] + x_change
        head_y = snake_pos[0][1] + y_change
        new_head = (head_x, head_y)

        # Condições de game over (colisão com as paredes, com o próprio corpo ou com as barreiras)
        if head_x >= WINDOWS_WIDTH or head_x < 0 or head_y >= WINDOWS_HEIGHT or head_y < 0:
            game_over = True
        for block in snake_pos[1:]:
            if block == new_head:
                game_over = True
        for barrier in barriers:
            if barrier == new_head:
                game_over = True

        # Se a cobra comer a comida
        snake_pos.insert(0, new_head)
        if new_head == food_pos:
            food_spawn = False
            snake_length += 1
            # Adicionar barreira após comer a comida
            barriers.append((random.randrange(1, (WINDOWS_WIDTH // BLOCK)) * BLOCK,
                             random.randrange(1, (WINDOWS_HEIGHT // BLOCK)) * BLOCK))
        else:
            snake_pos.pop()

        if not food_spawn:
            food_pos = (random.randrange(1, (WINDOWS_WIDTH // BLOCK)) * BLOCK,
                        random.randrange(1, (WINDOWS_HEIGHT // BLOCK)) * BLOCK)
        food_spawn = True

        # Atualizar a tela
        window.fill(PASTEL_GREEN)

        # Desenhar a comida (ponto alvo) em vermelho
        pygame.draw.rect(window, RED, [food_pos[0], food_pos[1], BLOCK, BLOCK])

        # Desenhar as barreiras
        for barrier in barriers:
            pygame.draw.rect(window, CINZA, [barrier[0], barrier[1], BLOCK, BLOCK])

        # Desenhar a cobra com um estilo mais agradável
        for i, pos in enumerate(snake_pos):
            color = SNAKE_COLOR if i == 0 else (0, 0, 0)  # A cabeça da cobra será de cor diferente
            pygame.draw.rect(window, color, [pos[0], pos[1], BLOCK, BLOCK])
            # Sombra para dar um efeito de profundidade
            pygame.draw.rect(window, (0, 0, 0), [pos[0] + 2, pos[1] + 2, BLOCK, BLOCK])

        # Mostrar o placar
        your_score(snake_length - 1)

        # Atualizar a tela
        pygame.display.update()

        # Controle de FPS
        pygame.time.Clock().tick(FPS)

    # Mensagem de Game Over
    window.fill(PASTEL_GREEN)
    message("Fim de Jogo!", RED, y_offset=50)
    message("Pressione Q para Sair ou C para Jogar Novamente", RED, y_offset=100)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    quit()
                if event.key == K_c:
                    gameLoop()

# Iniciar o jogo
gameLoop()
