import streamlit as st
from pathlib import Path
from services.llm import analyze_resumes, build_prompt, RateLimitError, AuthenticationError, APIError, TokenLimitError
from services.config import get_hf_api_key, get_hf_model

st.set_page_config(
    page_title="Análise de Candidatos",
    page_icon=":gear:",
    layout="wide",
)

st.markdown(
    f"<style>{Path('assets/style.css').read_text(encoding='utf-8')}</style>",
    unsafe_allow_html=True,
)

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

col_logo, col_title = st.columns([1, 20], vertical_alignment="center")
with col_logo:
    st.image("assets/logo.png", width=64)
with col_title:
    st.subheader("Análise de Candidatos")

col1, col2, col3 = st.columns(3)

LABEL_STYLE = 'style="font-size:14px;font-weight:600;display:inline-block;margin-bottom:0.5rem;"'

with col1:
    st.markdown(f'<label {LABEL_STYLE}>Insira os requisitos da vaga aqui:</label>', unsafe_allow_html=True)
    text_requisites = st.text_area("Insira os requisitos da vaga aqui:", height=200, label_visibility="collapsed")

with col2:
    st.markdown(f'<label {LABEL_STYLE}>Escolha um currículo no formato .md</label>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Escolha um currículo no formato .md",
        type=["md"],
        key=f"uploader_{st.session_state.uploader_key}",
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        st.session_state.uploaded_files[uploaded_file.name] = uploaded_file.read().decode("utf-8")
        st.session_state.uploader_key += 1
        st.rerun()

with col3:
    st.markdown(f'<label {LABEL_STYLE}>Currículos carregados:</label>', unsafe_allow_html=True)
    with st.container(height=154, border=False):
        if st.session_state.uploaded_files:
            to_remove = st.pills(
                "Selecione para remover:",
                options=list(st.session_state.uploaded_files.keys()),
                selection_mode="multi",
                label_visibility="collapsed",
            )
            if to_remove:
                for name in to_remove:
                    del st.session_state.uploaded_files[name]
                st.rerun()
        else:
            st.caption("Nenhum currículo carregado.")

st.divider()

if st.button("Analisar currículos", key="go-button"):
    if not text_requisites or not st.session_state.uploaded_files:
        st.error("Por favor, insira os requisitos da vaga e carregue pelo menos um currículo.")
    else:
        prompt_template = Path("prompts/analysis.md").read_text(encoding="utf-8")
        user_prompt = build_prompt(prompt_template, text_requisites, st.session_state.uploaded_files)
        api_key = get_hf_api_key()

        if not api_key:
            st.error("⚠️ Nenhum HF Token configurado. Configure a variável de ambiente HF_TOKEN para executar a análise.")
        else:
            with st.spinner("Analisando..."):
                try:
                    result = analyze_resumes(
                        api_key=api_key,
                        model=get_hf_model(),
                        prompt=user_prompt,
                    )
                    st.success("Análise concluída com sucesso!")
                    st.write(result)

                except TokenLimitError:
                    st.error(
                        "📄 O conteúdo enviado excede o limite de tokens do modelo.\n\n"
                        "Tente reduzir o número de currículos analisados por vez ou encurtar os requisitos da vaga."
                    )
                except RateLimitError:
                    st.error(
                        "⚠️ Limite de quota atingido ou muitas requisições por minuto!\n\n"
                        "Isso acontece quando é atingido o limite de chamadas gratuitas da Inference API do Hugging Face."
                    )
                except AuthenticationError:
                    st.error("❌ Erro de autenticação: o seu HF Token é inválido ou foi revogado.")
                except APIError as e:
                    st.error(f"💥 Ocorreu um erro na API do Hugging Face: {e.message}")
                except Exception as e:
                    st.error(f"Anomalia inesperada: {e}")

        with st.expander("Prompt enviado ao modelo"):
            st.code(user_prompt, language="markdown")
