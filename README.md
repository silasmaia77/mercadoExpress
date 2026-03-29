# 🛒 Mercado Express Bot - Agente Autônomo de IA para WhatsApp

## 📌 Descrição
O **Mercado Express Bot** é um agente autônomo de Inteligência Artificial desenvolvido para automatizar e escalar o atendimento e as vendas de mercados, mercearias e conveniências via WhatsApp. 

Diferente de chatbots tradicionais de menu, este sistema utiliza **IA Generativa (OpenAI)** orquestrada pelo framework **LlamaIndex**, permitindo que o bot converse de forma natural, consulte preços em tempo real em uma planilha Excel, gerencie um carrinho de compras e finalize pedidos de forma 100% autônoma.

## 🎥 Demonstração
Assista ao vídeo do bot em funcionamento, demonstrando o fluxo completo de atendimento, consulta de catálogo e finalização de pedidos com notificação para a equipe:

▶️ **[Assistir Demonstração no YouTube](https://www.youtube.com/watch?v=vs3tprnz5y0&t=41s)**

## 🎯 Problema que resolve
Estabelecimentos do varejo alimentar frequentemente enfrentam:
* Alto volume de mensagens de clientes perguntando preços e disponibilidade.
* Demora no atendimento em horários de pico, gerando desistência e vendas perdidas.
* Erros manuais na anotação de pedidos, itens e endereços de entrega.
* Falta de comunicação rápida entre o atendimento e a equipe de separação (logística).

Este agente atua como um funcionário incansável que atende, vende e coordena a equipe 24 horas por dia, resolvendo esses gargalos de forma escalável.

## ⚙️ Funcionalidades Principais
* **Atendimento Humanizado:** Conversa fluida e natural, guiada por um *System Prompt* rigoroso que mantém a IA focada em vendas.
* **Consulta de Catálogo (Excel):** O bot possui uma ferramenta (`FunctionTool`) que lê uma planilha Excel em tempo real para informar preços e disponibilidade exatos aos clientes.
* **Gestão de Carrinho e Pagamentos:** Memoriza os itens solicitados e gerencia opções de pagamento (Dinheiro com troco, PIX, Cartões).
* **Notificação de Logística:** Ao finalizar um pedido, o bot salva os dados no banco, gera um cupom TXT e **dispara um alerta automático para o grupo de WhatsApp da equipe de separação**.
* **Processamento Assíncrono:** Arquitetura robusta baseada em filas (Redis) para suportar múltiplos clientes simultâneos sem travar.

## 🧰 Tecnologias Utilizadas
* **Linguagem:** Python 3
* **Orquestração de IA:** LlamaIndex (Agents & Tools)
* **LLM:** OpenAI API (Modelos GPT)
* **Mensageria:** WAHA (WhatsApp HTTP API)
* **Fila de Processamento:** Redis
* **Banco de Dados:** SQLite
* **Leitura de Dados:** Pandas / Openpyxl (Integração Excel)
* **Infraestrutura:** Docker & Docker Compose

## 🏗️ Arquitetura do Sistema
O projeto é estruturado em microsserviços rodando em contêineres Docker:
1. **WAHA:** Motor que conecta com o WhatsApp, recebe mensagens e envia via Webhook.
2. **API (Flask):** Porta de entrada de segurança que recebe o Webhook, valida tokens e enfileira a mensagem.
3. **Redis:** Gerencia a fila de mensagens (`queue:incoming`) garantindo que nenhuma requisição se perca.
4. **Worker (LlamaIndex):** O "cérebro" do sistema. Consome a fila, aciona o Agente OpenAI, decide quais ferramentas usar (Excel/DB) e devolve a resposta ao cliente.

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
* Docker e Docker Compose instalados na máquina.
* Uma chave de API válida da OpenAI.
* Uma planilha de produtos configurada na pasta do projeto.

### 2. Instalação e Configuração
Clone o repositório para a sua máquina:
```bash
git clone https://github.com/silasmaia77/mercadoExpress.git
cd mercado-express-bot
```

Crie o arquivo de variáveis de ambiente (`.env`) na raiz do projeto e preencha com suas credenciais:
```env
OPENAI_API_KEY=sk-proj-sua-chave-aqui
WEBHOOK_TOKEN=sua-senha-de-seguranca-aqui
GROUP_ID=1234567890@g.us # ID do grupo de logística no WhatsApp
```

### 3. Subindo a Infraestrutura
Execute o comando abaixo para construir as imagens e iniciar todos os serviços em segundo plano:
```bash
docker-compose up -d --build
```

### 4. Conectando o WhatsApp
1. Abra o navegador e acesse o painel do WAHA: **http://localhost:3100**
2. Verifique se a sessão `default` está com o status `WORKING`.
3. Caso seja o primeiro acesso, clique em "Play" e leia o QR Code com o WhatsApp que será usado como bot.
4. O sistema já estará pronto para receber mensagens e vender!