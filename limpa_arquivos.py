import re
from os import listdir
arquivos = [f for f in listdir('./dados_originais')]
for arquivo in arquivos:
    with open("./dados_originais/"+arquivo) as f:
        cabecalho = [next(f) for x in range(17)]
        data = f.readlines()
        data1 = [x for x in data if not re.match(r'^\s*$', x)]
        data1 = [x for x in data1 if not x.split(';')[1]=='']
        data1 = [x for x in data1 if not x.split(';')[2]=='']
        data1 = [x for x in data1 if not x.split(';')[6]=='']
    with open('relatorio_filtro.txt','a') as f:
        f.write('%s - %d linhas imcompletas removidas.\n'%(arquivo,len(data)-len(data1)))
    with open('./dados_estacoes/'+arquivo,'w') as f:
        data = cabecalho+data1
        f.writelines(data)
