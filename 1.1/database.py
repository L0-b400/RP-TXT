import json
import os

# Define o caminho do arquivo de dados (players.json) dentro da pasta onde o script está rodando
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "players.json")  # O arquivo JSON fica na pasta do jogo

def load_players():
    """Carrega os dados dos jogadores do arquivo JSON"""
    if not os.path.exists(DB_FILE):
        return {}  # Retorna um dicionário vazio se o arquivo não existir ainda

    with open(DB_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_players(players):
    """Salva os dados atualizados dos jogadores no arquivo JSON"""
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(players, file, indent=4, ensure_ascii=False)

def add_player(name):
    """Adiciona um novo jogador ao banco de dados"""
    players = load_players()
    if name not in players:
        players[name] = {
            "level": 1,  # Nível inicial do jogador
            "vida": 10,  # Vida inicial
            "força": 5,  # Força inicial
            "agilidade": 5,  # Agilidade inicial
            "status": "normal"  # Status inicial
        }
        save_players(players)
    return f"✅ Jogador '{name}' criado com sucesso!"
