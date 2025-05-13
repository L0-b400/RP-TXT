import database
import game_logic

def main():
    print("🎲 Bem-vindo ao RPG de Texto! 🎲")
    
    # Criar ou carregar jogadores
    while True:
        name = input("Digite o nome do jogador (ou 'jogar' para começar o jogo): ").strip()
        if name.lower() == "jogar":
            break
        database.add_player(name)

    print("\n✅ Jogadores cadastrados! Vamos começar!")

    # Escolher o jogador atual
    player_atual = input("Escolha 1 jogador: ").strip()

    # Loop do jogo
    while True:
        print("\n📜 Escolha uma ação para o turno: ")
        print("1. Treinar Ataque")
        print("2. Treinar Agilidade")
        print("3. Descansar (cura vida) ")
        print("4. Fugir")
        print("5. Caminhar (explorar o mapa)")
        print("6. Sair do jogo")

        choice = input("\nDigite o número da ação: ").strip()

        if choice == "6":
            print("\n🎮 Jogo encerrado. Até a próxima!")
            break

        players = database.load_players()
        if player_atual not in players:
            print("Jogador não encontrado!")
            continue

        result = game_logic.player_action(player_atual, int(choice))
        print(result)

if __name__ == "__main__":
    main()
