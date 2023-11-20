import argparse
import json
import os
import sys
from treinadores import scikit_learn

class Argumentos:

	def __init__(self):
		parser = argparse.ArgumentParser(description='Processa os argumentos.')
		parser.add_argument('-m', '--modelo', required=True, help='O nome do modelo a ser utilizado.')
		parser.add_argument('-a', '--arquivo', required=False, help='O arquivo que contém os dados para tipificar.')
		parser.add_argument('-l', '--log', required=False, help='Ative esta opção para gerar um log de precisão de todas as bases disponíveis')
		args = parser.parse_args()

		self.modelo = "_".join(sorted(args.modelo.split(" ")))
		self.arquivo = args.arquivo if args.arquivo else None
		self.log = args.log.split(" ") if args.log else None

		if self.arquivo:
			self.checar_arquivo()

		self.checar_modelo()

	def checar_modelo(self):
		modelo_caminho = os.path.join("./modelos", self.modelo)
		if not os.path.exists(modelo_caminho):
			print(f"A pasta do modelo '{self.modelo}' não existe.")
			exit()

		if not os.path.exists(os.path.join(modelo_caminho, "vetorizador_tfidf.joblib")):
			print("É necessário gerar o arquivo do Vetorizador")
			exit()

		if not os.path.exists(os.path.join(modelo_caminho, "unit_columns.joblib")):
			print("É necessário gerar o arquivo de dummie das unidades")
			exit()

		if not os.path.exists(os.path.join(modelo_caminho, "modelo_treinado.joblib")):
			print("É necessário gerar o arquivo do modelo")
			exit()

	def checar_arquivo(self):
		caminho_arquivo = os.path.join("./arquivos/bases", f"{self.arquivo}.json")
		if not os.path.exists(caminho_arquivo):
			print(f"O arquivo '{self.arquivo}' não existe. Certifique-se de que ele está na pasta correta.")
			exit()		

def comparador(base):
	file_path_previsao = f"./arquivos/previsoes/previsao_{base}.json"
	file_path_original = f"./arquivos/bases/{base}.json"

	with open(file_path_previsao, 'r') as file_previsao, open(file_path_original, 'r') as file_original:
		previsao = json.load(file_previsao)
		original = json.load(file_original)

	array_tipos = ["", "equipamento", "permanente", "mão de obra", "material", "serviços", "taxas", "outros"]
	erros = 0
	mensagens = []

	for codigo, valor in previsao.items():
		if original[codigo]["tipo"] != valor["tipo"]:
			descricao = original[codigo]['descricao']
			tipo_preditor = array_tipos[valor['tipo']]
			tipo_original = array_tipos[original[codigo]['tipo']]
			mensagens.append(f"{codigo}: {descricao}\nPreditor: {tipo_preditor} | Original: {tipo_original}\n")
			erros += 1

	total_items = len(previsao)
	precisao = 100 - (erros / total_items * 100)
	print("\n".join(mensagens))
	print(f"Erros = {erros}")
	print(f"Precisão de {round(precisao, 2)}%")

def gerar_log(args):
	novo_log = {}
	with open("arquivos/log.json", "r") as file:
		log = json.load(file)

	arquivos = [arq for arq in os.listdir("./arquivos/bases") if os.path.isfile(os.path.join("./arquivos/bases", arq))]

	for arquivo in arquivos:
		base = arquivo.split(".")[0]
		caminho_base = os.path.join("./arquivos/bases/", arquivo)		
		with open(caminho_base, 'r') as file:
			original = json.load(file)

		scikit_learn.preditor(args.modelo, base)
		file_path_previsao = f"./arquivos/previsoes/previsao_{base}.json"
		file_path_original = f"./arquivos/bases/{base}.json"

		with open(file_path_previsao, 'r') as file_previsao, open(file_path_original, 'r') as file_original:
			previsao = json.load(file_previsao)
			original = json.load(file_original)

		erros = 0
		for codigo, valor in previsao.items():
			if original[codigo]["tipo"] != valor["tipo"]:
				erros += 1

		itens_totais = len(previsao)
		precisao = round(100 - (erros / itens_totais * 100), 2)
		novo_log[base] = {}
		novo_log[base]["precisao"] = str(precisao)
		novo_log[base]["itens"] = str(itens_totais)
		novo_log[base]["erros"] = str(erros)

	novo_log["precisao_geral"] = calcular_precisao_geral(novo_log)

	log[args.modelo] = novo_log
	with open("arquivos/log.json", 'w') as file:
		json.dump(log, file, indent=2)

def calcular_precisao_geral(hash):
	erros = 0
	itens = 0
	for _, sub_hash in hash.items():
		erros += int(sub_hash["erros"])
		itens += int(sub_hash["itens"])
	return str(round(100 - (erros / itens * 100), 2))

def main():
	args = Argumentos()
	if args.arquivo:
		scikit_learn.preditor(args.modelo, args.arquivo)
		comparador(args.arquivo)
		
	if args.log:
		gerar_log(args)

if __name__ == "__main__":
	main()