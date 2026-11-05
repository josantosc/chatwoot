# Respostas prontas da BioSaúde (Configurações > Respostas prontas). Atalho: digite / na conversa.
# Rodar no container do Chatwoot (cria ou atualiza pelo atalho):
#   docker cp respostas_prontas.rb $CW:/tmp/ && docker exec $CW bundle exec rails runner /tmp/respostas_prontas.rb
# Trechos entre [colchetes] devem ser trocados pelos dados da clínica antes de rodar.
# {{agent.name}} vira o nome do atendente ao inserir. O nome do contato fica de fora: no widget ele é aleatório.

ACCOUNT_ID = (ENV['ACCOUNT_ID'] || 1).to_i

RESPOSTAS = {
  'saudacao' => <<~TXT,
    Olá! Aqui é {{agent.name}}, da BioSaúde. Como posso ajudar?
  TXT
  'aguarde' => <<~TXT,
    Só um instante, por favor. Estou verificando e já retorno.
  TXT
  'transferir' => <<~TXT,
    Vou transferir seu atendimento para o setor responsável. Em instantes alguém continua com você por aqui.
  TXT
  'endereco' => <<~TXT,
    Nosso endereço: [rua, número, bairro], Barras-PI.
    Ponto de referência: [referência].
    Localização: [link do Google Maps]
  TXT
  'horario' => <<~TXT,
    Nosso horário de funcionamento:
    Segunda a sexta: [horário]
    Sábado: [horário]
    Coletas laboratoriais: [horário da coleta]
  TXT
  'convenios' => <<~TXT,
    Atendemos particular e os convênios: [lista de convênios].
    Se o seu não estiver na lista, me informe o nome que eu verifico para você.
  TXT
  'documentos' => <<~TXT,
    No dia do atendimento, traga:
    - documento oficial com foto;
    - carteirinha do convênio (se for usar);
    - pedido médico, quando houver.
  TXT
  'valores' => <<~TXT,
    Para te passar o valor certinho, me envie o nome do exame ou consulta (ou uma foto do pedido médico) e se será particular ou por convênio.
  TXT
  'agendado' => <<~TXT,
    Pronto! Seu atendimento ficou agendado para [data] às [horário], com [profissional/setor].
    Chegue com 15 minutos de antecedência. Se precisar remarcar, é só chamar aqui.
  TXT
  'remarcar' => <<~TXT,
    Sem problema! Me diga qual dia e período ficam melhores para você (manhã ou tarde) que eu verifico os horários disponíveis.
  TXT
  'cancelado' => <<~TXT,
    Seu agendamento foi cancelado. Quando quiser marcar de novo, é só mandar uma mensagem aqui.
  TXT
  'resultado' => <<~TXT,
    Seu resultado fica disponível em até [prazo]. Você pode consultar em [site/portal] com o protocolo que está no seu comprovante, ou retirar na recepção com documento com foto.
  TXT
  'pedido-foto' => <<~TXT,
    Pode me enviar uma foto nítida do pedido médico, por favor? Assim confiro os exames e as orientações.
  TXT
  'sem-resposta' => <<~TXT,
    Ainda está por aí? Se precisar de mais alguma coisa, é só responder esta mensagem.
  TXT
  'fora-horario' => <<~TXT,
    Recebemos sua mensagem! No momento estamos fora do horário de atendimento, mas retornamos assim que reabrirmos. Para agendar, você também pode falar com nosso assistente virtual aqui mesmo, a qualquer hora.
  TXT
  'lgpd' => <<~TXT,
    Por segurança e em respeito à LGPD, não enviamos resultados nem dados de saúde por aqui sem confirmar sua identidade. Por favor, me informe seu nome completo e data de nascimento.
  TXT
  'encerramento' => <<~TXT,
    Posso ajudar em mais alguma coisa? Se não, vou encerrar este atendimento. A BioSaúde agradece o contato!
  TXT
}.freeze

account = Account.find(ACCOUNT_ID)
RESPOSTAS.each do |codigo, texto|
  resposta = account.canned_responses.find_or_initialize_by(short_code: codigo)
  resposta.update!(content: texto.strip)
  puts "#{resposta.previously_new_record? ? 'criada' : 'atualizada'}: /#{codigo}"
end
