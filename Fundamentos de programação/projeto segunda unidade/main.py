import csv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

TREINOS = []
COMPETICOES = []
meta_km_mes = 10
meta_velocidade = 2

PATH_REGISTROS = "./registros.csv"
PATH_METAS = "./metas.csv"

class Data:
    def __init__(self, str) -> None:
        dia, mes, ano = str.split("/")

        self.dia = int(dia)
        self.mes = int(mes)
        self.ano = int(ano)

    def __str__(self) -> str:
        return f"{self.dia:02}/{self.mes:02}/{self.ano:04}"
    
    def valor(self):
        return self.dia + self.mes * 31 + self.ano * 372
    
    def date_time(self):
        return datetime(self.ano, self.mes, self.dia)
    
    def data_atual():
        # Pega a data atual
        data_atual = datetime.now()

        # Formata a data no formato 'DD/MM/AAAA'
        return Data(data_atual.strftime('%d/%m/%Y'))

class Registro:
    def __init__(self, tipo, data, distancia, tempo, localizacao, clima) -> None:
        self.tipo = tipo
        self.data = Data(data)
        self.distancia = float(distancia)
        self.tempo = float(tempo)
        self.localizacao = localizacao
        self.clima = clima

    def array(self):
        return [
            self.tipo,
            self.data.__str__(),
            self.distancia,
            self.tempo,
            self.localizacao,
            self.clima
        ]
    
    def __str__(self) -> str:
        return f"{self.tipo:^10} | {self.data.__str__():^10} | {f'{self.distancia} km':^10} | {f'{self.tempo} mins':^12} | {self.localizacao:^16} | {self.clima:^15}"

def add_registro(reg, tipo):
    global COMPETICOES, TREINOS

    if tipo == "Treino":
        TREINOS.append(reg)
    else:
        COMPETICOES.append(reg)

def filtrar(valor, modo, tipo):
    global COMPETICOES, TREINOS

    filtrados = []

    if tipo == "Treino":
        data = TREINOS
    else:
        data = COMPETICOES

    for r in data:
        if float(getattr(r, modo)) >= float(valor):
            filtrados.append(r)

    return filtrados

def filtrar_tempo(tempo, tipo):
    return filtrar(tempo, "tempo", tipo)

def filtrar_distancia(dist, tipo):
    return filtrar(dist, "distancia", tipo)

def estatisticas_treinos():
    global TREINOS

    media_dist = 0
    media_tempo = 0

    if not TREINOS:
        return 5, 30

    for r in TREINOS:
        media_dist += r.distancia
        media_tempo += r.tempo

    media_dist /= len(TREINOS)
    media_tempo /= len(TREINOS)

    return media_dist, media_tempo

def sugerir_treino():
    import random
    media_d, media_t = estatisticas_treinos()

    delta_d = media_d / 4
    delta_t = media_t / 4

    registro_data = [
    "Treino",
    Data.data_atual().__str__(),
    round(random.random() * delta_d - delta_d / 2 + media_d, 2),
    round(random.random() * delta_t - delta_t / 2 + media_t, 2),
    TREINOS[-1].localizacao if TREINOS else "Recife",
    "Não definido"
    ]

    return Registro(*registro_data)

def registros_ultimo_mes():
    global TREINOS

    data_atual = Data.data_atual()

    registros_mes = []

    for r in TREINOS:
        if r.data.ano != data_atual.ano or r.data.mes != data_atual.mes:
            continue

        registros_mes.append(r)

    return registros_mes

def distancia_mes(registros_mes):
    global meta_km_mes

    distancia_total = 0
    
    for r in registros_mes:
        distancia_total += r.distancia

    return distancia_total

def verificar_meta_velocidade(registros_mes):
    global meta_velocidade

    classificados = []
    
    for r in registros_mes:
        velocidade = r.distancia / r.tempo * 60
        classificados.append([r, velocidade >= meta_velocidade])

    return classificados

