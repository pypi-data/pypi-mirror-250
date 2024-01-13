from datetime import datetime
import time
import psutil

def dec_desepenhoExecucao(funcao):
    def wrapper():
        ramInicial = psutil.virtual_memory().used
        tempoInicial = time.time()
        funcao()
        ramFinal = psutil.virtual_memory().used
        tempoFinal = time.time()

        print(f'A Função Executou Em {tempoFinal-tempoInicial} - Segundos')
        print(f'A Função Gastou APROXIMADAMENTE {ramFinal-ramInicial} De Memoria')
    return wrapper