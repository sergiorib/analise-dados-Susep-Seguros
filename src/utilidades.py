# src/utilidades.py
import pandas as pd
from . import config 
# Necessário para detecção de encoding (instalado via Poetry)
from charset_normalizer import from_path 

# Variáveis globais para rastrear o DataFrame e o estado do cache (Tabela Única)
DF_ATIVO = None
TABELA_ATUALMENTE_CARREGADA = None
ULTIMO_REGISTRO_DE_RESULTADO = None 

def carrega_dados_otimizado(linha_parametro: pd.Series) -> tuple[pd.DataFrame, dict]:
    """
    Carrega um DataFrame (tabela) do disco de forma otimizada (cache de tabela única).
    
    Retorna uma tupla: (pd.DataFrame, dict | None).
    - Em SUCESSO: (DataFrame, {})
    - Em FALHA: (DataFrame Vazio, dict de Registro de Resultado de Falha)
    """
    global DF_ATIVO
    global TABELA_ATUALMENTE_CARREGADA
    global ULTIMO_REGISTRO_DE_RESULTADO
    
    # Reseta o registro de resultado para esta nova tentativa de carregamento
    ULTIMO_REGISTRO_DE_RESULTADO = None 
    
    # Colunas lidas do df_parametros (assumindo nomes em minúsculo)
    nome_tabela = linha_parametro['tabela']
    nome_arquivo = linha_parametro['arquivo']
    nome_aba = linha_parametro.get('aba') 

    # 1. Verifica se a Tabela JÁ ESTÁ ATIVA na memória (Lógica de cache)
    if nome_tabela == TABELA_ATUALMENTE_CARREGADA and DF_ATIVO is not None:
        return DF_ATIVO, {}
    
    # 2. Se for uma NOVA Tabela, LIMPA a memória
    if TABELA_ATUALMENTE_CARREGADA is not None:
        # print(f"\nINFO: Descarregando tabela anterior: '{TABELA_ATUALMENTE_CARREGADA}'.") # Silencioso
        DF_ATIVO = None 
        TABELA_ATUALMENTE_CARREGADA = None

    # 3. Carrega a NOVA Tabela do Disco
    caminho_completo = config.CAMINHO_DADOS_BRUTOS / nome_arquivo
    
    # print(f"INFO: Carregando nova tabela: '{nome_tabela}' do arquivo {caminho_completo.name}") # Silencioso
    
    try:
        if config.FORMATO_DADOS == 'xlsx':
            # Leitura de Excel (com correção de engine)
            df = pd.read_excel(
                caminho_completo, 
                sheet_name=nome_aba, 
                engine='openpyxl'
            )
            
        elif config.FORMATO_DADOS == 'csv':
            # Obtém o separador configurado (que deve ser configurado no config.json)
            separador_configurado = config.SEPARADOR
            
            # Detecção de Encoding (usa charset-normalizer)
            try:
                # print("INFO: Tentando detectar encoding...") # Silencioso
                detectado = from_path(str(caminho_completo)).best() 
                encoding_detectado = detectado.encoding if detectado else 'utf-8'
            except Exception:
                encoding_detectado = 'utf-8' # Fallback
            
            # print(f"INFO: Usando Separador: '{separador_configurado}', Encoding: '{encoding_detectado}'") # Silencioso
            
            # Leitura do CSV: Força o separador e encoding
            df = pd.read_csv(
                caminho_completo,
                encoding=encoding_detectado,
                sep=separador_configurado,
                engine='python' # Mais tolerante a inconsistências
            )
            
        else:
            raise ValueError(f"Formato de dados '{config.FORMATO_DADOS}' não suportado.")
            
        # 4. Armazena a nova tabela como ATIVA (SUCESSO)
        DF_ATIVO = df
        TABELA_ATUALMENTE_CARREGADA = nome_tabela
        # print(f"SUCESSO: Tabela '{nome_tabela}' (shape: {df.shape}) agora é a tabela ATIVA.") # Silencioso
        return DF_ATIVO, {}

    except Exception as e:
        # 5. Tratamento de Falha Crítica de Estrutura (FAIL)
        # print(f"ERRO CRÍTICO ao carregar dados do arquivo '{nome_arquivo}'. Detalhe: {e}") # Silencioso
        
        # Cria o Registro de Resultado de Falha Padronizado
        registro_de_resultado = {
            "ID": 0,
            "Tabela": nome_tabela,
            "Campo": "Nenhum",
            "Grupo_analise": "Dados do arquivo",
            "Analise": "Estrutura (Carregamento)",
            "Resultado": str(e).split('\n')[0], # Pega apenas a primeira linha do erro (o erro real do parser)
            "Evidencia": nome_arquivo,          # O arquivo que deu problema é a evidência
            "Detalhes": f"Erro completo: {str(e)}", # Detalhe completo da falha
            "Status": "Fail"
        }
        
        ULTIMO_REGISTRO_DE_RESULTADO = registro_de_resultado
        
        # Retorna DataFrame vazio (pd.DataFrame()) para que df_dados.empty funcione no notebook
        return pd.DataFrame(), registro_de_resultado 

__all__ = ["carrega_dados_otimizado", "DF_ATIVO", "TABELA_ATUALMENTE_CARREGADA", "ULTIMO_REGISTRO_DE_RESULTADO"]