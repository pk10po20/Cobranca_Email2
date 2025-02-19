import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from ProcessarCodigos import extrair_codigos, salvar_codigos

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

OMIE_API_URL = "https://app.omie.com.br/api/v1/"
OMIE_APP_KEY = os.getenv("OMIE_APP_KEY")
OMIE_APP_SECRET = os.getenv("OMIE_APP_SECRET")
MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY")
MAILCHIMP_LIST_ID = os.getenv("MAILCHIMP_LIST_ID")
MAILCHIMP_DC = MAILCHIMP_API_KEY.split('-')[-1]

def listar_contas_receber():
    url = f"{OMIE_API_URL}financas/contareceber/"
    payload = {
        "call": "ListarContasReceber",
        "app_key": OMIE_APP_KEY,
        "app_secret": OMIE_APP_SECRET,
        "param": [{
            "pagina": 1,
            "registros_por_pagina": 500,
            "apenas_importado_api": "N",
            "filtrar_por_status": "VENCEHOJE"
        }]
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    print("Debug: Resposta da API Omie")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    
    return data

def obter_cliente(codigo_cliente):
    url = f"{OMIE_API_URL}geral/clientes/"
    payload = {
        "call": "ConsultarCliente",
        "app_key": OMIE_APP_KEY,
        "app_secret": OMIE_APP_SECRET,
        "param": [{
            "codigo_cliente_omie": codigo_cliente
        }]
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def obter_boleto(codigo_lancamento_omie):
    url = f"{OMIE_API_URL}financas/contareceberboleto/"
    payload = {
        "call": "ObterBoleto",
        "app_key": OMIE_APP_KEY,
        "app_secret": OMIE_APP_SECRET,
        "param": [{
            "nCodTitulo": codigo_lancamento_omie
        }]
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def processar_contas_receber():
    # 1. Listar contas a receber do dia
    contas_receber = listar_contas_receber()
    
    # Verificar a resposta da API
    print("Status da resposta da API:")
    print(f"Total de registros: {contas_receber.get('total_de_registros', 0)}")
    print(f"Página atual: {contas_receber.get('pagina', 0)}")
    
    # Extrair e salvar os códigos
    codigos = extrair_codigos(contas_receber)
    
    # Verificar se foram extraídos códigos
    if not codigos:
        print("AVISO: Nenhum código foi extraído!")
    
    salvar_codigos(codigos)
    
    # Continua com o processamento normal
    for conta in contas_receber.get("conta_receber_cadastro", []):
        # 2. Obter informações do cliente
        codigo_cliente = conta.get("codigo_cliente_fornecedor")
        cliente = obter_cliente(codigo_cliente)
        email_cliente = cliente.get("email")
        
        # 3. Obter boleto
        codigo_lancamento = conta.get("codigo_lancamento_omie")
        boleto = obter_boleto(codigo_lancamento)
        
        print(f"Cliente: {cliente.get('razao_social')}")
        print(f"CNPJ/CPF: {cliente.get('cnpj_cpf')}")
        print(f"Email: {email_cliente}")
        print(f"Valor: R$ {conta.get('valor')}")
        print(f"Boleto: {boleto.get('url_boleto', 'Não disponível')}")
        print("-" * 50)

if __name__ == "__main__":
    processar_contas_receber()