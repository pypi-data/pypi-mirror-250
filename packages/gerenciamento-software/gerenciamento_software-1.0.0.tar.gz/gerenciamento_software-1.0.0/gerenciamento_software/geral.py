from datetime import datetime
from colorama import init, Fore, Back
import os
from hashlib import sha256

init()

# Variaveis De Controle:

parametrosBloqueados = []
gerarLogs = False
estadoConsoleLog = False
caracteresSeparadores = [' ']
palavrasBloqueadas = []
comandosSQLInjection = ['WHERE','FROM','SELECT','CREATE',';','=',"'",'"','`','AND','OR','ALTER','TABLE','GROUP BY','NOT','!','--']


# Verificar String Vazia:
def stringVazia(*strings):
    for item in strings:
        if (len(item)) <=0:
            return False
        else:
            contador = 0
            for letra in range(len(item)):
                if item[letra] == ' ':
                    contador += 1
            
            if contador >= len(item):
                return True
            else:
                return False


# Filtrar Parametros URL Banidos:

    # Adicionando os parametros banidos
def bloquearParametro(*valoresParametro):
    for item in valoresParametro:
        item = item.upper()
        parametrosBloqueados.append(item)

    # Verificando se o parametro esta banido:
def parametroBanido(*valoresParametros):
    for item in valoresParametros:
        item = item.upper()
        if item in parametrosBloqueados:
            return True
    else:
        return False
    

# Validar CPF:


# Criar Log's De Testes:
    
    # Configura o funcionamento do log:
def configLog(criarLogs:bool=False,exibirLogsEmConsole:bool=False):
    global gerarLogs
    global estadoConsoleLog
    gerarLogs = criarLogs
    estadoConsoleLog = exibirLogsEmConsole

    # Retorna o status do Log
def statusLog():
    global gerarLogs
    return gerarLogs

    # Criar um Log
def gerarLog(tipo:str,conteudo:str):
    if gerarLogs == True:
        data_atual = datetime.now()
        data_atual = data_atual.date()
        data_atual = data_atual.strftime("%d-%m-%Y")

        hora_atual = datetime.now()
        hora_atual = hora_atual.time()
        hora_atual = str(hora_atual)
        hora_atual = hora_atual[0:8]

        tipo = tipo.upper()

        conteudo = f'{tipo}: {conteudo} || DATA: {data_atual} || HORA: {hora_atual}\n'
        with open('log.txt', 'a') as arquivo:
            arquivo.write(conteudo)

        if estadoConsoleLog == True:
            os.system("cls")
            print(Fore.RED + conteudo)

        return True
    else:
        print(Fore.RED + "ERRO: Gerar Log está desativado! Para ativar use a função 'ativarLogs(True)'")


# Quebrar frases em palavras separadas:
def quebrarFrase(frase):
    palavras = []
    controle = 0
    tamanhoFrase = len(frase)
    for i in range(tamanhoFrase):
        item = frase[i]
        if ((item in caracteresSeparadores) or (i == (tamanhoFrase-1))):
            if (i == (tamanhoFrase-1)):
                i +=1
            palavra = frase[controle:i]
            palavras.append(palavra)
            controle = i+1

    return palavras


# Anti SQL Injection

    # Verificar se não há códigos SQL num parâmetro:
def antiSQLInjection(parametro):
    parametro = parametro.upper()
    isolados = quebrarFrase(parametro)
    for i in range(len(isolados)):
        if (isolados[i] in comandosSQLInjection) or (isolados[i] in palavrasBloqueadas):
            return [False, 'Parametro potencialmente perigoso']
    else:
        for letra in parametro:
            if (letra in comandosSQLInjection) or (letra in palavrasBloqueadas):
                return [False, 'Parametro potencialmente perigoso']
        else:
            return [True, 'Parametro válido']


    # Bloquear outras palavras além das já bloqueadas:
def bloquearPalavraSQLInjection(*palavra):
    for item in palavra:
        item = item.upper()
        palavrasBloqueadas.append(item)
    return True


# Criptografia

    # Criptografar em SHA256
def criptoToSHA256(arg:str):
    hash = sha256(arg.encode())
    resultado = hash.hexdigest()
    return resultado

    