require 'json'

ARQUIVOS = ["sicro3", "sinapi", "sbc", "sbc_composicoes"]

hash = {}
ARQUIVOS.each do |arquivo|
  hash_arquivo = JSON.parse(File.read("../arquivos/#{arquivo}.json"))
  hash.merge!(hash_arquivo)  
end

File.open("../arquivos/treinador.json", 'w') {|f| f << hash.to_json}