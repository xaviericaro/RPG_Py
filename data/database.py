# data/database.py

ITENS = {
    "Minério de Ferro": {"tipo": "material", "valor": 15},
    "Pele de Lobo": {"tipo": "material", "valor": 10},
    "Tecido Rasgado": {"tipo": "material", "valor": 5},
    "Escama de Dragão": {"tipo": "material", "valor": 100},
    
    "Espada de Ferro": {
        "tipo": "arma", 
        "ataque": 15, 
        "valor": 100, 
        "durabilidade": 100
    },
    "Armadura de Couro": {
        "tipo": "armadura", 
        "defesa": 10, 
        "valor": 80, 
        "durabilidade": 100
    }
}

RECEITAS = {
    "Espada de Ferro": {
        "materiais": {"Minério de Ferro": 3},
        "custo_ouro": 50
    },
    "Armadura de Couro": {
        "materiais": {"Pele de Lobo": 4},
        "custo_ouro": 40
    }
}

# Aqui você define os inimigos e o que eles podem dropar (pelas chaves do ITENS)
LISTA_INIMIGOS = {
    "Floresta": [
        {"nome": "Goblin", "hp": 50, "atk": 10, "def": 4, "xp": 30, "ouro": 10, "drops": ["Tecido Rasgado"]},
        {"nome": "Orc Brutal", "hp": 70, "atk": 15, "def": 6, "xp": 80, "ouro": 15, "drops": ["Minério de Ferro"]},
        {"nome": "Lobo Sombrio", "hp": 80, "atk": 18, "def": 7, "xp": 60, "ouro": 20, "drops": ["Pele de Lobo"]}
    ],
    "Montanha": [
        {"nome": "Dragão Ancião", "hp": 250, "atk": 35, "def": 15, "xp": 300, "ouro": 200, "drops": ["Escama de Dragão"]}
    ],
}

MAPA = {
    "Vilarejo": {
        "descricao": "Um vilarejo tranquilo, com pessoas amigaveis.",
        "opcoes": [
            "Falar com o Ancião",
            "Ir à Loja",
            "Descansar",
            "Distribuir Pontos",
            "Ferreiro (Crafting)",
            "Salvar e Sair",
            "Ir para a Floresta",
        ],
        "destinos": [
            None, None, None, None, None, None, "Floresta"
        ],
    },
    "Floresta": {
        "descricao": "Uma floresta sombria cheia de perigos.",
        "opcoes": [
            "Explorar",
            "Voltar ao Vilarejo",
            "Seguir para a Montanha",
        ],
        "destinos": [
            None, "Vilarejo", "Montanha"
        ],
    },
    "Montanha": {
        "descricao": "Uma montanha onde o Dragão Ancião habita.",
        "opcoes": [
            "Enfrentar o Dragão",
            "Voltar para a Floresta",
        ],
        "destinos": [
            None, "Floresta"
        ],
    },
}