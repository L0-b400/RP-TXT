from flask import Flask, render_template, request, jsonify
import database
import game_logic

app = Flask(__name__)

@app.route('/')
def home():
    """Página inicial do jogo"""
    players = database.load_players()
    return render_template('index.html', players=players)

@app.route('/start_game', methods=['POST'])
def start_game():
    """Inicia o jogo e seleciona um jogador"""
    player_name = request.form['player_name']
    players = database.load_players()
    if player_name not in players:
        return jsonify({"message": "Jogador não encontrado!"}), 404
    
    return render_template('game.html', player_name=player_name, players=players)

@app.route('/action', methods=['POST'])
def action():
    """Processa a ação do jogador no jogo"""
    player_name = request.form['player_name']
    action = int(request.form['action'])
    result = game_logic.player_action(player_name, action)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
