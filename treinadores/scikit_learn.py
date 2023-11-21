import json
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

    with open(ARQUIVO_TREINO, 'r') as file:
        data = json.load(file)

    descriptions = [item['descricao'] for item in data.values()]
    units = [item['unidade'] for item in data.values()]
    types = [item['tipo'] for item in data.values()]
    preco = [item['precos_iguais'] for item in data.values()]
  
    tfidf = TfidfVectorizer()
    X_desc = tfidf.fit_transform(descriptions)

    df_units = pd.get_dummies(units)
    preco_array = np.array(preco).reshape(-1, 1)

    X = np.hstack((X_desc.toarray(), df_units, preco_array))
    y = np.array(types)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=13)

    classifier = RandomForestClassifier(random_state=42)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)
    print(classification_report(y_test, y_pred))

    diretorio_base_modelos = './modelos'
    diretorio_modelo = os.path.join(diretorio_base_modelos, nome_modelo)
    if not os.path.exists(diretorio_modelo):
        os.makedirs(diretorio_modelo)

    dump(classifier, os.path.join(diretorio_modelo, 'modelo_treinado.joblib'))
    dump(tfidf, os.path.join(diretorio_modelo, 'vetorizador_tfidf.joblib'))
    dump(df_units.columns.tolist(), os.path.join(diretorio_modelo, 'unit_columns.joblib'))
    print(f'Novo modelo treinado: {nome_modelo}')


def preditor(pasta_modelo, base):
    classifier = load(f'./modelos/{pasta_modelo}/modelo_treinado.joblib')
    tfidf = load(f'./modelos/{pasta_modelo}/vetorizador_tfidf.joblib')
    unit_columns = load(f'./modelos/{pasta_modelo}/unit_columns.joblib')

    caminho_arquivo = os.path.join('./arquivos/bases', f"{base}.json" )
    with open(caminho_arquivo, "r") as file:
        dados_sem_tipo = json.load(file)

    new_descriptions = [transliteracao(item['descricao']) for item in dados_sem_tipo.values()]
    new_units = [item['unidade'] for item in dados_sem_tipo.values()]
    new_preco = [item['precos_iguais'] for item in dados_sem_tipo.values()]

    X_new_desc = tfidf.transform(new_descriptions)

    new_df_units = pd.get_dummies(new_units).reindex(columns=unit_columns, fill_value=0)
    new_preco_array = np.array(new_preco).reshape(-1, 1)

    X_new = np.hstack((X_new_desc.toarray(), new_df_units, new_preco_array))
    predicted_types = classifier.predict(X_new)

    for i, item_id in enumerate(dados_sem_tipo):
        dados_sem_tipo[item_id]['tipo'] = int(predicted_types[i])

    with open(f'./arquivos/previsoes/previsao_{base}.json', 'w') as file:
        json.dump(dados_sem_tipo, file, indent=2)

    print(f'Arquivo salvo com sucesso: previsao_{base}.json')


def transliteracao(descricao):
	return unidecode(descricao).upper()