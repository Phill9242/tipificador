import json
from random import randint
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from joblib import dump, load
import os
from unidecode import unidecode

ARQUIVO_TREINO = './arquivos/treinador.json'

def treinador(nome_modelo):
	numero_aleatorio = randint(1, 100)
	tamanho_teste = 0.01
	with open(ARQUIVO_TREINO, 'r') as file:
			data = json.load(file)

	descricoes = [item['descricao'] for item in data.values()]
	units = [item['unidade'] for item in data.values()]
	tipos = [item['tipo'] for item in data.values()]
	preco = [item['precos_iguais'] for item in data.values()]

	tfidf = TfidfVectorizer()
	descricoes_tfidf = tfidf.fit_transform(descricoes)
	unidades_dummie = pd.get_dummies(units)
	preco_array = np.array(preco).reshape(-1, 1)
	x_dados = np.hstack((descricoes_tfidf.toarray(), unidades_dummie, preco_array))
	array_tipos = np.array(tipos)

	x_dados_treino, x_dados_teste, array_tipos_treino, array_tipos_teste = train_test_split(x_dados, array_tipos, test_size=tamanho_teste, random_state=numero_aleatorio)

	classifier = RandomForestClassifier(random_state=numero_aleatorio)
	classifier.fit(x_dados_treino, array_tipos_treino)

	y_pred = classifier.predict(x_dados_teste)
	print(classification_report(array_tipos_teste, y_pred))

	diretorio_base_modelos = './modelos'
	diretorio_modelo = os.path.join(diretorio_base_modelos, nome_modelo)
	if not os.path.exists(diretorio_modelo):
			os.makedirs(diretorio_modelo)

	dump(classifier, os.path.join(diretorio_modelo, 'modelo_treinado.joblib'))
	dump(tfidf, os.path.join(diretorio_modelo, 'vetorizador_tfidf.joblib'))
	dump(unidades_dummie.columns.tolist(), os.path.join(diretorio_modelo, 'unidades.joblib'))
	print(f'Novo modelo treinado: {nome_modelo}')


def preditor(pasta_modelo, base):
	modelo = load(f'./modelos/{pasta_modelo}/modelo_treinado.joblib')
	tfidf = load(f'./modelos/{pasta_modelo}/vetorizador_tfidf.joblib')
	unidades_treino = load(f'./modelos/{pasta_modelo}/unidades.joblib')

	caminho_arquivo = os.path.join('./arquivos/bases', f"{base}.json" )
	with open(caminho_arquivo, "r") as file:
		arquivo_base = json.load(file)

	descricoes = [transliteracao(item['descricao']) for item in arquivo_base.values()]
	unidades = [item['unidade'] for item in arquivo_base.values()]
	preco = [item['precos_iguais'] for item in arquivo_base.values()]

	descricoes_tfidf = tfidf.transform(descricoes)
	unidades_dummie = pd.get_dummies(unidades).reindex(columns=unidades_treino, fill_value=0)
	preco_array = np.array(preco).reshape(-1, 1)

	x_dados = np.hstack((descricoes_tfidf.toarray(), unidades_dummie, preco_array))
	previsoes = modelo.predict(x_dados)

	for i, item_id in enumerate(arquivo_base):
		arquivo_base[item_id]['tipo'] = int(previsoes[i])

	with open(f'./arquivos/previsoes/previsao_{base}.json', 'w') as file:
		json.dump(arquivo_base, file, indent=2)

	print(f'Arquivo salvo com sucesso: previsao_{base}.json')

def transliteracao(descricao):
	return unidecode(descricao).upper()