# src/analises/regras.py
from pathlib import Path
import json

# Define o caminho para o arquivo JSON de regras
# Agora usa 'regras_config.json'
REGRAS_CONFIG_FILE = Path(__file__).resolve().parent / "regras_config.json"

def carrega_regras_de_analise() -> dict:
    """Carrega as regras de análise do arquivo regras_config.json."""
    try:
        with open(REGRAS_CONFIG_FILE, 'r', encoding='utf-8') as f:
            # Agora retorna a chave principal "REGRAS_DE_ANALISE"
            return json.load(f)["REGRAS_DE_ANALISE"] 
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo de regras não foi encontrado em: {REGRAS_CONFIG_FILE}")
    except json.JSONDecodeError:
        raise ValueError(f"Erro ao decodificar o JSON no arquivo: {REGRAS_CONFIG_FILE}")

# Carrega as regras uma única vez ao importar o módulo
REGRAS_DE_ANALISE = carrega_regras_de_analise()

# Exporta o dicionário carregado
__all__ = ["REGRAS_DE_ANALISE"]