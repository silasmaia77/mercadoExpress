from llama_index.core.tools import FunctionTool
from src.excel_engine import buscar_produto_no_excel
from src.database import salvar_pedido_db
import os
from dotenv import load_dotenv

# --- IMPORTAÇÃO DA FUNÇÃO DE ENVIO (WAHA) ---
try:
    from waha import send_message
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from waha import send_message

load_dotenv()

# Carrega o ID do GRUPO do .env
GROUP_ID = os.getenv("GROUP_ID")

# --- FERRAMENTAS ---

def tool_consultar_preco(produto: str) -> str:
    """Consulta o preço e marca de um produto no catálogo."""
    return buscar_produto_no_excel(produto)

def tool_finalizar_pedido(nome: str, telefone: str, endereco: str, resumo_itens: str, total: float, metodo_pagamento: str) -> str:
    """
    Finaliza o pedido, salva no banco de dados, gera o arquivo TXT e NOTIFICA O GRUPO DA LOGÍSTICA.
    Deve ser chamado APENAS quando o cliente confirmar tudo e fornecer o endereço.
    """

    # 1. Salvar no Banco
    pedido_id = salvar_pedido_db(nome, telefone, endereco, resumo_itens, total, metodo_pagamento)

    # 2. Montar o conteúdo do pedido
    conteudo = (
        f"PEDIDO #{pedido_id}\n"
        f"Cliente: {nome}\n"
        f"Telefone: {telefone}\n"
        f"Endereço: {endereco}\n"
        f"Pagamento: {metodo_pagamento}\n"
        f"-------------------------\n"
        f"{resumo_itens}\n"
        f"-------------------------\n"
        f"TOTAL: R$ {total:.2f}\n"
    )

    # 3. Salvar TXT individual
    os.makedirs("data/pedidos", exist_ok=True)
    filename = f"data/pedidos/pedido_{pedido_id}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(conteudo)

    # --- NOVA LÓGICA: NOTIFICAR GRUPO ---
    if GROUP_ID:
        print(f"Enviando notificação para o grupo: {GROUP_ID}")
        # Adicionei emojis de alerta para chamar atenção no grupo
        msg_grupo = f"🚨 *NOVO PEDIDO NO SISTEMA!* 🚨\n\n{conteudo}\n📦 *Equipe:* Favor iniciar separação."
        try:
            send_message(chat_id=GROUP_ID, text=msg_grupo)
        except Exception as e:
            print(f"Erro ao notificar grupo: {e}")
    else:
        print("AVISO: GROUP_ID não configurado no .env. O grupo não foi notificado.")
    # ------------------------------------

    return f"Pedido #{pedido_id} finalizado e salvo com sucesso! Informe o número do pedido ao cliente."

# --- DEFINIÇÃO DAS TOOLS PARA O LLAMAINDEX ---
tools_mercado = [
    FunctionTool.from_defaults(fn=tool_consultar_preco),
    FunctionTool.from_defaults(fn=tool_finalizar_pedido)
]

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
Você é o atendente virtual do 'MercadoExpress'. Sua função é atender clientes via WhatsApp, consultar preços no Excel e fechar pedidos.

REGRAS RÍGIDAS DE COMPORTAMENTO:
1. **INÍCIO:** Na PRIMEIRA mensagem, se você ainda não sabe, pergunte o NOME e o TELEFONE do cliente. Guarde isso no contexto. Não prossiga sem isso.
2. **CONSULTA:** Use a ferramenta `tool_consultar_preco` para ver preços. NUNCA invente preços. Se não estiver na lista, diga que está em falta.
3. **CARRINHO:** Memorize o que o cliente pediu. Se ele pedir "2 leites", e depois "1 arroz", o carrinho tem os dois.
4. **ENDEREÇO:** Só peça o endereço de entrega quando o cliente disser que quer fechar/finalizar a compra.
5. **PAGAMENTO:** 
   - Aceitamos: Dinheiro, Débito, Crédito, PIX.
   - **Dinheiro:** Pergunte ao cliente se ele precisará de troco e para qual valor.
   - **PIX:** Envie a chave "CNPJ: 00.000.000/0001-00". Peça o comprovante após o pagamento, mas **NÃO IMPEDA A FINALIZAÇÃO DO PEDIDO** caso o comprovante não seja enviado imediatamente. O pedido pode ser finalizado e o comprovante enviado depois.
   - **Débito/Crédito:** Apenas confirme que aceitamos e prossiga com a finalização.
6. **FINALIZAÇÃO:**
   - Ao ter todos os dados (Itens, Endereço, Pagamento), use a ferramenta `tool_finalizar_pedido`.
   - Apresente o resumo final no formato:
     * 2x Produto X (R$ 0,00) = R$ 0,00
     -------------------------
     💰 TOTAL: R$ 0,00
     📍 Endereço: ...
     🆔 Pedido: #...

Seja educado, prestativo e eficiente.
"""
