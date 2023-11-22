import argparse
import json
import os
import sys
from treinadores import scikit_learn
from unidecode import unidecode

class Tipificador:

	def __init__(self):
		self.processar_argumentos()
		self.verificar_arquivos()
		self.instanciar_variaveis()
		return
	
	def processar_argumentos(self):
		parser = argparse.ArgumentParser(description='Processa os argumentos.')
		parser.add_argument('-m', '--modelo', required=True, help='O nome do modelo a ser utilizado.')
		parser.add_argument('-b', '--bases', required=False, help='As bases a serem tipificadas.\nSe o argumento não for utilizado todas as bases serão tipificadas')
		args = parser.parse_args()

		self.modelo = "_".join(sorted(args.modelo.split(" ")))
		self.bases = args.bases.split(" ") if args.bases else None
		return

	def verificar_arquivos(self):
		if self.bases:
			self.checar_arquivo_bases()
		else:
			bases_json = [arq for arq in os.listdir("./arquivos/bases") if os.path.isfile(os.path.join("./arquivos/bases", arq))]
			self.bases = list(map(lambda base: base.split(".")[0], bases_json))
		self.checar_modelo()
		return

	def instanciar_variaveis(self):
		with open("arquivos/log.json", "r") as file:
			self.log = json.load(file)
		self.novo_log = {}
		self.array_previsao = []
		self.array_tipo_original = []
		self.array_tipos = ["", "equipamento", "equipamento permanente", "mão de obra", "material", "serviços", "taxas", "outros", "", "administracao", "aluguel", "verba"]
		return

	def checar_modelo(self):
		modelo_caminho = os.path.join("./modelos", self.modelo)
		if not os.path.exists(modelo_caminho):
			print(f"A pasta do modelo '{self.modelo}' não existe.")
			exit()
		if not os.path.exists(os.path.join(modelo_caminho, "vetorizador_tfidf.joblib")):
			print("É necessário gerar o arquivo do Vetorizador")
			exit()
		if not os.path.exists(os.path.join(modelo_caminho, "unidades.joblib")):
			print("É necessário gerar o arquivo de dummie das unidades")
			exit()
		if not os.path.exists(os.path.join(modelo_caminho, "modelo_treinado.joblib")):
			print("É necessário gerar o arquivo do modelo")
			exit()
		return

	def checar_arquivo_bases(self):
		for base in self.bases:
			caminho_arquivo = os.path.join("./arquivos/bases", f"{base}.json")
			if not os.path.exists(caminho_arquivo):
				print(f"O arquivo '{base}' não existe. Certifique-se de que ele está na pasta correta.")
				exit()
		return	

	def gerar_log(self):
		i = 0
		self.novo_log = {}
		for previsao in self.array_previsao:
			original = self.array_tipo_original[i]
			base = self.bases[i]
			mensagens = self.log.get(self.modelo, {}).get(base, {}).get("erros", {})
			self.percorrer_dicionario_previsoes(previsao, original, mensagens)
			itens_totais = len(previsao)
			erros = len(mensagens)
			precisao = round(100 - (erros / itens_totais * 100), 2)
			self.novo_log[base] = {}
			self.novo_log[base]["erros"] = mensagens
			self.novo_log[base]["precisao"] = str(precisao)
			self.novo_log[base]["itens"] = str(itens_totais)
			self.novo_log[base]["n_erros"] = str(erros)
			i += 1
		self.salvar_log()
		return
	
	def salvar_log(self):
			self.novo_log["precisao_geral"] = self.calcular_precisao_geral()
			self.log[self.modelo] = self.novo_log
			with open("arquivos/log.json", 'w') as file:
				json.dump(self.log, file, indent=2)
			print ("Arquivo de log gerado com sucesso em \"./arquivos/log.json\"")
			return

	def percorrer_dicionario_previsoes(self, previsao, original, mensagens):
		for codigo, valor in previsao.items():
			if original[codigo]["tipo"] != valor["tipo"]:
				descricao = self.transliteracao(original[codigo]['descricao'])
				tipo_preditor = unidecode(self.array_tipos[valor['tipo']])
				tipo_original = unidecode(self.array_tipos[original[codigo]['tipo']])
				mensagens[codigo] = {"codigo": f"{codigo}", "descricao": f"{descricao}", "preditor": f"{tipo_preditor}", "original": f"{tipo_original}"}
		return 

	def transliteracao(self, descricao):
		return unidecode(descricao).upper()

	def preditor(self):
		for base in self.bases:
			scikit_learn.preditor(self.modelo, base)
			self.abrir_arquivos_json(base)
		return
	
	def abrir_arquivos_json(self, base):
		caminho_arquivo_previsao = f"./arquivos/previsoes/previsao_{base}.json"
		caminho_arquivo_original = f"./arquivos/bases/{base}.json"
		with open(caminho_arquivo_previsao, 'r') as arquivo_previsao, open(caminho_arquivo_original, 'r') as arquivo_original:
			self.array_previsao.append(json.load(arquivo_previsao))
			self.array_tipo_original.append(json.load(arquivo_original))
		return
	
	def calcular_precisao_geral(self):
		erros = 0
		itens = 0
		for _, sub_hash in self.novo_log.items():
			erros += int(sub_hash["n_erros"])
			itens += int(sub_hash["itens"])
		return str(round(100 - (erros / itens * 100), 2))
# FIM CLASSE TIPIFICADOR

def main():
	tipificador = Tipificador()
	tipificador.preditor()
	tipificador.gerar_log()

if __name__ == "__main__":
	main()