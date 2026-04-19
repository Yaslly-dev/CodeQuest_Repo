import requests#Importa a biblioteca requests para fazer requisições
import pprint#Importa a biblioteca pprint para imprimir os dados de forma bonita
import os #usar variaveis de ambiente
url = "http://api.weatherapi.com/v1/current.json"#Url da api
key = 'Cole sua chave aqui'#token de acesso
params = {"key": key,"q": "Brasilia","lang": "pt"}#Parametros
resposta = requests.get(url, params)#request para a api com os parametros
if resposta.status_code == 200:#Verifica se o request deu certo
    dados = resposta.json()#Transforma a resposta em um dicionário
    #pprint.pprint(dados)
    clima = dados["current"]["temp_c"]#Pega a temperatura em celcius
    print(f"A temperatura atual em {params['q']} é de {clima}°C")#mostra temperatura atual
else:    print("Erro ao obter os dados do clima")#Imprime uma mensagem de erro caso o .code não seja 200 ou seja nao deu certo
