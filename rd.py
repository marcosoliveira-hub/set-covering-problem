# Trabalho sobre o problema de cobertura de conjuntos (Set Covering Problem)
# Guilherme Frare Clemente - RA: 124349

# Modelagem e Otimização de Algoritmos 

from copy import deepcopy
import math, random
from math import inf
from functools import cmp_to_key

class Coluna:
    def __init__(self, indice: int, custo: float, linhascobertas: set[int]):
        self.indice = indice
        self.custo = custo
        self.linhascobertas = linhascobertas

class Dados:
    def __init__(self, nlinhas: int, ncolunas: int, colunas: list[Coluna]):
        self.nlinhas = nlinhas
        self.ncolunas = ncolunas
        self.colunas = colunas


funcoes_de_custo = [
        lambda cj, kj : cj,
        lambda cj, kj : cj/kj,
        lambda cj, kj : cj/math.log2(kj) if math.log2(kj) != 0 else inf,
        lambda cj, kj : cj/(kj*math.log2(kj)) if (kj*math.log2(kj)) != 0 else inf,
        lambda cj, kj : cj/(kj*math.log(kj)) if kj*math.log(kj) != 0 else inf,
        lambda cj, kj : cj/(kj*kj),
        lambda cj, kj : cj**(1/2)/(kj*kj)]

def ler_arquivo(arq: str) -> Dados:

    with open(arq, 'r') as f:
        linhas = f.readlines()


    nmr_linhas = int(linhas[0].split()[1])
    nmr_colunas = int(linhas[1].split()[1])

    dados = []
    for linha in linhas[3:]:

        elementos = linha.split()
        indice = int(elementos[0])
        custo = float(elementos[1])
        linhas_cobertas = [int(x) for x in elementos[2:]]
        dado = Coluna(indice, custo, linhas_cobertas)
        dados.append(dado)

    return Dados(nmr_linhas, nmr_colunas, dados)


def funcao_aleatoria(custo: float, kj: int) -> float:
    return random.choice(funcoes_de_custo)(custo, kj)


def remove_colunas_redundantes(S, dados):
    T = S.copy()
    wi = [sum(1 for j in S if i in dados.colunas[j].linhascobertas) for i in range(1, dados.nlinhas+1)]
    while T:
        j = random.choice(list(T))
        T.remove(j)
        Bj = dados.colunas[j].linhascobertas
        if all(wi[i-1] >= 2 for i in Bj):
            S.remove(j)
            for i in Bj:
                wi[i-1] -= 1
    return S
    

def construtivo(dados):

    solucao = set()
    R = set(range(1, dados.nlinhas+1))

    Pj = [set() for _ in range(dados.ncolunas)]
    for j, coluna in enumerate(dados.colunas):
        Pj[j] = set(coluna.linhascobertas)

    
    while R != set():
        num_linhas_cobertas_por_coluna = [len(R.intersection(pj)) for pj in Pj]
        J = min(range(dados.ncolunas), key=lambda j: funcao_aleatoria(dados.colunas[j].custo, num_linhas_cobertas_por_coluna[j]) if num_linhas_cobertas_por_coluna[j] > 0 else float('inf'))

        R = R.difference(Pj[J])
        solucao.add(J)

    
    solucao = sorted(solucao, key=lambda j: dados.colunas[j].custo, reverse=True)

    for i in solucao:
        if set.union(*[Pj[j] for j in solucao if j != i]) == set(range(1, dados.nlinhas+1)):
            solucao.remove(i)

    solucao = remove_colunas_redundantes(solucao, dados)

    assert valid_solution(solucao, dados)
    
    custo = sum([dados.colunas[j].custo for j in solucao])
    
    return solucao, custo
   

def construtivo2(dados):
    pass


def melhoramento(solucao, dados):
    
    d = 0
    D = math.ceil(random.uniform(0.05, 0.7) * len(solucao[0]))
    E = math.ceil(random.uniform(1.1, 2) * max(dados.colunas[j].custo for j in solucao[0]))
    wi = [sum(1 for j in solucao[0] if i in dados.colunas[j].linhascobertas) for i in range(1, dados.nlinhas+1)]
    colunas_fora_da_solucao = set(range(dados.ncolunas)).difference(solucao[0])

    while d < D:
        k = random.choice(solucao[0])
        solucao[0].remove(k)
        colunas_fora_da_solucao.add(k)

        for i in dados.colunas[k].linhascobertas:
            wi[i-1] -= 1
        d += 1
    
    # define U as the set of rows for which wi = 0
    U = set(i for i in range(1, dados.nlinhas+1) if wi[i-1] == 0)

    while U != set() and 0 in wi:
        #Define Re as the set of columns for which cj <= E | j belonging to colunas_fora_da_solucao
        Re = set(j for j in colunas_fora_da_solucao if dados.colunas[j].custo <= E)
        alpha_ij = [1 if i in U and all(i in dados.colunas[j].linhascobertas for j in Re) else 0 for i in range(1, dados.nlinhas+1)]
        alpha_j = [sum(alpha_ij[i-1] for i in dados.colunas[j].linhascobertas) for j in Re]
        
        if not Re:
            break

        beta_j = [dados.colunas[j].custo/alpha_j[i] if alpha_j[i] != 0 else inf for i, j in enumerate(Re)]
        bmin = min(beta_j)
        Re_list = list(Re)
        K = set(j for j in Re if beta_j[Re_list.index(j)] == bmin)

        j = random.choice(list(K))
        colunas_fora_da_solucao.remove(j)
        solucao[0].append(j)

        for i in dados.colunas[k].linhascobertas:
            wi[i-1] += 1

        U = set(i for i in range(1, dados.nlinhas+1) if wi[i-1] == 0)
    

    for k in reversed(solucao[0]):
        if all(wi[i-1] >= 1 for i in dados.colunas[k].linhascobertas):
            solucao[0].remove(k)
            colunas_fora_da_solucao.add(k)
            for i in dados.colunas[k].linhascobertas:
                wi[i-1] -= 1

    while not valid_solution(solucao[0], dados):
        for j in range(dados.ncolunas):
            if j not in solucao[0] and any(i in dados.colunas[j].linhascobertas for i in range(1, dados.nlinhas + 1)):
                solucao[0].append(j)
                break
    
    solucao = list(solucao)
    solucao[0] = remove_colunas_redundantes(solucao[0], dados)
    solucao[1] = sum([dados.colunas[j].custo for j in solucao[0]])
    solucao = tuple(solucao)

    assert valid_solution(solucao[0], dados)

    return solucao



def valid_solution(solucao, dados):
    rows = [False for _ in range(dados.nlinhas)]

    for c in solucao:
        for r in dados.colunas[c].linhascobertas:
            rows[r-1] = True

    return all(f for f in rows)


def main():
    arq = ler_arquivo('test1.txt')
    # solucao1, custo = construtivo(arq)
    # solucao = (solucao1, custo)
    # for _ in range(1000):
    #     solucao = melhoramento(solucao, arq)
    #     if solucao[1] < custo:
    #         custo = solucao[1]
    #         solucao1 = deepcopy(solucao[0])
    #         print(custo)
    
    # print(solucao1, custo)
    print(construtivo(arq))
    #print(melhoramento(teste, arq))


if __name__ == '__main__':
    main()