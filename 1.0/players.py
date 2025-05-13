lista_player = []

def criar_player():
    jogador = input("digite o nome do jogador: ")

    novo_player = {
        "Nome": jogador,
        "Vida": 1,
        "For": 1,
        "Int": 1,
        "Sor": 1,
        "Agi": 1,
    }

    lista_player.append(novo_player)

def exibir_players():
    for player in lista_player:
       
        print(
            f"1 - {player['Nome']} // {player['Vida']} // {player['For']} // {player['Int']} // {player['Sor']} // {player['Agi']}"
        )
