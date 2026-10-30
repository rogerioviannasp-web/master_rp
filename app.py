import hashlib
import re
import streamlit as st
import requests

# URL do Web App do Apps Script
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbye1l70fNhw5ECEfGqRUFNl64UmKmMnaj2futo4VhFtSJz3kRxvVXB1uWNgxfHqwM4e/exec"

st.set_page_config(
    page_title="Portal de Cadastro | Enterprise Access",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização corporativa
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 580px;
        }
        div[data-testid="stForm"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 2.5rem 2rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
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
    """Gera hash SHA-256 da senha."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def is_valid_email(email: str) -> bool:
    """Validação básica de e-mail."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


# UI do Formulário
st.markdown("### 🛡️ Portal de Acesso Corporativo")
st.markdown("<p style='color: #64748B; font-size: 0.95rem; margin-bottom: 1.5rem;'>Efetue seu cadastro no sistema.</p>", unsafe_allow_html=True)

with st.form(key="corporate_registration_form", clear_on_submit=True):
    nome = st.text_input("Nome Completo", placeholder="Ex: Ana Silva")
    email = st.text_input("E-mail Corporativo", placeholder="nome@empresa.com.br")
    senha = st.text_input("Senha de Acesso", type="password")
    
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="Concluir Cadastro", use_container_width=True, type="primary")

if submit_button:
    nome = nome.strip()
    email = email.strip()

    # Apensar validação de preenchimento básico
    if not nome or not email or not senha:
        st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
    elif not is_valid_email(email):
        st.error("❌ E-mail inválido. Por favor, insira um e-mail correto.")
    else:
        # Criptografa a senha (sem filtro de tamanho mínimo)
        senha_hashed = hash_password(senha)
        
        payload = {
            "nome": nome,
            "email": email,
            "senha": senha_hashed
        }
        
        with st.spinner("🔒 Registrando dados na planilha..."):
            try:
                # Faz o POST permitindo redirecionamentos do Google (allow_redirects=True)
                response = requests.post(
                    APPS_SCRIPT_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    allow_redirects=True,
                    timeout=15
                )
                
                if response.status_code == 200:
                    try:
                        res_data = response.json()
                        if res_data.get("result") == "success":
                            st.success("✅ **Cadastro realizado com sucesso!** O registro foi gravado na planilha.")
                        else:
                            st.error(f"❌ Erro retornado pelo Google: {res_data.get('error')}")
                    except ValueError:
                        # Se o Google respondeu 200 mas retornou HTML ao invés de JSON (comum após gravar no Apps Script)
                        st.success("✅ **Cadastro realizado com sucesso!**")
                else:
                    st.error(f"⚠️ Erro ao comunicar com o servidor (Status HTTP: {response.status_code})")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ A requisição demorou muito. Verifique se os dados apareceram na planilha.")
            except requests.exceptions.RequestException as e:
                st.error(f"🔌 Erro de conexão: {e}")

st.markdown("<div class='footer-text'>Sistema Corporativo Protegido • Hash SHA-256 Enabled</div>", unsafe_allow_html=True)