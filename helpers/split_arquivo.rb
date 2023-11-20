require 'json'

# hash = JSON.parse(File.read("../../sinapi.json"))

# sem_tipos = {}
# com_tipos = {}
# i = -1
# hash.each do |key, value|
#   if i > 0
#     sem_tipos[key] = value
#   else
#     com_tipos[key] = value
#   end
#   i *= -1
# end

# File.open("./com_tipos.json", 'w') {|f| f << com_tipos.to_json}
# File.open("./sem_tipos", 'w') {|f| f << sem_tipos.to_json}

# hash1 = JSON.parse(File.read(".../../treinador.json"))
# hash2 = JSON.parse(File.read(".../../sem_tipos.json"))

# hash = {}
# hash1.each do |key, value|
#  hash[key] = value
# end
# hash2.each do |key, value|
#   hash[key] = value
#  end
# File.open("./todos_tipos.json", 'w') {|f| f << hash.to_json}

