"""Resolução de caminhos que funciona tanto rodando `python main.py`
quanto empacotado como .exe (PyInstaller).

Tanto os dados de leitura (data/quests.json) quanto os dados graváveis
(saves/) são resolvidos a partir da mesma pasta: onde o .exe realmente
está. Isso evita depender da extração temporária do PyInstaller
(sys._MEIPASS), que é fácil de configurar errado num build manual —
basta colocar a pasta "data" do lado do executável.
"""
import os
import sys


def _congelado():
    """True quando rodando como .exe empacotado pelo PyInstaller."""
    return bool(getattr(sys, "frozen", False))


def dir_base():
    """Pasta onde o .exe (ou o main.py) realmente está."""
    if _congelado():
        return os.path.dirname(os.path.abspath(sys.executable))
    # core/paths.py -> sobe um nível (core/) -> raiz do projeto
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Mantidos como aliases para não quebrar quem já importa estes nomes:
# ambos apontam para a mesma pasta base agora.
def dir_dados():
    return dir_base()


def dir_app():
    return dir_base()