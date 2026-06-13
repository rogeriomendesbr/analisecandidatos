import streamlit as st 
import openai
from openai import OpenAI 
from pathlib import Path 

st.set_page_config(
    page_title="Análise de Currículos", 
    page_icon=":gear:", 
    layout="wide" 
)

def load_file(file_path): 
    return Path(file_path).read_text(encoding="utf-8")

st.markdown(f"<style>{load_file('default.css')}</style>", unsafe_allow_html=True)

# Session state para arquivos e para a key dinâmica do uploader
if 'uploaded_files' not in st.session_state: 
    st.session_state.uploaded_files = {}

if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

col_logo, col_title = st.columns([1, 20], vertical_alignment="center")

with col_logo:
    st.image("logo.png", width=64)

with col_title:
    st.subheader("Análise de Currículos") 

col1, col2, col3 = st.columns(3)

with col1: 
    text_requisites = st.text_area("Insira os requisitos da vaga aqui:", height=200) 

with col2: 
    # A key dinâmica faz o widget "resetar" quando uploader_key muda
    uploaded_file = st.file_uploader(
        "Escolha um currículo no formato .md",
        type=['md'],
        key=f"uploader_{st.session_state.uploader_key}"
    )
    
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state.uploaded_files[file_name] = file_content
        # Incrementa a key para limpar o uploader no próximo rerun
        st.session_state.uploader_key += 1
        st.rerun()
    
with col3:
    st.write("Currículos carregados:")
    with st.container(height=154, border=False):
        if st.session_state.uploaded_files:
            nomes = list(st.session_state.uploaded_files.keys())
            remover = st.pills(
                "Selecione para remover:",
                options=nomes,
                selection_mode="multi",
                label_visibility="collapsed"
            )
            if remover:
                for name in remover:
                    del st.session_state.uploaded_files[name]
                st.rerun()
        else:
            st.caption("Nenhum currículo carregado.")

st.divider()

if st.button("Analisar currículos", key="go-button"): 
    if not text_requisites or not st.session_state.uploaded_files: 
        st.error("Por favor, insira um texto com os requisitos da vaga e carregue pelo menos um currículo.") 
    else: 
        text_prompt = load_file("prompt.md")
        text_resumes = "\n\n- ".join(st.session_state.uploaded_files.values())
        user_prompt = f"{text_prompt}\n\nRequisitos:\n\n{text_requisites}\n\nCurrículos:\n\n- {text_resumes}"

        if st.secrets["openai"]["api_key"]:
            ia_agent = OpenAI(api_key=st.secrets["openai"]["api_key"])
            with st.spinner("Analisando..."):
                try:
                    response = ia_agent.chat.completions.create(
                        model=st.secrets["openai"]["model"],
                        messages=[
                            {"role": "system", "content": "Você é um assistente prestativo."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    st.success("Análise concluída com sucesso!")
                    st.write(response.choices[0].message.content)

                except openai.RateLimitError:
                    text_error = "⚠️ Limite de quota atingido ou muitas requisições por minuto!\n\n"
                    text_error += "Isso acontece quando seus créditos na OpenAI acabaram ou você atingiu o limite de chamadas permitidas para o seu plano atual.\n\n"
                    text_error += "Verifique seu painel de faturamento."
                    st.error(text_error)

                except openai.AuthenticationError:
                    st.error("❌ Erro de Autenticação: A sua API Key é inválida ou foi revogada.")

                except openai.APIError as e:
                    st.error(f"💥 Ocorreu um erro na API da OpenAI: {e.message}")

                except Exception as e:
                    st.error(f"Anomalia inesperada: {e}")

        else:
            with st.expander("Prompt gerado", expanded=True):
                st.code(user_prompt, language="markdown")