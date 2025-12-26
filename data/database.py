# data/database.py

ITENS = {
    "espada_ferro": {
        "nome": "Espada de Ferro",
        "tipo": "arma",
        "ataque": 15,
        "valor": 100
    },
    "armadura_couro": {
        "nome": "Armadura de Couro",
        "tipo": "armadura",
        "defesa": 10,
        "valor": 80
    },
    "pocao_vida": {
        "nome": "Poção de Vida",
        "tipo": "consumivel",
        "cura": 20,
        "valor": 25
    }
}

INIMIGOS = {
    "goblin": {
        "nome": "Goblin",
        "hp": 50, "atk": 10, "def": 4, "xp": 30, "ouro": 10,
        "drops": ["tecido_rasgado"]
    },
    "orc": {
        "nome": "Orc Brutal",
        "hp": 70, "atk": 15, "def": 6, "xp": 80, "ouro": 15,
        "drops": ["minerio_ferro"]
    }
}

RECEITAS = {
    "espada_ferro": {
        "materiais": {"Minério de Ferro": 3},
        "custo_ouro": 50
    },
    "armadura_couro": {
        "materiais": {"Pele de Lobo": 4},
        "custo_ouro": 40
    }
}