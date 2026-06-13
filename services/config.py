import os
import streamlit as st


def get_secret(env_var: str, toml_section: str, toml_key: str, default: str = "") -> str:
    if value := os.environ.get(env_var):
        return value
    try:
        return st.secrets[toml_section][toml_key]
    except (KeyError, FileNotFoundError):
        return default


def get_hf_api_key() -> str:
    return get_secret("HF_TOKEN", "huggingface", "token")


def get_hf_model() -> str:
    return get_secret("HF_MODEL", "huggingface", "model", default="Qwen/Qwen2.5-72B-Instruct")
