import pandas as pd
import os

EXCEL_PATH = "data/produtos.xlsx"

def carregar_catalogo():
    if not os.path.exists(EXCEL_PATH):
        return None
    # Lê o Excel garantindo que as colunas sejam strings para busca
    df = pd.read_excel(EXCEL_PATH, dtype=str)
    # Converte preço para float para cálculos se necessário, mas aqui manteremos string para exibição
    return df

def buscar_produto_no_excel(termo_busca: str) -> str:
    """
    Busca produtos no catálogo Excel pelo nome ou setor.
    Retorna uma string formatada com as opções encontradas.
    """
    df = carregar_catalogo()
    if df is None:
        return "Erro: Catálogo de produtos não encontrado."

    termo = termo_busca.lower()

    # Filtra onde o termo aparece no Produto ou no Setor
    resultados = df[
        df['Produto'].str.lower().str.contains(termo, na=False) | 
        df['Setor'].str.lower().str.contains(termo, na=False)
    ]

    if resultados.empty:
        return f"Desculpe, não encontrei nenhum produto relacionado a '{termo_busca}'."

    resposta = f"🔎 Encontrei estas opções para '{termo_busca}':\n\n"

    for _, row in resultados.iterrows():
        # Formata conforme suas colunas: Produto, Marca, Unidade, Preço
        resposta += f"- {row['Produto']} ({row['Marca']}) - {row['Unidade']}: R$ {row['Preço']}\n"

    return resposta
