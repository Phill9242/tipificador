require 'json'

hash = JSON.parse(File.read("log.json"))

log = []
hash.each do |modelo, bases|
  bases.each do |base, subhash|
    next if base == "precisao_geral"
    subhash["erros"].each do |chave, erro|
      temp_hash =  {
                    "codigo": erro["codigo"], 
                    "descricao": erro["descricao"],
                    "preditor": erro["preditor"],
                    "original": erro["original"],
                    "base": base
                  }
      log << temp_hash
    end
  end
end

puts log.size
File.open("erro.json", "w") {|f| f.write(log.to_json)}