#FlyFood - Algoritmo de força bruta
#Diego Diniz

from itertools import permutations
from time import time

inicio = time()

#lendo o arquivo

arq = open('matrizFlyFood5.txt', 'r')

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

#permutação e soma dos pontos

pontos.remove('R')
permut = list(permutations(pontos))
menor_custo = float('inf')

def mov_drone(x1, x2, y1, y2):
    """Soma o movimento do drone"""
    s = abs(x2-x1)+abs(y2-y1)
    return s

for p in permut:
    custo_atual = 0
  
    p = list(p)
    p.insert(0, 'R')
    p.append('R')

    for i in range(len(p)-1):
        custo_atual += mov_drone(coordenadas[p[i]][0], coordenadas[p[i+1]][0],coordenadas[p[i]][1], coordenadas[p[i+1]][1]) 

    if custo_atual < menor_custo:
        menor_custo = custo_atual
        caminho = p

print('Melhor caminho:', ' '.join(caminho[1:-1]))
print(f'distância: {menor_custo}')
#print(coordenadas)

fim = time()
print(fim-inicio)