import json
import os
import sys
from treinadores import scikit_learn
from unidecode import unidecode

def main():
	caminho = "./arquivos/bases/"
	extensao = ".json"
	hash_bases = {}
	bases = sorted([base for base in sys.argv[1:]])

	for base in bases:
		arquivo = os.path.join(caminho, base + extensao)
		if not os.path.exists(arquivo):
			return print(f'Arquivo {base} não existe. Por favor, verifique os argumentos.')

		with open(arquivo, 'r', encoding='utf-8') as file:
			temp_hash = json.load(file)		
		tratar_hash(temp_hash)
		hash_bases.update(temp_hash)

	nome_modelo = "_".join(bases)
	with open(os.path.join("./arquivos/", "treinador.json"), 'w', encoding='utf-8') as f:
		json.dump(hash_bases, f, ensure_ascii=False, indent=2)
	
	scikit_learn.treinador(nome_modelo)

def tratar_hash(hash):
	for codigo, valor in hash.items():
		valores_iguais = 1 if valor["preco_desonerado"] == valor["preco_onerado"] else 0
		hash[codigo]["descricao"] = transliteracao(valor["descricao"])
		hash[codigo]["precos_iguais"] = valores_iguais

def transliteracao(descricao):
	return unidecode(descricao).upper()

if __name__ == "__main__":
	main()
