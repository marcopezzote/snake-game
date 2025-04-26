#!/usr/bin/env python3
"""
Arquivo inicializador do Snake Game
"""

import os
import sys
import subprocess

def main():
    """Função principal para iniciar o jogo"""
    print("Iniciando Snake Game...")
    
    # Verificar se o Pygame está instalado
    try:
        import pygame
        print("Pygame já está instalado!")
    except ImportError:
        print("Pygame não encontrado. Instalando...")
        subprocess.call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Pygame instalado com sucesso!")

    try:
        import numpy
        print("Numpy já está instalado!")
    except ImportError:
        print("Numpy não encontrado. Instalando...")
        subprocess.call([sys.executable, "-m", "pip", "install", "numpy"])
        print("Numpy instalado com sucesso!")
    
    # Gerar os sons se eles não existirem
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    if not os.path.exists(os.path.join(assets_dir, "eat.wav")) or \
       not os.path.exists(os.path.join(assets_dir, "crash.wav")) or \
       not os.path.exists(os.path.join(assets_dir, "powerup.wav")):
        print("Gerando sons para o jogo...")
        try:
            from generate_sounds import generate_and_save
            # Usar a função importada para gerar os sons
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)
                
            # Gerar os sons do jogo
            generate_and_save("eat.wav", 440, 0.1, 0.6)
            generate_and_save("crash.wav", 100, 0.3, 0.7, True)
            generate_and_save("powerup.wav", 800, 0.2, 0.6)
        except:
            # Executar o script como processo separado
            subprocess.call([sys.executable, os.path.join(os.path.dirname(__file__), "generate_sounds.py")])
    
    # Iniciar o jogo
    try:
        from snake_game import SnakeGame
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        # Tentar executar diretamente
        subprocess.call([sys.executable, os.path.join(os.path.dirname(__file__), "snake_game.py")])

if __name__ == "__main__":
    main()
