import hashlib
import json
import re
import requests
import streamlit as st

# URL oficial do Web App do Google Apps Script
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbye1l70fNhw5ECEfGqRUFNl64UmKmMnaj2futo4VhFtSJz3kRxvVXB1uWNgxfHqwM4e/exec"

st.set_page_config(
    page_title="Portal de Cadastro | Enterprise Access",
    page_icon="🛡️",
    layout="centered"
)

# Estilização CSS Corporativa
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            max-width: 550px;
        }
        div[data-testid="stForm"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        div[data-testid="stForm"] button[kind="primary"] {
            background-color: #2563EB;
            color: #FFFFFF;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1rem;
        }
        .footer-text {
            text-align: center;
            font-size: 0.8rem;
            color: #64748B;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

def hash_password(password: str) -> str:
    """Gera o hash SHA-256 seguro da senha."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def is_valid_email(email: str) -> bool:
    """Valida formato de e-mail por expressão regular."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

# Interface do Usuário (UI)
st.markdown("### 🛡️ Cadastro de Usuário")
st.markdown("Preencha os campos abaixo para cadastrar o usuário na aba **Usuario**.")

with st.form(key="user_registration_form", clear_on_submit=True):
    nome = st.text_input("Nome Completo", placeholder="Digite o nome")
    email = st.text_input("E-mail", placeholder="nome@empresa.com")
    senha = st.text_input("Senha", type="password", placeholder="Digite a senha")
    
    submit_button = st.form_submit_button(label="Cadastrar Usuário", use_container_width=True, type="primary")

if submit_button:
    nome = nome.strip()
    email = email.strip()

    # Validações dos campos
    if not nome or not email or not senha:
        st.error("❌ **Cadastro não efetuado:** Todos os campos são obrigatórios.")
    elif not is_valid_email(email):
        st.error("❌ **Cadastro não efetuado:** Formato de e-mail inválido.")
    else:
        # Payload com senha protegida por Hash
        payload = {
            "nome": nome,
            "email": email,
            "senha": hash_password(senha)
        }
        
        with st.spinner("🔒 Processando e salvando cadastro..."):
            try:
                # Requisição POST com text/plain para evitar bloqueios CORS do Google Apps Script
                response = requests.post(
                    APPS_SCRIPT_URL,
                    data=json.dumps(payload),
                    headers={"Content-Type": "text/plain;charset=utf-8"},
                    allow_redirects=True,
                    timeout=15
                )
                
                if response.status_code == 200:
                    try:
                        res_json = response.json()
                        if res_json.get("result") == "success":
                            st.success("🎉 **Cadastro efetuado com sucesso!**")
                        else:
                            erro_msg = res_json.get("message", "Erro desconhecido")
                            st.error(f"❌ **Cadastro não efetuado:** {erro_msg}")
                    except json.JSONDecodeError:
                        st.success("🎉 **Cadastro efetuado com sucesso!**")
                elif response.status_code == 401:
                    st.error("❌ **Cadastro não efetuado:** Erro 401 (Acesso Negado). Certifique-se de que o Apps Script está configurado com acesso para 'Qualquer pessoa'.")
                else:
                    st.error(f"❌ **Cadastro não efetuado:** Falha na conexão (Status HTTP: {response.status_code})")
                    
            except requests.exceptions.Timeout:
                st.error("❌ **Cadastro não efetuado:** O servidor demorou muito para responder (Timeout).")
            except Exception as e:
                st.error(f"❌ **Cadastro não efetuado:** {str(e)}")

st.markdown("<div class='footer-text'>Sistema Corporativo Protegido • Google Sheets Database</div>", unsafe_allow_html=True)