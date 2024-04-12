from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecpersona import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo"
contexto = carrega("dados/banese.txt")

def criar_thread():
    return cliente.beta.threads.create()

def criar_assistente():
    assistente = cliente.beta.assistants.create(
        name="Atendente EcoMart",
        instructions = f"""
                Você é um chatbot de atendimento a clientes de um Banco (Banese). 
                Você não deve responder perguntas que não sejam dados do ecommerce informado!
                Além disso, adote a persona abaixo para respondero ao cliente.
                
                ## Contexto
                {contexto}

                ## Persona
                {personas["neutro"]}
                """,
        model = modelo
    )
    return assistente

