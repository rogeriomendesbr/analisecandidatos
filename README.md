---
title: Análise de Currículos
emoji: ⚙️
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.45.1
app_file: app.py
pinned: false
---

# Análise de Currículos

Ferramenta para análise e ranqueamento de currículos com base nos requisitos de uma vaga, utilizando IA (OpenAI).

## Como usar

1. Insira os requisitos da vaga no campo de texto
2. Carregue os currículos no formato `.md`
3. Clique em **Analisar currículos**

## Configuração de segredos (deploy)

No Hugging Face Spaces, configure os segredos em **Settings → Repository secrets**:

| Nome | Valor |
|------|-------|
| `openai__api_key` | Sua chave da API OpenAI |
| `openai__model` | Ex: `gpt-4o-mini` |
