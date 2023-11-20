require 'i18n'

CONECTIVOS = ["DE", "DA", "PARA", "EM", "A", "E", "-", "COM", "O", "NO", "PRA", "OU"]

I18n.available_locales = [:en, :'pt-BR']

def transliteracao(descricao)
  transliteracao = I18n.transliterate(descricao)
  transliteracao.upcase
end

def remover_conectivos(descricao)
  sem_conectivos = []
  array_palavras = descricao.gsub(/[()]/, '').split(/[\s,]+/)
  sem_conectivos = array_palavras.reject {|palavra| CONECTIVOS.include?(palavra)}
  sem_conectivos.join(" ")
end

def normalizador(hash)
  hash.each do |codigo, value|
    hash[codigo]["descricao"] = transliteracao(value["descricao"])
  end
end
