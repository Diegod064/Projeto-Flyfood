#FlyFood - Algoritmo Genético
#Diego Diniz

import random

taxaDeReproducao = 20
probabilidadeMutacao = 0.05
tamanhoPopulacao = 40
criterioParada = 80

#lendo o arquivo

arq = open('matrizFlyFood3.txt', 'r')

nlinha, ncoluna = map(int, arq.readline().split())

coordenadas = {}
pontos = []

for l in range(nlinha):
    linha = arq.readline().split()
    for c in range(ncoluna):
        if linha[c] != '0':
            pontos.append(linha[c])
            coordenadas[linha[c]] = (l, c)

arq.close()
pontos.remove('R')



#gerar primeira população
def popinicial():
    populacao = []

    for i in range(tamanhoPopulacao):
        pt = pontos * 1
        individuo = []
        for i in range(0, len(pontos)):
            cromossomo = random.randint(0, len(pt) - 1)
            individuo.append(pt[cromossomo])
            pt.remove(pt[cromossomo])
        populacao.append(individuo)

    return populacao


def mov_drone(x1, x2, y1, y2):
    """Soma o movimento do drone"""
    s = abs(x2-x1)+abs(y2-y1)
    return s

def calcdist(p):
    distancia = 0
  
    p = list(p)
    p.insert(0, 'R')
    p.append('R')

    for i in range(len(p)-1):
        distancia += mov_drone(coordenadas[p[i]][0], coordenadas[p[i+1]][0],coordenadas[p[i]][1], coordenadas[p[i+1]][1]) 

    return distancia

def fitness(individuo):
    custo = 0

    individuo.insert(0, 'R')
    individuo.append('R')

    for i in range(len(individuo)-1):
        custo += mov_drone(coordenadas[individuo[i]][0], coordenadas[individuo[i+1]][0],coordenadas[individuo[i]][1], coordenadas[individuo[i+1]][1])

    fit = 1/int(custo)
    del(individuo[0], individuo[-1])

    return fit


def rank(pop):
    populacaoFitness = []
    for p in pop:
        fitList = [p, fitness(p)]
        populacaoFitness.append(fitList)
    populacaoFitness.sort(key=lambda x: x[1], reverse=True)
    return populacaoFitness


def selecao(population):  #seleção por torneio
    vencedores = []
    torneio = []

    for i in range(taxaDeReproducao):
        participantes = random.sample(population, 5)
        for j in participantes:
            torneio.append(j)
        ganhador = rank(torneio)[0][0]
        vencedores.append(ganhador)
    return vencedores


def crossover(pais):
    novaPopulacao = []
    pontoCorte = random.randint(1, len(pontos)-1)
    for i in range(0, len(pais)-1):
        pai1 = pais[i]
        pai2 = pais[i+1]
        filho1 = pai1[0:pontoCorte]+pai2[pontoCorte:len(pai2)]
        filho2 = pai2[0:pontoCorte]+pai1[pontoCorte:len(pai1)]
        filho1 = mutacao(filho1)
        filho2 = mutacao(filho2)
        orgarnizarFilho(pai1, filho1)
        orgarnizarFilho(pai1, filho2)
        novaPopulacao.append(filho1)
        novaPopulacao.append(filho2)

    novaPopulacao = [rank(novaPopulacao)[k][0] for k in range(len(novaPopulacao))]
    
    return novaPopulacao

def mutacao(individuo):  #mutação por swap com 0.05% de chance de ocorrer
    if random.uniform(0.0, 1.0) < probabilidadeMutacao:
        ptMutacao = random.randint(0, len(individuo)-2)
        copia = individuo[ptMutacao]

        individuo[ptMutacao] = individuo[ptMutacao+1]
        individuo[ptMutacao+1] = copia

    return individuo

def orgarnizarFilho(pai, filho):
    # verificação letras faltando e letras repetidas
    letrasRepetidas = [k for k in pai if filho.count(k) > 1]
    letraFaltando = list(set(pai).difference(set(filho)))
    idc = []

    if letrasRepetidas == []:
        return filho
    else:
        for i in range(0, len(letrasRepetidas)):
            c = 0
            for x in range(0, len(filho)):
                if filho[x] == letrasRepetidas[i]:
                    c += 1  # contador para não pegar o primeiro item da lista
                    if c > 1:
                        idc.append(x)

    for j in range(0, len(idc)):
        filho[idc[j]] = letraFaltando[j]
    return filho

def contolePopulacao(populacao, tamanhoPopulacao):

    while len(populacao) > tamanhoPopulacao:
        tam = len(populacao)
        individuo1 = random.randint(0, tam-1)
        individuo2 = random.randint(0, tam-1)
        if individuo1 != individuo2:
            if rank(populacao)[individuo1][1] > rank(populacao)[individuo2][1]:
                populacao.remove(populacao[individuo2])
            else:
                populacao.remove(populacao[individuo1])
        else:
            populacao.remove(populacao[individuo2])

    return populacao

def ag(tamanhoPopulacao, criterioParada):
    populacao = popinicial()

    geracao = 1
    for k in range(criterioParada): # laço que se refere ao numero de iterações

        #selação para fazer crossover
        pais = selecao(populacao)

        novaPopulacao = crossover(pais)
        
        populacao = [rank(populacao + novaPopulacao)[k][0] for k in range(len(populacao + novaPopulacao))]

        #ajustando tamanho da população
        populacao = contolePopulacao(populacao, tamanhoPopulacao)

        geracao += 1

    return rank(populacao)[0]

agn = ag(tamanhoPopulacao, criterioParada)


print('Melhor caminho: ', ' '.join(agn[0]))
print('Distancia em dronômetros: ', calcdist(agn[0]))
