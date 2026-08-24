"""Resolução de caminhos que funciona tanto rodando `python main.py`
quanto empacotado como .exe (PyInstaller).

Sem isso, caminhos como "data/quests.json" ou "saves/save_slot_1.json"
só funcionam se você rodar o programa exatamente de dentro da pasta do
projeto — o que quebra fácil quando é um executável na Área de Trabalho.
"""
import os
import sys


def _congelado():
    """True quando rodando como .exe empacotado pelo PyInstaller."""
    return bool(getattr(sys, "frozen", False))


def dir_dados():
    """Pasta onde ficam os arquivos de dados somente-leitura (ex.: data/quests.json).

    Quando empacotado com `--add-data`, o PyInstaller extrai esses arquivos
    para uma pasta temporária apontada por sys._MEIPASS.
    """
    if _congelado():
        return sys._MEIPASS  # type: ignore[attr-defined]
    # core/paths.py -> sobe um nível (core/) -> raiz do projeto
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dir_app():
    """Pasta onde o .exe (ou o main.py) realmente está.

    Usada para dados GRAVÁVEIS, como a pasta saves/ — ela precisa sobreviver
    entre execuções, e sys._MEIPASS é apagada toda vez que o programa fecha.
    """
    if _congelado():
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
