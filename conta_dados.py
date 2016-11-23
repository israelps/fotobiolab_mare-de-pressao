from os import listdir
arquivos = [f for f in listdir('./dados_originais')]
dados_originais=0
dados_estacoes=0
for arquivo in arquivos:
    with open("./dados_originais/"+arquivo) as f:
        cabecalho = [next(f) for x in range(17)]
        data = f.readlines()
    dados_originais+=len(data)
for arquivo in arquivos:
    with open("./dados_estacoes/"+arquivo) as f:
        cabecalho = [next(f) for x in range(17)]
        data = f.readlines()
    dados_estacoes+=len(data)


print('Dados originais: %d'%dados_originais)
print('Dados consistentes: %d'%dados_estacoes)
print('Dados removidos: %d'%(dados_originais-dados_estacoes))
