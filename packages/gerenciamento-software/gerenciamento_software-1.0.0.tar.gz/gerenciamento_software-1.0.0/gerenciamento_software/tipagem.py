from geral import gerarLog,statusLog,configLog
from colorama import init, Fore, Back

init()

# Variáveis de controle:

variaveisTipadas = []
tiposPossiveis = ['bool','int','str','float']
constantesCriadas = []

# Verifica o tipo de uma variável e retorna seu tipo:
def verificarTipo(valor):
    tipo = type(valor)
    if tipo == str:
        return 'str'
    elif tipo == int:
        return 'int'
    elif tipo == bool:
        return 'bool'
    elif tipo == float:
        return 'float'


# Declara uma variável de forma tipada:
def declararVariavel(nomeVariavel:str,tipoVariavel:str,valorInicial=None):
    tipoVariavel = tipoVariavel.lower()

    if tipoVariavel in tiposPossiveis:
        if valorInicial == None:
            if tipoVariavel == 'bool':
                valorInicial = False
            elif tipoVariavel == 'str':
                valorInicial = ''
            elif tipoVariavel == 'float':
                valorInicial = 0.0
            elif tipoVariavel == 'int':
                valorInicial = 0

        tipo = verificarTipo(valorInicial)
        
        if tipo == tipoVariavel:
            newVariavel = {'nome':nomeVariavel,'tipo':tipoVariavel,'valor':valorInicial}    
            variaveisTipadas.append(newVariavel)

            return valorInicial
        else:
            erro = f'ERRO: O tipo inicial é "{tipoVariavel}", enquanto o valor inicial é do tipo "{tipo}"'
            print(Fore.YELLOW + erro)
            logAtivado = statusLog()
            if logAtivado == True:
                configLog(criarLogs=True,exibirLogsEmConsole=False)
                gerarLog('CRITICAL',erro)
            return None
    else:
        erro = f'ERRO: Não é possivel usar o tipo "{tipoVariavel}"'
        print(Fore.RED + erro)
        logAtivado == statusLog()
        if logAtivado == True:
            configLog(criarLogs=True,exibirLogsEmConsole=False)
            gerarLog('CRITICAL',erro)
        return None


# Atribuiu um novo valor a uma variável tipada já declarada:
def atribuirValor(nomeVariavel:str, valor):
    for i in range(len(variaveisTipadas)):
        if nomeVariavel == variaveisTipadas[i]['nome']:
            tipoDeclarado = variaveisTipadas[i]['tipo']
            tipoPassado = verificarTipo(valor)
            if tipoDeclarado == tipoPassado:
                variaveisTipadas[i]['valor'] = valor
                return valor
            else:
                erro = f"ERRO: Você está tentando atribuir um valor do tipo '{tipoPassado}' numa variável do tipo '{tipoDeclarado}'"
                print(Fore.YELLOW + erro)
                logAtivado = statusLog()
                if logAtivado == True:
                    configLog(criarLogs=True,exibirLogsEmConsole=False)
                    gerarLog('CRITICAL',erro)
                return None

# Cria uma constante:
def declararCostante(nome:str,valor,tipo:str=None):
    if (len(constantesCriadas)) <=0:
        novaConstante = {'nome':nome,'valor':valor,'tipo':tipo}
        constantesCriadas.append(novaConstante)
        return valor
    else:
        for i in range(len(constantesCriadas)):
            if nome == constantesCriadas[i]['nome']:
                erro = f"Constante {nome} já existe e seu valor não pode ser alterado"
                print(Fore.YELLOW + erro)
                logAtivado = statusLog()
                if logAtivado == True:
                    configLog(criarLogs=True,exibirLogsEmConsole=False)
                    gerarLog('CRITICAL',erro)
                return None
        else:
            novaConstante = {'nome':nome,'valor':valor,'tipo':tipo}
            constantesCriadas.append(novaConstante)
            return valor