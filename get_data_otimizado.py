from astropy.time import Time #biblioteca que converte o datetime atual para o julian
from os import listdir #biblioteca para acessar funcoes do sistema operacional (listar arquivos em uma pasta)
from time import time #biblioteca que acessa o relogio do sistema
from astropy.coordinates import EarthLocation,get_moon,AltAz,solar_system_ephemeris,get_sun #funcoes do astropy
from datetime import datetime
from numpy import genfromtxt #biblioteca de computação cientifica, cria um vetor otimizado a partir de um arquivo
from numba import jit #biblioteca para compilar(deixando mais rapida) operações com vetores (usando funções internas do FORTRAN)

#usando a base de dados do JPL/NASA para receber os dados do sol e lua
solar_system_ephemeris.set('jpl')

#função que le um arquivo e retorna um vetor com todos os dados
def get_dataset(nome_arquivo):
    print('lendo arquivo ',nome_arquivo)
    dataset = genfromtxt('dados_estacoes/'+nome_arquivo, dtype=[('Estacao', 'i8'), ('Data', 'U19'), ('Hora', 'i4'),
        ('TempBulboSeco','f2'), ('TempBulboUmido', 'f2'), ('UmidadeRelativa', 'i2'),
            ('PressaoAtmEstacao', 'f2')], delimiter=';', skip_header=18)

    with open("./dados_estacoes/"+arquivo) as f:
        data = [next(f) for x in range(7)]
    lat = float(data[4].split(':')[1])
    lon = float(data[5].split(':')[1])
    alt = float(data[6].split(':')[1])
    return dataset,lat,lon,alt

#função que escreve os dados completos depois da coleta em um arquivo
def write_file(nome_arquivo,dados):
    f = open('dados_completos/'+nome_arquivo,'w') #abre arquivo para escrita
    print('escrevendo arquivo ',nome_arquivo)
    f.write('estacao data hora_gmt hora_local temp_bulbo_seco temp_bulbo_umido umidade_relativa pressao_atm lua_azimute lua_altitude lua_distancia sol_azimute sol_altitude sol_distancia latiude_estacao longitude_estacao altitude_estacao\n')
    for i in dados:
        linha = ' '.join([str(a) for a in i])+'\n' #converte os dados para string e adiciona quebra de linha
        f.write(linha)
    f.close() #fecha arquivo
    print('fim')

#função que faz a coleta dos dados na base de dados da JPL
#recebe o nome do arquivo da estacao, latitude, longitude e altitude da estacao.
def coleta_dados(nome_arquivo):
    start = time() #conta o tempo de inicio do algoritimo
    print('criando um datetime')
    dataset,lat,lon,alt = get_dataset(nome_arquivo)
    for i in dataset: #loop que percorre todo o arquivo e monta um vetor com a data/hora e converte em um 'datetime'
        dia, mes, ano = [int(k) for k in i['Data'].split('/')] #le a data no formato 10/10/2000 e separa em dia, mes e ano
        hora = int(i['Hora'] / 100 ) #le a hora no formato 1800 (18h) converte para inteiro, 18 e soma +3 do fuso horario
        i['Data'] = str(datetime(ano, mes, dia, hora, 0, 0)) #monta o datetime com os dados obtidos

    loc = EarthLocation.from_geodetic(lon, lat, height=alt) #chama a funcao JPL GetLocation passando a informação da estacao
    times = Time(dataset['Data']) #converte o datetime em universal/julian time (necessario para o JPL)
    print('datetime ok')
    print('get_moon')

    #list comprehension do pyhton, for r in time percorre o vetor de datetime
    #cria uma lista de objetos 'moon' obtidos pela função get_moon do Astropy passando 'r' (item no vetor time)
    #chama a função .transform_to para converter as unidades de ra,dec para alt,az
    moon = [get_moon(r).transform_to(AltAz(obstime=r, location=loc)) for r in times]

    #list comprehension do python para cada objeto moon salva um vetor com az,alt e distancia
    moon = [(i.az.deg,i.alt.deg,i.distance.km) for i in moon]

    print('get_sun') #faz a mesma coisa que o algoritimo anterior para o sol
    sun = [get_sun(r).transform_to(AltAz(obstime=r, location=loc)) for r in times]
    sun = [(i.az.deg,i.alt.deg,i.distance.km) for i in sun]

    print('montando dataset')
    #cria um vetor to tamanho do vetor time para salvar as informacoes de lat,lon e alt
    estacao = [(lat,lon,alt) for _ in range(len(times))]
    dados = dataset.tolist() #converte o vetor dados(um array do numpy para calculos mais rapidos) em uma lista simples
    #concatena todos os vetores(dados = dados anteriores, moon=posicao da lua, sun=posicao do sol, estacao=informacoes da estacao)
    dados = [list(i+k+j+e) for i,k,j,e in zip(dados,moon,sun,estacao)]
    write_file(nome_arquivo,dados) #chama a funcao que escreve os dados do vetor em um arquivo de mesmo nome na pasta /dados_completos
    elapsed = time() - start #conta o tempo que o algoritimo levou para executar
    print('tempo de execução: %d minutos'%(elapsed/60)) #imprime o tempo em minutos



#lista todos os arquivos na pasta 'dados_estacoes' e salva eles em um vetor
arquivos = [f for f in listdir('./dados_estacoes')]

#loop que percorre todos os arquivos da pasta e chama o algoritimo de coleta de dados
for arquivo in arquivos:
    coleta_dados(arquivo)
