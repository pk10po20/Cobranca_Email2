def extrair_codigos(contas_receber):
    """
    Extrai apenas os códigos de cliente e lançamento das contas a receber
    Retorna uma lista de dicionários com os pares de códigos
    """
    codigos = []
    
    # Verificar se estamos recebendo os dados
    print("Dados recebidos da API:", contas_receber)
    
    # Verificar se a chave existe e tem conteúdo
    conta_receber_cadastro = contas_receber.get("conta_receber_cadastro", [])
    print(f"Número de registros encontrados: {len(conta_receber_cadastro)}")
    
    for conta in conta_receber_cadastro:
        codigo_cliente = conta.get("codigo_cliente_fornecedor")
        codigo_lancamento = conta.get("codigo_lancamento_omie")
        
        # Verificar se os códigos foram encontrados
        print(f"Código cliente: {codigo_cliente}, Código lançamento: {codigo_lancamento}")
        
        if codigo_cliente and codigo_lancamento:
            par_codigos = {
                'codigo_cliente_fornecedor': codigo_cliente,
                'codigo_lancamento_omie': codigo_lancamento
            }
            codigos.append(par_codigos)
    
    # Verificar o resultado final
    print(f"Total de códigos extraídos: {len(codigos)}")
    return codigos

def salvar_codigos(codigos, nome_arquivo='codigos_extraidos.json'):
    """
    Salva os códigos em um arquivo JSON
    """
    import json
    from datetime import datetime
    
    dados_para_salvar = {
        'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'codigos': codigos
    }
    
    # Verificar os dados antes de salvar
    print("Dados que serão salvos:", dados_para_salvar)
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_para_salvar, f, indent=4) 