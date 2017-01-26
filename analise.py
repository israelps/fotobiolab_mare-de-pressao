# -*- coding: utf-8 -*-
from scipy import stats
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter

def cria_arquivao():
    arquivos = os.listdir('dados_completos/')
    saida = open('dados_completos/arquivao.txt', 'w')
    saida.write('\n')
    for arquivo in arquivos:
        f = open('dados_completos/' + arquivo, 'r')
        f.readline()
        saida.writelines(f.readlines())
        f.close()
    saida.close()


def get_dados_normalizados(nome_arquivo, filtro_min=100):
    f = open('dados_completos/' + nome_arquivo, 'r')
    f.readline()
    arquivo = f.readlines()
    f.close()
    # 0estacao 1data 2hora_gmt 3hora_local 4temp_bulbo_seco 5temp_bulbo_umido 6umidade_relativa 7pressao_atm 8lua_azimute 9lua_altitude
    # 10lua_distancia 11sol_azimute 12sol_altitude 13sol_distancia
    # 14latiude_estacao 15longitude_estacao 16altitude_estacao
    vetor_p0 = []
    vetor_l0 = []
    vetor_p12 = []
    vetor_l12 = []
    vetor_p18 = []
    vetor_l18 = []

    cod_estacao = 0
    latitude_estacao = 0
    for linha in arquivo:
        linha = linha.split(' ')
        if len(linha) < 17:
            continue
        hora = int(linha[2].split(':')[0])
        cod_estacao = int(linha[0])
        latitude_estacao = float(linha[14])
        if hora == 0:
            vetor_p0.append(float(linha[7]))
            vetor_l0.append(float(linha[9]))
        elif hora == 12:
            vetor_p12.append(float(linha[7]))
            vetor_l12.append(float(linha[9]))
        elif hora == 18:
            vetor_p18.append(float(linha[7]))
            vetor_l18.append(float(linha[9]))

    p0_mean = stats.describe(vetor_p0).mean
    vetor_p0 = [(i - p0_mean) for i in vetor_p0]

    p12_mean = stats.describe(vetor_p12).mean
    vetor_p12 = [(i - p12_mean) for i in vetor_p12]

    p18_mean = stats.describe(vetor_p18).mean
    vetor_p18 = [(i - p18_mean) for i in vetor_p18]

    vetor_p = vetor_p0 + vetor_p12 + vetor_p18
    vetor_l = vetor_l0 + vetor_l12 + vetor_l18

    vetor_l = [vetor_l[i]
               for i in range(len(vetor_l)) if abs(vetor_p[i]) <= filtro_min]
    vetor_p = [i for i in vetor_p if abs(i) <= filtro_min]

    return vetor_p, vetor_l, cod_estacao, latitude_estacao


def conta(P, A, intervalo_inf, intervalo_sup):
    n = len(P)
    S = []
    for i in range(n):
        if A[i] >= intervalo_inf and A[i] < intervalo_sup:
            S.append(P[i])
    return S


def contagem(P, A, n):
    bins = np.linspace(-90, 90, n)
    S = []
    B = []
    for i in range(n - 1):
        c = conta(P, A, bins[i], bins[i + 1])
        B.append((bins[i] + bins[i + 1]) / 2)
        S.append(c)
    return S, B


def analise_estacao(nome_arquivo):
    P, A, cod, lat = get_dados_normalizados(nome_arquivo, filtro_min=2.5)
    S, B = contagem(P, A, 24)

    arquivo_total = open('analise/' + nome_arquivo, 'w')
    soma_a = 0
    saida = []
    for i in range(len(S)):
        a = stats.describe(S[i])
        minimo, maximo = a.minmax
        saida.append([B[i], a.mean, sqrt(a.variance / a.nobs), a.nobs])
        soma_a += a.nobs

    arquivo_total.write('CODIGO ESTACAO: %d \n' % cod)
    arquivo_total.write('LATITUDE ESTACAO: %.2f \n' % lat)
    arquivo_total.write('bin_center media erro nobs\n')
    X = [i[0] for i in saida]
    Y = [i[1] for i in saida]
    erro = [i[2] for i in saida]

    fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
    ax.plot(X, Y)
    fig.savefig('analise/'+nome_arquivo[:6]+'.png')   # save the figure to file
    plt.close(fig)

    for i in saida:
        linha = ' '.join([str(a) for a in i]) + '\n'
        arquivo_total.write(linha)

    arquivo_total.close()


arquivos = os.listdir('dados_completos/')

for arquivo in arquivos:
    print(arquivo)
    analise_estacao(arquivo)
    print('fim %s' % arquivo)
