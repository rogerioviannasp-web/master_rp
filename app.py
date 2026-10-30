import streamlit as st
import requests

# URL do Web App fornecida
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbye1l70fNhw5ECEfGqRUFNl64UmKmMnaj2futo4VhFtSJz3kRxvVXB1uWNgxfHqwM4e/exec"

st.set_page_config(page_title="Cadastro de Usuários", page_icon="👤", layout="centered")

st.title("👤 Cadastro de Usuário")
st.write("Preencha os campos abaixo para realizar o seu cadastro.")

with st.form(key="user_registration_form", clear_on_submit=True):
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    
    submit_button = st.form_submit_button(label="Cadastrar")

if submit_button:
    if not nome or not email or not senha:
        st.warning("⚠️ Por favor, preencha todos os campos do formulário.")
    else:
        payload = {
            "nome": nome,
            "email": email,
            "senha": senha
        }
        
        with st.spinner("Enviando dados para a planilha..."):
            try:
                response = requests.post(APPS_SCRIPT_URL, json=payload)
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json.get("result") == "success":
                        st.success("🎉 Usuário cadastrado com sucesso!")
                    else:
                        st.error(f"Erro no Apps Script: {res_json.get('error')}")
                else:
                    st.error(f"Falha ao conectar. Código de status: {response.status_code}")
            except Exception as e:
                st.error(f"Ocorreu um erro na requisição: {e}")