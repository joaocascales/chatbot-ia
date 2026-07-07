# Projeto adicional -  SENAI IA Chatbot - Criando Seu Assistente de Programação Python, em Python

# Importa módulo para interagir com o sistema operacional
import os

# Importa a biblioteca Streamlit para criar a interface web interativa
import streamlit as st

# Importa a classe Groq para se conectar à API da plataforma Groq e acessar o LLM
from groq import Groq

# Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar
st.set_page_config(
    page_title="Chatbot do JP",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o "Chatbot IA voltado para conhecimentos gerais e para auxiliar em tarefas operacionais do dia-a-dia", um assistente de IA especialista em arquivos .xlsx, .csv, .bpm, .txt, e especialista em SAP 4Hana e SAP Concur. Sua missão é ajudar analistas a encontrarem respostas, soluções e ideias de acordo com suas necessidades.

REGRAS DE OPERAÇÃO:
1.  **Foco em suporte nas tarefas**: Responda de acordo com os dados fornecidos pelo usuário para que a orientação seja dada de maneira objetiva e baseado nas ferramentas e atividades do usuário.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Como Executar**: Dê exemplos de como o usuário pode prosseguir, pois os sistemas utilizados são SAP 4Hana, Coupa, SAP Concur e Pipefy.
    * **Detalhes do Retorno**: Inicialmente questione qual perfil, área e atividades do usuário para que você se baseie do perfil dele.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para auxiliar com exemplos e com respostas de dúvidas.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    
    # Define o título da barra lateral
    st.title("🤖 Chatbot do JP")
    
    # Mostra um texto explicativo sobre o assistente
    st.markdown("Chatbot IA voltado para conhecimentos gerais e para auxiliar em tarefas operacionais do dia-a-dia.")
    
    # Campo para inserir a chave de API da Groq
    groq_api_key = st.text_input(
        "Insira sua API Key Groq", 
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar em suas dúvidas operacionais.")
    st.markdown(" IA pode cometer erros. Sempre verifique as respostas.")

    st.markdown("---")
    st.markdown("Para suporte, procure João Pedro Amor (joao.amor.ext@vtal.com)")

    # Link para o site do SENAI Suiço
    st.markdown("🔗 [Linkedin JP](https://www.linkedin.com/in/joaopedrocascales/)")
    

# Título principal do app
st.title("IA para auxiliar em suas necessidades")

# Subtítulo adicional
st.title("Assistente Pessoal particular")

# Texto auxiliar abaixo do título
st.caption("Faça sua pergunta sobre processos e documentos que necessita de ajuda.")

# Inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variável do cliente Groq como None
client = None

# Verifica se o usuário forneceu a chave de API da Groq
if groq_api_key:
    
    try:
        
        # Cria cliente Groq com a chave de API fornecida
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

# Caso não tenha chave, mas já existam mensagens, mostra aviso
elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Qual sua dúvida?"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                senai_ia_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(senai_ia_resposta)
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": senai_ia_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>Chatbot do JP</p>
    </div>
    """,
    unsafe_allow_html=True
)
