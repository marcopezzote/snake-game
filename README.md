# Snake Game - Jogo da Cobra em Pygame

![Python Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame Badge](https://img.shields.io/badge/Pygame-20232A?style=for-the-badge&logo=python&logoColor=white)

Este é um jogo Snake (Jogo da Cobra) moderno e profissional desenvolvido em Python utilizando a biblioteca Pygame. O projeto demonstra conceitos avançados de programação, incluindo orientação a objetos, gerenciamento de estados, e técnicas de game design.

## 🎮 Características Principais

- **Design Orientado a Objetos**: Código estruturado com classes e hierarquias bem definidas
- **Sistema de Menu Completo**: Menu principal, tela de opções e tabela de recordes
- **Múltiplos Níveis de Dificuldade**: O jogo aumenta de dificuldade conforme o jogador avança
- **Power-ups Diversos**: Diversos itens especiais que afetam a jogabilidade:
  - **Velocidade+**: Aumenta temporariamente a velocidade da cobra
  - **Velocidade-**: Diminui temporariamente a velocidade da cobra
  - **Invencibilidade**: Torna a cobra temporariamente imune a colisões
  - **Pontos+**: Adiciona pontos extras ao placar
  - **Redução**: Reduz o tamanho da cobra pela metade
- **Sistema de Níveis**: A cada 5 comidas consumidas, o jogador avança um nível
- **Barreiras Dinâmicas**: Novas barreiras aparecem a cada nível, aumentando o desafio
- **Sistema de Recordes**: Armazena e exibe as melhores pontuações

## 📷 Capturas de Tela

![Jogo Snake](screenshot.png)

## 🔧 Instalação

### Pré-requisitos

- **Python 3.x**: Certifique-se de ter o Python 3 instalado no seu computador
- **Pygame**: A biblioteca Pygame deve ser instalada para que o jogo funcione corretamente
- **NumPy**: Necessário para geração de efeitos sonoros

### Como instalar em Linux

1. Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/snake-game.git
```

2. Navegue até o diretório do projeto:

```bash
cd snake-game
```

3. Crie um ambiente virtual (recomendado):

```bash
python3 -m venv venv
```

4. Ative o ambiente virtual:

```bash
source venv/bin/activate
```

5. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

6. Execute o jogo:

```bash
python run_game.py
```

### Verificação de dependências

Se preferir, você pode usar nosso script de verificação para garantir que todas as dependências estão instaladas:

```bash
chmod +x check_project.py
./check_project.py
```

### Desativando o ambiente virtual

Quando terminar de jogar, você pode desativar o ambiente virtual:

```bash
deactivate
```

## 🎯 Como Jogar

- **Menu Principal**: Use as setas para cima e para baixo para navegar e Enter para selecionar
- **Durante o Jogo**:
  - **Setas Direcionais**: Controle a direção da cobra
  - **ESC**: Pause o jogo
  - **Q** (quando pausado): Volte ao menu principal
- **Objetivo**: Coma os itens vermelhos para crescer e ganhar pontos
- **Power-ups**: Itens coloridos especiais que aparecem periodicamente com efeitos diferentes
- **Desafio**: Evite colidir com as paredes, barreiras ou com o próprio corpo da cobra

## 💻 Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação principal
- **Pygame**: Biblioteca para criação de jogos 2D
- **NumPy**: Para processamento numérico e geração de sons
- **Programação Orientada a Objetos**: Para estruturação do código
- **JSON**: Para armazenamento de configurações e recordes

## 🏗️ Arquitetura do Jogo

O jogo é estruturado com os seguintes componentes principais:

- **SnakeGame**: Classe principal que gerencia o jogo
- **Snake**: Controla o comportamento e renderização da cobra
- **Food**: Gerencia os itens que a cobra deve comer
- **PowerUp**: Implementa os diferentes power-ups e seus efeitos
- **MainMenu**: Gerencia a interface do menu principal
- **GameSettings**: Armazena configurações e recordes
- **AssetManager**: Carrega e gerencia recursos como sons e fontes

## 🛠️ Resolução de Problemas em Linux

### Problemas com o Pygame

Se você encontrar problemas com o Pygame em sistemas Linux, pode ser necessário instalar algumas dependências adicionais:

```bash
sudo apt-get update
sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

### Problemas de Áudio

Se os efeitos sonoros não funcionarem:

```bash
sudo apt-get install libasound2-dev
pip install pygame==2.0.1 --upgrade
```

### Problemas de Permissão

Se encontrar problemas de permissão ao executar os scripts:

```bash
chmod +x run_game.py
chmod +x generate_sounds.py
chmod +x check_project.py
```

## 🚀 Melhorias Futuras

- Implementação de modo multijogador
- Novas variedades de power-ups
- Mapas com formatos diferentes
- Modo de jogo sem fim (endless)
- Efeitos visuais aprimorados

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
