import pygame
import numpy as np
import sys
import os

# Inicializar o mixer do pygame
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
pygame.init()

# Criar diretório de assets se não existir
assets_dir = os.path.join(os.path.dirname(__file__), "assets")
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# Função para gerar um sinal de áudio simples
def generate_sound(freq, duration, volume=0.5, fade_out=False):
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    wave = np.sin(2 * np.pi * freq * t) * volume * 32767
    wave = wave.astype(np.int16)
    
    sound_buffer = pygame.mixer.Sound(buffer=wave)
    
    if fade_out:
        sound_buffer.fadeout(int(duration * 500))
    
    return sound_buffer

# Função para gerar e salvar o som
def generate_and_save(filename, freq, duration, volume=0.5, fade_out=False):
    file_path = os.path.join(assets_dir, filename)
    sound = generate_sound(freq, duration, volume, fade_out)
    
    # Criar um objeto de som no formato correto
    pygame.mixer.Sound.save(sound, file_path)
    print(f"Som '{filename}' gerado e salvo em {file_path}")

# Gerar os sons do jogo
print("Gerando efeitos sonoros para o jogo Snake...")

# Som de comer a comida
generate_and_save("eat.wav", 440, 0.1, 0.6)

# Som de colisão
generate_and_save("crash.wav", 100, 0.3, 0.7, True)

# Som de power-up
generate_and_save("powerup.wav", 800, 0.2, 0.6)

print("Efeitos sonoros gerados com sucesso!")
pygame.quit()
