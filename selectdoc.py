from openai import *
from dotenv import *
import os
from time import *
from helpers import *

load_dotenv()

cliente = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo"


dados_banese = carrega("dados\dados.txt")
politicas_banese = carrega("dados\políticas_banese.txt")
produtos_banese = carrega("dados\_funcoes_banese.txt")

def selecionar_documentos(resposta_openai):
    if "políticas" in resposta_openai:
        return dados_banese + "\n" + politicas_banese
    elif "produtos" in resposta_openai:
        return dados_banese + "\n" + produtos_banese
    else:
        return dados_banese

def selecionar_contexto(mensagem_usuario):
    prompt_sistema = f"""
    O banco Banese tem três documentos principais, dois deles é explicando sobre o banese e as funcionalidades do chatbot enquanto o outro é um arquivo de texto com uns dados dos usuários:
    
        #Documento n1 "\n {dados_banese}"\n"
        #Documento n2 "\n" {politicas_banese} "\n"
        #Documento n3 "\n" {produtos_banese} "\n"
        
    Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta.
    Utilize o Documento 1 para responder perguntas sobre o usuário, exemplo ele saber se ele posssui dividas ou fundos de investimentos, caso o usuário 
    queira saber sobre as políticas do banco retorne o Documento 2 e se ele quiser saber sobre os produtos/ serviços do banese retorne o Documento 3
    
    
    Você pode pegar os dados como se há dividas e se a pessoa fez investimento, lendo o arquivo n1 e analisando o arquivo
    n1.
    """
    
    resposta = cliente.chat.completions.create(
        model = modelo,
        messages = [
            {
                "role" : "system",
                "content": prompt_sistema
            },
            {
                "role" : "user",
                "content": mensagem_usuario
            }
        ],
        temperature = 1,
    )
    
    contexto = resposta.choices[0].message.content.lower()
    return contexto