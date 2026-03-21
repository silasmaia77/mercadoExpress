from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from src.workflow import tools_mercado, SYSTEM_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()

def get_agent():
    # Usando gpt-4o para máxima inteligência ou gpt-3.5-turbo para economia
    llm = OpenAI(model="gpt-4o", temperature=0) 

    agent = OpenAIAgent.from_tools(
        tools_mercado,
        llm=llm,
        verbose=True,
        system_prompt=SYSTEM_PROMPT
    )
    return agent
