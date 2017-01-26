import re
from os import listdir
arquivos = [f for f in listdir('./dados_originais')]
print('iniciando')
linhas_totais = 0
linhas_removidas = 0
for arquivo in arquivos:
    print(arquivo)    
    with open("./dados_originais/"+arquivo) as f:
        cabecalho = [next(f) for x in range(17)]
        data = f.readlines()        
        data1 = [x for x in data if not re.match(r'^\s*$', x)]
        data1 = [x for x in data1 if not x.split(';')[1]=='']
        data1 = [x for x in data1 if not x.split(';')[2]=='']
        data1 = [x for x in data1 if not x.split(';')[6]=='']
        linhas_totais+=len(data)
        linhas_removidas+=len(data)-len(data1)
    with open('relatorio_filtro.txt','a') as f:
        f.write('%s - %d linhas imcompletas removidas.\n'%(arquivo,len(data)-len(data1)))
    with open('./dados_estacoes/'+arquivo,'w') as f:
        data = cabecalho+data1
        f.writelines(data)
print('%.2f p/cento de linhas removidas'%((linhas_removidas/linhas_totais)*100))
print('fim')