def load_data():
    global PATH_REGISTROS, PATH_METAS, TREINOS, COMPETICOES, meta_km_mes, meta_velocidade

    if os.path.exists(PATH_REGISTROS):
        with open(PATH_REGISTROS, "r", newline="", encoding="utf8") as arquivo:
            tabela = csv.reader(arquivo)

            for linha in tabela:
                registro = Registro(*linha)

                if registro.tipo == "Treino":
                    TREINOS.append(registro)
                else:
                    COMPETICOES.append(registro)

    if os.path.exists(PATH_METAS):
        with open(PATH_METAS, "r", newline="", encoding="utf8") as arquivo:
            tabela = csv.reader(arquivo)

            primeira_linha = next(tabela)
            segunda_linha = next(tabela)

            meta_km_mes = float(primeira_linha[0])
            meta_velocidade = float(segunda_linha[0])

def ordenar_data(arr):
    arr.sort(key = lambda x: x.data.valor())

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def grafico(reg):
    # Ordena os registros por data
    ordenar_data(reg)
    
    # Criando uma lista de objetos datetime a partir dos atributos dia, mes e ano
    x = [r.data.date_time() for r in reg]
    y_velocidade = [r.distancia / r.tempo * 60 for r in reg]  # Velocidade média em km/h
    y_distancia = [r.distancia for r in reg]  # Distância de cada treino
    y_tempo = [r.tempo for r in reg]  # Tempo de cada treino

    # Criando o gráfico para velocidade
    plt.plot(x, y_velocidade, marker='o', linestyle='-', color='b', label='Velocidade (km/h)')
    
    # Criando o gráfico para distância
    plt.plot(x, y_distancia, marker='x', linestyle='--', color='g', label='Distância (km)')
    
    # Criando o gráfico para tempo
    plt.plot(x, y_tempo, marker='^', linestyle='-.', color='r', label='Tempo (min)')

    # Adicionando título e rótulos aos eixos
    plt.title("Evolução do Desempenho nos Treinos")
    plt.xlabel('Data')
    plt.ylabel('Valores')

    # Formatando o eixo x para mostrar as datas no formato dd/mm
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # Marca por dia
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))  # Formato: dia/mês
    
    # Rotacionando os labels para facilitar a leitura
    plt.xticks(rotation=45)

    # Adicionando o local e clima para cada ponto
    for i, r in enumerate(reg):
        local = r.localizacao  # Supondo que o local esteja no atributo `local`
        clima = r.clima  # Supondo que o clima esteja no atributo `clima`
        # Adiciona texto no gráfico próximo ao ponto
        plt.text(x[i], y_velocidade[i], f"{local}, {clima}", fontsize=8, ha='right', va='bottom')

    # Exibindo a legenda
    plt.legend()

    # Exibindo o gráfico
    plt.tight_layout()  # Ajusta o layout para não cortar as labels
    plt.show()

def save_data():
    global PATH_REGISTROS, PATH_METAS, TREINOS, COMPETICOES, meta_km_mes, meta_velocidade

    dados = []

    if TREINOS:
        for t in TREINOS:
            dados.append(t.array())

    if COMPETICOES:
        for c in COMPETICOES:
            dados.append(c.array())

    with open(PATH_REGISTROS, "w", newline="", encoding="utf8") as arquivo:
        escritor = csv.writer(arquivo)

        escritor.writerows(dados)

    dados = [
        [meta_km_mes],
        [meta_velocidade]
    ]

    with open(PATH_METAS, "w", newline="", encoding="utf8") as arquivo:
        escritor = csv.writer(arquivo)

        escritor.writerows(dados)

def indice_valido(list, idx):
    if not is_int(idx): return False
    idx = int(idx) - 1
    return idx >= 0 and idx < len(list)

def conteudo(tipo):
    global TREINOS, COMPETICOES

    return len(TREINOS) if tipo == "Treino" else len(COMPETICOES)

