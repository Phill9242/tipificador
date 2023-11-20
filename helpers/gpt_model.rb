require 'net/http'
require 'json'

API_KEY = "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"
THREAD_ID = "thread_YxjPK2BZwkeLpTWAN6BJZ3fE"
ASSISTANT_ID = "asst_fTbAzBR7DoKjmnCZvmD8KYmM"
HEADERS = {'Content-Type' => 'application/json', 'Authorization' => "Bearer #{API_KEY}", 'OpenAI-Beta' => 'assistants=v1'}


def gerar_mensagem(array)
  messages_post = "https://api.openai.com/v1/threads/#{THREAD_ID}/messages"
  uri = URI(messages_post)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  
  body = {
    role: 'user',
    content: array.to_s
  }.to_json
    
  request = Net::HTTP::Post.new(uri, HEADERS)
  request.body = body  
  response = http.request(request)
end

def executar_thread()
  run_thread = "https://api.openai.com/v1/threads/#{THREAD_ID}/runs"
  uri = URI(run_thread)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true

  body = {
    "assistant_id": ASSISTANT_ID
  }.to_json

  request = Net::HTTP::Post.new(uri, HEADERS)
  request.body = body  
  response = http.request(request)
end

def recuperar_mensagem(x)
  sleep 3
  mensagens = "https://api.openai.com/v1/threads/#{THREAD_ID}/messages"
  uri = URI(mensagens)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true

  request = Net::HTTP::Get.new(uri, HEADERS)
  response = http.request(request)
  hash = JSON.parse(response.body)
  if hash["data"].first["role"] == "user"
    puts "Esperando"
    return if x > 1
    return recuperar_mensagem(x + 1)
  else
    array_tipos = hash["data"].first["content"].first["text"]["value"]
  end
  puts "EITA NOIS\n\n"
  puts hash["data"].first
  return array_tipos
end

@keys = []

def gerar_array_de_descrições()
  x = JSON.parse(File.read("./nao_tipados.json"))
  array = []
  x.each do |key, value|
    next if value["tipo"]
    array << value["descricao"] 
    @keys << key
  end
  puts array.first
  array
end

array = gerar_array_de_descrições()
x = 0
sub_array = []

def converter_string_resposta_para_array(resposta)
  puts resposta
  resposta = resposta.gsub(/["'\[\]]/, "")
  array = resposta.split(",")
  array.map {|valor| valor.strip}
end

def adicionar_tipos_ao_json(array_tipos)
  hash = JSON.parse(File.read("./nao_tipados.json"))
  puts @keys.first
  array_tipos.each do |tipo|
    hash[@keys.shift]["tipo"] = tipo    
  end
  File.open("./nao_tipados.json", 'w') {|f| f << hash.to_json}
end

array.each do |valor|
  sub_array << valor
  x += 1
  next if sub_array.size < 20
  gerar_mensagem(sub_array)
  executar_thread()
  resposta = recuperar_mensagem(0)
  array_tipos = converter_string_resposta_para_array(resposta)
  adicionar_tipos_ao_json(array_tipos)
  sub_array = []
end

if sub_array.any?

  gerar_mensagem(sub_array)
  executar_thread()
  resposta = recuperar_mensagem(0)
  array_tipos = converter_string_resposta_para_array(resposta)
  adicionar_tipos_ao_json(array_tipos)

end