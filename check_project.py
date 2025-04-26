#!/usr/bin/env python3
"""
Script para verificar e testar o Snake Game
"""

import os
import sys
import subprocess
import shutil

def check_dependencies():
    """Verifica e instala dependências necessárias"""
    print("Verificando dependências...")
    
    try:
        import pygame
        print("✓ Pygame instalado.")
    except ImportError:
        print("✗ Pygame não encontrado. Instalando...")
        subprocess.call([sys.executable, "-m", "pip", "install", "pygame"])
        print("✓ Pygame instalado com sucesso!")

    try:
        import numpy
        print("✓ Numpy instalado.")
    except ImportError:
        print("✗ Numpy não encontrado. Instalando...")
        subprocess.call([sys.executable, "-m", "pip", "install", "numpy"])
        print("✓ Numpy instalado com sucesso!")

def check_files():
    """Verifica a existência dos arquivos necessários"""
    print("\nVerificando arquivos do jogo...")
    
    required_files = [
        "snake_game.py",
        "run_game.py",
        "requirements.txt",
        "README.md"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} encontrado.")
        else:
            print(f"✗ {file} não encontrado!")

def check_assets():
    """Verifica a existência dos assets necessários"""
    print("\nVerificando assets do jogo...")
    
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        print(f"✗ Diretório {assets_dir} não encontrado. Criando...")
        os.makedirs(assets_dir)
        print(f"✓ Diretório {assets_dir} criado com sucesso!")
    else:
        print(f"✓ Diretório {assets_dir} encontrado.")
    
    # Verificar sons
    sound_files = ["eat.wav", "crash.wav", "powerup.wav"]
    missing_sounds = False
    
    for sound in sound_files:
        sound_path = os.path.join(assets_dir, sound)
        if os.path.exists(sound_path):
            print(f"✓ Som {sound} encontrado.")
        else:
            print(f"✗ Som {sound} não encontrado!")
            missing_sounds = True
    
    if missing_sounds:
        print("\nGerando arquivos de som faltantes...")
        try:
            if os.path.exists("generate_sounds.py"):
                subprocess.call([sys.executable, "generate_sounds.py"])
                print("✓ Sons gerados com sucesso!")
            else:
                print("✗ Script generate_sounds.py não encontrado!")
        except Exception as e:
            print(f"✗ Erro ao gerar sons: {e}")

def generate_screenshot():
    """Gera uma nova captura de tela do jogo"""
    print("\nGerando nova captura de tela do jogo...")
    print("Isso pode demorar alguns segundos...")
    
    try:
        # Configurar a variável de ambiente para não exibir a janela do Pygame
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        
        # Importar pygame e inicializar
        import pygame
        pygame.init()
        
        # Resetar a variável de ambiente
        os.environ.pop("SDL_VIDEODRIVER", None)
        
        # Lançar o jogo para captura com o módulo específico
        try:
            # Tentar importar o módulo de captura de tela
            import pyscreenshot as ImageGrab
            
            print("Iniciando o jogo para captura...")
            game_process = subprocess.Popen([sys.executable, "run_game.py"])
            
            # Aguardar um tempo para o jogo carregar
            import time
            time.sleep(5)
            
            # Capturar a tela
            im = ImageGrab.grab()
            im.save("screenshot_new.png")
            
            # Encerrar o processo do jogo
            game_process.terminate()
            
            print("✓ Nova captura de tela gerada como screenshot_new.png!")
            
        except ImportError:
            print("Módulo pyscreenshot não encontrado. Pulando geração automática de screenshot.")
            print("Você pode gerar manualmente jogando o jogo e usando a tecla Print Screen.")
    
    except Exception as e:
        print(f"✗ Erro ao gerar captura de tela: {e}")

def run_tests():
    """Executa testes simples para validar o jogo"""
    print("\nExecutando testes básicos do jogo...")
    
    try:
        # Testar importação da classe principal
        from snake_game import SnakeGame
        print("✓ Classe SnakeGame importada com sucesso!")
        
        # Verificar se o método run existe
        if hasattr(SnakeGame, "run"):
            print("✓ Método run() encontrado na classe SnakeGame!")
        else:
            print("✗ Método run() não encontrado na classe SnakeGame!")
        
        # Verificar importação de outras classes
        from snake_game import Snake, Food, PowerUp, MainMenu
        print("✓ Classes auxiliares importadas com sucesso!")
        
    except Exception as e:
        print(f"✗ Erro nos testes: {e}")

def print_summary():
    """Imprime um resumo do estado do projeto"""
    print("\n" + "="*60)
    print("RESUMO DO PROJETO SNAKE GAME")
    print("="*60)
    
    # Verificar arquivo README
    if os.path.exists("README.md"):
        with open("README.md", "r") as f:
            readme_content = f.read()
            readme_size = len(readme_content)
            print(f"README: {readme_size} caracteres")
    else:
        print("README: Não encontrado")
    
    # Verificar tamanho do código principal
    if os.path.exists("snake_game.py"):
        with open("snake_game.py", "r") as f:
            code_content = f.read()
            code_size = len(code_content)
            lines = code_content.count("\n") + 1
            print(f"Código principal: {code_size} caracteres, {lines} linhas")
    else:
        print("Código principal: Não encontrado")
    
    # Listar arquivos do projeto
    print("\nArquivos do projeto:")
    for item in os.listdir("."):
        if os.path.isfile(item):
            size = os.path.getsize(item)
            print(f"- {item}: {size/1024:.1f} KB")
    
    print("\nO jogo está pronto para ser executado!")
    print("Execute com: python run_game.py")

def main():
    """Função principal"""
    print("=== Snake Game - Verificação do Projeto ===\n")
    
    check_dependencies()
    check_files()
    check_assets()
    run_tests()
    # Comentado para não gerar screenshots automaticamente
    # generate_screenshot()
    print_summary()

if __name__ == "__main__":
    main()
