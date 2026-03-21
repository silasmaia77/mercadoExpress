import os
from datetime import datetime
from src.database import buscar_pedidos_quinzena

def gerar_relatorio_txt():
    pedidos = buscar_pedidos_quinzena()
    if not pedidos:
        return "Nenhum pedido encontrado para gerar relatório."

    os.makedirs("data/relatorios", exist_ok=True)
    nome_arquivo = f"data/relatorios/relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

    total_geral = 0.0

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"RELATÓRIO DE VENDAS - {datetime.now().strftime('%d/%m/%Y')}\n")
        f.write("="*50 + "\n\n")

        for p in pedidos:
            # p = (id, nome, tel, end, itens, total, metodo, data)
            f.write(f"Pedido #{p[0]} - {p[1]}\n")
            f.write(f"Data: {p[7]}\n")
            f.write(f"Itens: {p[4]}\n")
            f.write(f"Total: R$ {p[5]:.2f}\n")
            f.write("-" * 30 + "\n")
            total_geral += p[5]

        f.write(f"\nTOTAL GERAL VENDIDO: R$ {total_geral:.2f}")

    return f"Relatório gerado com sucesso: {nome_arquivo}"
