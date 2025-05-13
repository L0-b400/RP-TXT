import random
import json
import database

def load_defeated_monsters():
    """Carrega os monstros derrotados do arquivo JSON"""
    try:
        with open("monstros_derrotados.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Retorna uma lista vazia caso o arquivo não exista

def save_defeated_monsters(monsters):
    """Salva os monstros derrotados no arquivo JSON"""
    with open("monstros_derrotados.json", "w") as file:
        json.dump(monsters, file)

def player_action(player_name, action):
    """Processa a ação escolhida pelo jogador e atualiza o status"""
    players = database.load_players()
    
    if player_name not in players:
        return "❌ Jogador não encontrado."
    
    player = players[player_name]
    dice_roll = random.randint(1, 12)  # Rola um dado de 12 lados
    print(f"Você tirou {dice_roll}")
    
    # Determina a ação escolhida
    if action == 1:
        outcome = attack(player, dice_roll)
    elif action == 2:
        outcome = defend(player, dice_roll)
    elif action == 3:
        outcome = rest(player)
    elif action == 4:
        outcome = flee(player, dice_roll)
    elif action == 5:
        outcome = walk(player_name)  # Caminhar/Explorar o mapa
    else:
        return "❌ Ação inválida!"
    
    apply_status_effect(player)  # Aplica os efeitos de status ao jogador
    players[player_name] = player  # Atualiza o jogador na base de dados
    database.save_players(players)  # Salva as mudanças no JSON
    
    return outcome

def apply_status_effect(player):
    """Aplica os efeitos de status ao jogador dependendo do seu status atual"""
    status_effects = {
        "Machucado": {"vida": -2},
        "Envenenado": {"vida": -1, "força": -1},
        "Sangrando": {"vida": -3},
        "Cansado": {"agilidade": -2},
        "A beira da morte": {"vida": -5, "força": -3, "inteligencia": -3},
        "Com bastante energia": {"agilidade": +2, "força": +1},
        "Forte": {"força": +3},
        "Resistente": {"vida": +3}
    }
    
    if "status" in player and player["status"] in status_effects:
        for attr, value in status_effects[player["status"]].items():
            player[attr] = max(1, player[attr] + value)  # Garante que o valor mínimo do atributo seja 1

def attribute_gain_chance(dice_roll):
    """Determina a chance do jogador ganhar um ponto de atributo com base no dado"""
    if dice_roll >= 10:
        return random.random() < 0.8  # 80% de chance
    elif dice_roll >= 7:
        return random.random() < 0.5  # 50% de chance
    elif dice_roll >= 4:
        return random.random() < 0.3  # 30% de chance
    else:
        return random.random() < 0.1  # 10% de chance

# Funções de ação do jogador:
def attack(player, dice_roll):
    """Processa o ataque do jogador"""
    if attribute_gain_chance(dice_roll):
        player["força"] += 1
        return f"🗡️ Ataque bem-sucedido! Você ganhou +1 de força. Novo status: {player}"
    
    if random.random() < 0.3:
        player["status"] = "Sangrando"
        return "⚔️ Você atacou, mas se machucou! Está sangrando!"
    
    return "⚔️ Você atacou, mas não conseguiu melhorar sua força."

def defend(player, dice_roll):
    """Processa a defesa do jogador"""
    if attribute_gain_chance(dice_roll):
        player["agilidade"] += 1
        return f"🛡️ Defesa bem-sucedida! Você ganhou +1 de agilidade. Novo status: {player}"
    
    if random.random() < 0.3:
        player["status"] = "Machucado"
        return "🛡️ Você se defendeu, mas se machucou!"

    return "🛡️ Defesa bem-sucedida, mas sem melhorias."

def rest(player):
    """Recupera vida do jogador ao descansar"""
    player["vida"] = min(player["vida"] + 5, 20)
    
    if "status" in player and player["status"] != "normal":
        cure_chance = random.random()
        if cure_chance >= 0.7:
            player["status"] = "normal"
            return f"💤 Você descansou e recuperou 5 de vida. Além disso, seu debuff foi curado! Vida atual: {player['vida']}"
        else:
            return f"💤 Você descansou e recuperou 5 de vida, mas seu debuff ainda persiste. Vida atual: {player['vida']}"
    
    return f"💤 Você descansou e recuperou 5 de vida. Vida atual: {player['vida']}"

def flee(player, dice_roll):
    """Tenta fugir do combate"""
    if dice_roll >= 10:
        return "🏃 Você conseguiu fugir com sucesso!"
    return "🚪 Tentativa de fuga falhou!"

def walk(player_name):
    """Simula caminhar no mapa e encontrar monstros"""
    players = database.load_players()
    
    if player_name not in players:
        return "❌ Jogador não encontrado."
    
    player = players[player_name]
    
    walk_choice = input("Você quer caminhar para frente? (1- Sim /2- não): ").strip().lower()
    
    if walk_choice != "1":
        return "Você decidiu não caminhar."

    level = player.get("level", 1)
    monster = generate_monster(level)
    
    if monster:
        print(f"Você encontrou um monstro de nível {monster['level']}!")
        outcome = combat(player, monster)
        return outcome
    else:
        return "Você caminhou sem encontrar nenhum monstro."
    
def generate_monster(player_level):
    """Gera um monstro baseado no nível do jogador"""
    monster_level = random.randint(max(1, player_level - 1), player_level + 2)
    return {"level": monster_level, "vida": monster_level * 10, "força": monster_level * 2, "nome": f"Monstro {monster_level}"}

def combat(player, monster):
    """Realiza o combate entre o jogador e o monstro"""
    print("\n🎮 Começando a batalha!")
    
    while player["vida"] > 0 and monster["vida"] > 0:
        print(f"\nVocê tem {player['vida']} de vida e {player['força']} de força.")
        print(f"O monstro tem {monster['vida']} de vida e {monster['força']} de força.")
        
        print("Escolha uma ação:")
        print("1. Atacar")
        print("2. Defender")
        print("3. Fugir")
        action = input("Digite o número da ação: ").strip()

        if action == "1":
            print(attack(player, random.randint(1, 12)))
            damage = max(1, player["força"] - random.randint(1, 4))
            monster["vida"] -= damage
            print(f"Você causou {damage} de dano no monstro! Vida do monstro: {monster['vida']}")
        elif action == "2":
            print(defend(player, random.randint(1, 12)))
        elif action == "3":
            return flee(player, random.randint(1, 12))
        else:
            print("❌ Ação inválida!")

        monster_attack(player, monster)
        
    if player["vida"] <= 0:
        return "💀 Você foi derrotado pelo monstro..."
    else:
        defeated_monsters = load_defeated_monsters()
        defeated_monsters.append({"nome": monster["nome"], "level": monster["level"]})
        save_defeated_monsters(defeated_monsters)
        
        return "🏆 Você derrotou o monstro!"

def monster_attack(player, monster):
    """Realiza o ataque do monstro"""
    print(f"O monstro ataca com {monster['força']} de força!")
    damage = max(1, monster["força"] - random.randint(1, 4))
    player["vida"] -= damage
    print(f"O monstro causou {damage} de dano em você! Sua vida: {player['vida']}")
