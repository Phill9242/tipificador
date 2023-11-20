require 'json'

seinfra = JSON.parse(File.read("../arquivos/seinfra.json"))

tipos = File.read("./datas").split("\n")
codigos = File.read("./codigo").split("\n")

MAO_DE_OBRA = "2"
EQUIP = "1"
MAT = "3"
tipos.each_with_index do |tipo, index|
  case tipo
  when EQUIP
    seinfra[codigos[index].upcase]["tipo"] = 1
    next
  when MAO_DE_OBRA
  seinfra[codigos[index].upcase]["tipo"] = 3
    next
  when MAT
    seinfra[codigos[index].upcase]["tipo"] = 4
    next
  end
end

File.open("../arquivos/seinfra_tipos_certos.json", "w") {|f| f << seinfra.to_json}