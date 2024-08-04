# src/config.py (Trecho Atualizado)
from pathlib import Path
import json

# Define o diretório raiz do projeto (o diretório acima de 'src')
DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent

# Caminho para o arquivo JSON de configuração (estático)
CONFIG_JSON_FILE = DIRETORIO_RAIZ / "src" / "config.json"

# Carrega os dados do arquivo JSON
def _carrega_config_json():
    """Carrega o arquivo de configuração JSON."""
    # ... (lógica de try/except)
    try:
        with open(CONFIG_JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo de configuração não foi encontrado em: {CONFIG_JSON_FILE}")
        
# Carrega a configuração uma única vez ao iniciar o módulo
_DADOS_CONFIG = _carrega_config_json()


# -----------------------------------------------------------------
# Configurações de Caminho e Parâmetros (Geradas Dinamicamente)
# -----------------------------------------------------------------

# Parâmetros lidos do JSON
FORMATO_DADOS = _DADOS_CONFIG.get("formato_dados")
SEPARADOR = _DADOS_CONFIG.get("separador", ",") # <--- AGORA LÊ E EXPORTA O SEPARADOR!

# Caminho completo para o diretório de dados brutos
CAMINHO_DADOS_BRUTOS = DIRETORIO_RAIZ / _DADOS_CONFIG.get("caminho_dados")

# Caminho completo para a planilha de parâmetros de análise
ARQUIVO_PARAMETROS_EDA = DIRETORIO_RAIZ / "params" / _DADOS_CONFIG.get("arquivo_parametros")


# Lista de caminhos e parâmetros disponíveis para importação em outros módulos
__all__ = [
    "DIRETORIO_RAIZ",
    "CAMINHO_DADOS_BRUTOS",
    "ARQUIVO_PARAMETROS_EDA",
    "FORMATO_DADOS",
    "SEPARADOR",            # <--- EXPORTADO
    "_DADOS_CONFIG"         # Manter para utilidades.py acessar dados brutos
]