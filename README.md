---
title: Análise de Candidatos
emoji: ⚙️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Análise de Candidatos

Ferramenta para análise e ranqueamento de candidatos com base nos requisitos de uma vaga de emprego, utilizando IA via Hugging Face Inference API.

## Como usar

1. Insira os requisitos da vaga no campo de texto
2. Carregue os currículos dos candidatos no formato `.md`
3. Clique em **Analisar candidatos**

O resultado é um parecer executivo de RH com uma tabela ranqueando os candidatos por grau de alinhamento à vaga. O prompt enviado ao modelo fica disponível colapsado ao final da página para consulta ou uso manual.

## Executar localmente com Docker

```bash
docker build -t analise-candidatos .
docker run -p 7860:7860 -e HF_TOKEN=hf_... analise-candidatos
```

Para usar um modelo diferente do padrão (`Qwen/Qwen2.5-72B-Instruct`):

```bash
docker run -p 7860:7860 -e HF_TOKEN=hf_... -e HF_MODEL=meta-llama/Llama-3.1-8B-Instruct analise-candidatos
```

Acesse em: http://localhost:7860

## Executar localmente sem Docker

```bash
pip install -r requirements.txt
# configure .streamlit/secrets.toml (veja secrets.toml.example)
python streamlit run app.py
```

## Configuração de segredos (Hugging Face Spaces)

Em **Settings → Repository secrets**, adicione:

| Variável de ambiente | Valor |
|---|---|
| `HF_TOKEN` | Seu token da Hugging Face (com permissão de Inference) |
| `HF_MODEL` | Opcional. Ex: `Qwen/Qwen2.5-72B-Instruct` |

O token pode ser criado em **huggingface.co → Settings → Access Tokens**.

## Autor

| | |
|---|---|
| **Nome** | Rogério Mendes |
| **E-mail** | rogeriomendes@gmail.com |
| **GitHub** | https://github.com/rogeriomendesbr |
| **LinkedIn** | https://www.linkedin.com/in/rogeriomendesbr |
