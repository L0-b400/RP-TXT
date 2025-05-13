import random

def rolar_dado():
    resultado = random.randint(1, 12)  
    print(f'O resultado do dado de 12 lados é: {resultado}')

    """Determina a chance de ganhar pontos de atributo com base no número do dado"""
    if resultado >= 10:
        return 1 if random.random() < 0.8 else 0  # 80% de chance
    elif resultado >= 7:
        return 1 if random.random() < 0.5 else 0  # 50% de chance
    elif resultado >= 4:
        return 1 if random.random() < 0.3 else 0  # 30% de chance
    else:
        return 1 if random.random() < 0.1 else 0  # 10% de chance
    
def apply_status_effect(jogador):
    """Altera atributos conforme o status do jogador"""
    status_effects = {
        "Machucado": {"Vida": -2},
        "Envenenado": {"Vida": -1, "For": -1},
        "Sangrando": {"Vida": -3},
        "Cansado": {"Agi": -2},
        "A beira da morte": {"Vida": -5, "For": -3, "Int": -3},
        "Com bastante energia": {"Agi": +2, "For": +1},
        "Forte": {"For": +3},
        "Resistente": {"Vida": +3}
    }

    if jogador.status in status_effects:
        for attr, value in status_effects[jogador.status].items():
            setattr(jogador, attr, max(1, getattr(jogador, attr) + value))  # Mantém o mínimo de 1