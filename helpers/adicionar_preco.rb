require 'json'

ARQUIVO = "../arquivos/sbc_composicoes.json"

insumos = JSON.parse(File.read(ARQUIVO))

insumos.each do |codigo, value|
  insumos[codigo]["precos_iguais"] = value["preco_desonerado"] == value["preco_onerado"] ? 1 : 0
end

File.open(ARQUIVO, 'w') {|f| f << insumos.to_json}