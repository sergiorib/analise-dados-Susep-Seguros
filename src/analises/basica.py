# src/analises/basica.py
import pandas as pd
from .. import config # Importa o módulo de config do diretório pai (src)

def rodar_analises_universais(nome_tabela: str, df: pd.DataFrame, nome_arquivo: str) -> list:
    """
    Executa análises básicas e universais em nível de arquivo e tabela.
    
    Args:
        nome_tabela: O nome da tabela sendo analisada (do eda.xlsx).
        df: O DataFrame ativo.
        nome_arquivo: O nome do arquivo no disco.
        
    Retorna:
        Uma lista de dicionários no formato de Log Padronizado.
    """
    resultados = []
    
    # --- Análises de Nível de Arquivo (Grupo: Dados do arquivo) ---
    
    # 1. Análise: Tamanho
    caminho_completo = config.CAMINHO_DADOS_BRUTOS / nome_arquivo
    try:
        tamanho_bytes = caminho_completo.stat().st_size
        tamanho_mb = tamanho_bytes / (1024 * 1024)
        
        resultados.append({
            "ID": 0,
            "Tabela": nome_tabela,
            "Campo": "Nenhum",
            "Grupo_analise": "Dados do arquivo",
            "Analise": "Tamanho",
            "Resultado": f"{tamanho_mb:.2f} MB",
            "Evidencia": f"Caminho: {caminho_completo.name}",
            "Detalhes": "",
            "Status": "Pass", 

        })
    except FileNotFoundError:
        # Se o arquivo de dados brutos não for encontrado, falha.
        resultados.append({
            "ID": 0,
            "Tabela": nome_tabela,
            "Campo": "Nenhum",
            "Grupo_analise": "Dados do arquivo",
            "Analise": "Tamanho",
            "Resultado": "Arquivo não encontrado",
            "Evidencia": f"Arquivo {nome_arquivo}",
            "Detalhes": "",
            "Status": "Fail"
        })

    # --- Análises de Nível de Tabela (Grupo: Dados da tabela) ---

    # 2. Análise: Quantidade de Registros
    qtde_registros = len(df)
    resultados.append({
        "ID": 0,
        "Tabela": nome_tabela,
        "Campo": "Nenhum",
        "Grupo_analise": "Dados da tabela",
        "Analise": "Qtde de registros",
        "Resultado": f"{qtde_registros:,}".replace(",", "."), 
        "Evidencia": f"Linhas x Colunas: {df.shape}",
        "Detalhes": "",
        "Status": "Pass"
    })
    
    # 3. Análise: Total de Colunas
    colunas_df = ", ".join(df.columns.tolist())
    resultados.append({
        "ID": 0,
        "Tabela": nome_tabela,
        "Campo": "Nenhum",
        "Grupo_analise": "Dados da tabela",
        "Analise": "Total de Colunas",
        "Resultado": f"{len(df.columns)}",
        "Evidencia": f"Primeiras Colunas: {colunas_df[:50]}...",
        "Detalhes": "",
        "Status": "Pass"
    })
    
    return resultados

# Exporta a função para ser importada pelo orquestrador
__all__ = ["rodar_analises_universais"]