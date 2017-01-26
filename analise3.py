# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:44:43 2016

@author: lz
"""

import numpy as np
from scipy import stats
import os
from math import fabs

def get_file(nome_arquivo):
    arquivo = open('dados_finais/'+nome_arquivo)
    arquivo.readline()
    x = []

    for linha in arquivo:
        x.append(linha)
    n = len(x)
    pressao = []
    altitude_lua = []
    latitude_estacao = []

    for i in x:
        l = i.split(' ')
        hora = float(l[2])
        dif = fabs(float(l[8]))

        if hora ==0.75 or hora ==0.5 or hora ==0:
#        if hora ==0.75:
            if dif<=2.5:
                pressao.append(float(l[8]))
                altitude_lua.append(float(l[10]))
                latitude_estacao.append(float(l[15]))

    arquivo.close()
    return pressao,altitude_lua,latitude_estacao

def conta(P,A,intervalo_inf,intervalo_sup):
    n = len(P)
    S = []
    for i in range(n):
        if A[i]>=intervalo_inf and A[i]<intervalo_sup:
            S.append(P[i])
    return(S)

def contagem(P,A,n):
    bins = np.linspace(-90,90,n)
    S=[]
    B = []
    for i in range(n-1):
        c = conta(P,A,bins[i],bins[i+1])
        B.append((bins[i]+bins[i+1])/2)
        S.append(c)
    return S,B

def make_files(P,A,L):   
    arquivo_total = open('dados_finais_python/all.dat','a')
    
    
    S,B = contagem(P,A,24)
    soma_a = 0
    saida = []
    for i in range(len(S)):
        a = stats.describe(S[i])
        minimo,maximo = a.minmax
        saida.append([B[i],a.mean,a.variance,a.nobs])
        soma_a+=a.nobs
    print(soma_a)
    arquivo_total.write('bin_center media variancia nobs\n')
       
    for i in saida:
        linha = ' '.join([str(a) for a in i])+'\n'        
        arquivo_total.write(linha)
    
    arquivo_total.close()
    

arquivos = os.listdir('dados_finais/')

try:
    os.remove('dados_finais_python/all.dat')
except:
    print('arqvuivo nao foi excluido')
    pass


pressao_all=[]
altitude_all=[]
latitude_all=[]
for arquivo in arquivos:
    p,a,l = get_file(arquivo)
    pressao_all += p
    altitude_all+=a
    latitude_all +=l
try:
    make_files(pressao_all,altitude_all,latitude_all)
except:
    print('variavel dif muito pequena, vetor vazio')
n = len(pressao_all)
print('Programa finalizado, %d linhas aceitas'%n)