def atualizar_registro(tipo, idx, reg):
    global TREINOS, COMPETICOES
    
    if tipo == "Treino":
        TREINOS[idx] = reg
    else:
        COMPETICOES[idx] = reg

def excluir_reg(tipo, idx):
    global TREINOS, COMPETICOES
    
    if tipo == "Treino":
        TREINOS.pop(idx)
    else:
        COMPETICOES.pop(idx)

def mostrar_treinos(reg):
    if not reg:
        input("Não há registros para mostrar")
        return
    print("\nLista de Treinos/Competições:")
    print("| Índice |   Tipo    |    Data    | Distância  |   Duração    |    Localização   |      Clima     |")
    print("-" * 99)
    for i, r in enumerate(reg):
        print(f"| {i + 1:^6} |", r, "|", sep="")

def mostrar_metas(reg):
    print("\nAcompanhamento de Metas:")
    print("| Índice |   Tipo    |    Data    | Distância  |   Duração    |    Localização   |      Clima     |  Meta da velocidade  |")
    print("-" * 120)
    for i, reg in enumerate(reg):
        r, m = reg
        print(f"| {i + 1:^6} |", r, "|", f"{str('Alcançada'):^22}|" if m else f"{str('Não alcançada'):^22}|", sep="")

def is_float(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def is_int(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

def criar_registro_input(tipo):
    os.system("cls")
    print(f"\nCriando novo registro de {tipo.lower()}...\n")

    while True:
        dia = input("Dia: ")
        if is_int(dia) and 0 < int(dia) < 32: break
        print("O dia deve ser um número entre 1 - 31")
    while True:
        mes = input("Mês: ")
        if is_int(mes) and 0 < int(mes) < 13: break
        print("O mês deve ser um número entre 1 - 12")
    while True:
        ano = input("Ano: ")
        if is_int(ano) and int(ano) > 0: break
        print("O ano deve ser um número maior que 0")
    data = f"{int(dia):02}/{int(mes):02}/{int(ano):04}"
    while True:
        distancia = input("Distância em quilômetros: ")
        if is_float(distancia) and float(distancia) > 0: break
        print("A distância deve ser um número")
    while True:
        tempo = input("Duração do treino em minutos: ")
        if is_float(tempo) and float(tempo) > 0: break
        print("O tempo deve ser um número")
    while True:
        localizacao = input("Localização do treino: ")
        if localizacao: break
        print("A localização deve conter um valor")
    while True:
        clima = input("Clima: ")
        if clima: break
        print("O clima deve conter um valor")

    registro = Registro(tipo, data, float(distancia), float(tempo), localizacao, clima)

    print(f"\n{tipo} adicionado com sucesso!\n")

    return registro

def filtrar_dist_input(tipo):
    os.system("cls")
    if not conteudo(tipo):
        print("Não há conteúdo para filtrar ")
        input("Pressione enter para sair")
        return
    while True:
        dist = input("Digite a distância em km para ser buscada: ")
        if is_float(dist) and float(dist) > 0:
            dist = float(dist)
            break
        print("A distância deve ser um número maior que 0")

    filtrados = filtrar_distancia(dist, tipo)

    if filtrados:
        mostrar_treinos(filtrados)
    else:
        print("Treino não encontrado")

    input("Aperte enter para voltar ao Menu")

def filtrar_tempo_input(tipo):
    os.system("cls")
    if not conteudo(tipo):
        print("Não há conteúdo para fitrar ")
        input("Pressione enter para sair")
        return
    while True:
        tempo = input("Digite a duração do treino para ser buscado: ")
        if is_float(tempo) and float(tempo) > 0: 
            tempo = float(tempo)
            break
        print("A duração deve ser um número maior que 0")

    filtrados = filtrar_tempo(tempo, tipo)

    if filtrados:
        mostrar_treinos(filtrados)
    else:
        print("Treino não encontrado")

    input("Aperte enter para voltar ao Menu")

def excluir_reg_input(tipo):
    global TREINOS, COMPETICOES
    os.system("cls")
    if not conteudo(tipo):
        print("Não há conteúdo para excluir ")
        input("Pressione enter para sair")
        return
    
    mostrar_treinos(TREINOS if tipo == "Treino" else COMPETICOES)
    while True:
        idx = input("Índice a ser excluido: ")

        if indice_valido(TREINOS if tipo == "Treino" else COMPETICOES, idx):
            break
        print("Índice inválido")

    excluir_reg(tipo, int(idx) - 1)

    input("Pressione enter para sair")

def atualizar_reg_input(tipo):
    global TREINOS, COMPETICOES
    os.system("cls")
    if not conteudo(tipo):
        print("Não há conteúdo para atualizar ")
        input("Pressione enter para sair")
        return
    
    mostrar_treinos(TREINOS if tipo == "Treino" else COMPETICOES)
    while True:
        idx = input("Índice a ser modificado: ")

        if indice_valido(TREINOS if tipo == "Treino" else COMPETICOES, idx):
            break
        print("Índice inválido")

    reg = criar_registro_input(tipo)
    atualizar_registro(tipo, int(idx) - 1, reg)

    input("Pressione enter para sair")

def visualizar_reg(tipo):
    os.system("cls")
    print(f"\nMenu de Visualização de {tipo}/s\n")
    print(
f"""
1 - Mostrar {tipo}s
2 - Filtrar por distância
3 - Filtrar por tempo
0 - Voltar ao menu anterior
"""
    )
        
    modo = input("Escolha uma opção: ")

    if modo == "1":
        mostrar_treinos(TREINOS if tipo == "Treino" else COMPETICOES)
        input("Aperte enter para voltar ao Menu")
    elif modo == "2":
        filtrar_dist_input(tipo)
    elif modo == "3":
        filtrar_tempo_input(tipo)
    elif modo == "0":
        return
    else:
        print("Valor inválido, digite um número entre 0 - 3")
        input("Digite algo para continuar")
        visualizar_reg(tipo)

def treinos_input():
    os.system("cls")
    print("\nMenu de Treinos\n")
    print(
f"""
1 - Adicionar treino
2 - Visualizar treinos
3 - Atualizar treino
4 - Excluir treino
0 - Voltar ao menu principal
"""
    )

    modo = input("Escolha uma opção: ")

    if modo == "1":
        reg = criar_registro_input("Treino")
        add_registro(reg, "Treino")
        return
    elif modo == "2":
        visualizar_reg("Treino")
        return
    elif modo == "3":
        atualizar_reg_input("Treino")
        return
    elif modo == "4":
        excluir_reg_input("Treino")
        return
    elif modo == "0":
        return
    else:
        print("Valor inválido, digite um número entre 0 - 4")
        input("Digite algo para continuar")
        treinos_input()

def competicoes_input():
    os.system("cls")
    print("\nMenu de Competições\n")
    print(
f"""
1 - Adicionar competição
2 - Visualizar competições
3 - Atualizar competição
4 - Excluir competição
0 - Voltar ao menu principal
"""
    )

    modo = input("Escolha uma opção: ")

    if modo == "1":
        reg = criar_registro_input("Competição")
        add_registro(reg, "Competição")
        return
    elif modo == "2":
        visualizar_reg("Competição")
        return
    elif modo == "3":
        atualizar_reg_input("Competição")
        return
    elif modo == "4":
        excluir_reg_input("Competição")
        return
    elif modo == "0":
        return
    else:
        print("Valor inválido, digite um número entre 0 - 4")
        input("Digite algo para continuar")
        competicoes_input()

def atualizar_meta_input():
    global meta_km_mes, meta_velocidade
    os.system("cls")

    print(
f"""
1 - Meta distância por mês
2 - Meta velocidade por treino
0 - Menu
"""
    )

    modo = input()

    if modo == "1":
        while True:
            meta_km_mes = input("Meta de quilômetros mensal: ")
            if is_float(meta_km_mes) and float(meta_km_mes) > 0: 
                meta_km_mes = float(meta_km_mes)
                return
            print("A meta deve ser um número maior que 0")
    elif modo == "2":
        while True:
            meta_velocidade = input("Meta de velocidade por treino: ")
            if is_float(meta_velocidade) and float(meta_velocidade) > 0:
                meta_velocidade = float(meta_velocidade)
                return
            print("A meta deve ser um número maior que 0")
    elif modo == "0":
        return
    else:
        print("Valor inválido, digite um número entre 0 - 3")
        input("Digite algo para continuar")
        atualizar_meta_input()

def acompanhar_meta_input():
    global meta_km_mes, meta_velocidade
    os.system("cls")
    
    registros_mes = registros_ultimo_mes()

    meta_velocidade_treino = verificar_meta_velocidade(registros_mes)

    mostrar_metas(meta_velocidade_treino)

    print(f"\nMeta de velocidade média: {meta_velocidade} km / h")

    distancia_m = distancia_mes(registros_mes)

    print(f"Meta de distância por mês: {meta_km_mes:.2f} km")

    print(f"\nDistância total percorrida: {distancia_m:.2f} km")

    if distancia_m < meta_km_mes:
        print("Meta ainda não alcançada")
    else:
        print("Meta de distância mensal alcançada!")

    input("Aperte enter para voltar ao Menu")

def metas_input():
    os.system("cls")
    print("\nMenu de Metas\n")
    print(
f"""
1 - Atualizar metas
2 - Acompanhar meta mensal
0 - Voltar ao menu principal
"""
    )

    modo = input("Escolha uma opção: ")

    if modo == "1":
        atualizar_meta_input()
        return
    elif modo == "2":
        acompanhar_meta_input()
        return
    elif modo == "0":
        return
    else:
        print("Valor inválido, digite um número entre 0 - 2")
        input("Digite algo para continuar")
        metas_input()

def sugerir_treino_input():
    os.system("cls")
    treino = sugerir_treino()

    print("="*50)
    print("   Sugestão de Treino Baseada no Seu Histórico")
    print("="*50)

    print("\nCom base no seu desempenho anterior, aqui está o treino sugerido para você:\n")
    print(f"{treino}\n")

    print("="*50)
    input("Pressione Enter para voltar ao menu...")
    print("="*50)

def grafico_input():
    os.system("cls")

    print("="*50)
    print("   Gráfico de Desempenho dos Treinos - Mês Atual")
    print("="*50)

    print("\nEste gráfico irá mostrar a evolução do seu desempenho nos treinos ao longo do mês.\n")
    print("Pressione qualquer tecla para gerar o gráfico...\n")
    
    input()

    registros_mes = registros_ultimo_mes()

    if registros_mes:
        grafico(registros_mes)  
    else:
        print("Este mês ainda não possui treinos")

    print("\n" + "="*50)
    input("Pressione Enter para voltar ao menu...")
    print("="*50)

def main():
    save_data()
    os.system("cls")
    print("\nBem-vindo ao Gerenciador de Treinos e Competições\n")
    print(
f"""
Escolha um modo:

1 - Treinos
2 - Competições
3 - Metas
4 - Sugestões de Treino
5 - Gráfico de desempenho
6 - Sair
"""
    )

    modo = input("Escolha uma opção: ")

    if modo == "1":
        treinos_input()
        return
    elif modo == "2":
        competicoes_input()
        return
    elif modo == "3":
        metas_input()
        return
    elif modo == "4":
        sugerir_treino_input()
        return
    elif modo == "5":
        grafico_input()
        return
    elif modo == "6":
        print("Saindo... Até mais!")
        save_data()
        exit()
    else:
        print("Valor inválido")
        input("Digite algo para continuar")
        main()

if __name__ == "__main__":
    load_data()

    while True:
        main()
