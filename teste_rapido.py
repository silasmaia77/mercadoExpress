from src.agent import get_agent

try:
    agent = get_agent()
    print("✅ Agente carregado com sucesso!")
    response = agent.chat("Oi, qual seu nome?")
    print(f"🤖 Resposta: {response}")
except Exception as e:
    print(f"❌ Erro: {e}")
