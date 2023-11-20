require 'json'

ARQUIVO_COM_TIPOS_CERTOS = "../arquivos/seinfra.json"
ARQUIVO_PREVISAO = "../arquivos/dados_com_tipo_previsto.json"

tipos_certos = JSON.parse(File.read(ARQUIVO_COM_TIPOS_CERTOS))
hash_modelo = JSON.parse(File.read(ARQUIVO_PREVISAO))

array_tipos = ["", "equipamento", "permanente", "mao de obra", "material", "servicos", "taxas", "outros"]
log = []
i = 0

hash_modelo.each do |codigo, valor|
  if tipos_certos[codigo]["tipo"] != valor["tipo"]
    puts "#{codigo}: #{hash_modelo[codigo]["descricao"]}"
    puts "Preditor: #{array_tipos[valor["tipo"]]} | Original: #{array_tipos[tipos_certos[codigo]["tipo"]]}"
    i += 1
  end  
end

puts "Erros = #{i}"
puts "Precisão de #{(100 - ( i.to_f / hash_modelo.size.to_f) * 100).round(4)}%"