import hashlib
import re
import streamlit as st
import requests

# ==========================================
# CONFIGURAÇÕES E CONSTANTES CORPORATIVAS
# ==========================================
DEFAULT_APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbye1l70fNhw5ECEfGqRUFNl64UmKmMnaj2futo4VhFtSJz3kRxvVXB1uWNgxfHqwM4e/exec"

# Tenta carregar dos Secrets do Streamlit, fallback para URL padrão
APPS_SCRIPT_URL = st.secrets.get("APPS_SCRIPT_URL", DEFAULT_APPS_SCRIPT_URL)

st.set_page_config(
    page_title="Portal de Cadastro | Enterprise Access",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS para refinamento corporativo e UI fluida
st.markdown("""
    <style>
        /* Estilização do container principal */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 580px;
        }
        /* Card visual do formulário */
        div[data-testid="stForm"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 2.5rem 2rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
        }
        /* Botão de envio primário corporativo */
        div[data-testid="stForm"] button[kind="primary"] {
            background-color: #2563EB;
            color: #FFFFFF;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1rem;
            transition: all 0.2s ease-in-out;
        }
        div[data-testid="stForm"] button[kind="primary"]:hover {
            background-color: #1D4ED8;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        /* Indicador de rodapé */
        .footer-text {
            text-align: center;
            font-size: 0.8rem;
            color: #64748B;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# FUNÇÕES DE SEGURANÇA E VALIDAÇÃO
# ==========================================
def hash_password(password: str) -> str:
    """Gera um hash SHA-256 seguro da senha antes de enviar."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def is_valid_email(email: str) -> bool:
    """Valida sintaxe de e-mail usando expressão regular."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def evaluate_password_strength(password: str) -> tuple[bool, str]:
    """Mede a força da senha e retorna elegibilidade corporativa."""
    if len(password) < 8:
        return False, "A senha deve conter no mínimo 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "A senha deve conter ao menos uma letra maiúscula."
    if not re.search(r"[0-9]", password):
        return False, "A senha deve conter ao menos um número."
    return True, "Senha forte."


# ==========================================
# INTERFACE DO USUÁRIO (UI)
# ==========================================
st.markdown("### 🛡️ Portal de Acesso Corporativo")
st.markdown("<p style='color: #64748B; font-size: 0.95rem; margin-bottom: 1.5rem;'>Efetue seu cadastro para obter credenciais no sistema.</p>", unsafe_allow_html=True)

with st.form(key="corporate_registration_form", clear_on_submit=True):
    nome = st.text_input("Nome Completo", placeholder="Ex: Ana Silva")
    email = st.text_input("E-mail Corporativo", placeholder="nome@empresa.com.br")
    senha = st.text_input("Senha de Acesso", type="password", help="Mínimo 8 caracteres, contendo maiúscula e número.")
    
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="Concluir Cadastro", use_container_width=True, type="primary")

# ==========================================
# PROCESSAMENTO DO FORMULÁRIO
# ==========================================
if submit_button:
    # Sanitização dos campos
    nome = nome.strip()
    email = email.strip()

    # Validações dos campos
    if not nome or not email or not senha:
        st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
    elif not is_valid_email(email):
        st.error("❌ E-mail inválido. Por favor, insira um e-mail correto.")
    else:
        is_strong, pass_msg = evaluate_password_strength(senha)
        if not is_strong:
            st.warning(f"⚠️ {pass_msg}")
        else:
            # Hash seguro da senha
            senha_hashed = hash_password(senha)
            
            payload = {
                "nome": nome,
                "email": email,
                "senha": senha_hashed
            }
            
            with st.spinner("🔒 Criptografando e enviando dados com segurança..."):
                try:
                    # Envio HTTP POST com timeout seguro de 10s
                    response = requests.post(
                        APPS_SCRIPT_URL,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        if res_data.get("result") == "success":
                            st.success("✅ **Cadastro realizado com sucesso!** Suas credenciais foram registradas.")
                        else:
                            st.error(f"❌ **Falha no processamento:** {res_data.get('error', 'Erro desconhecido no servidor.')}")
                    else:
                        st.error(f"⚠️ Servidor retornou código HTTP {response.status_code}. Tente novamente mais tarde.")
                        
                except requests.exceptions.Timeout:
                    st.error("⏱️ Tempo limite de conexão excedido. Verifique sua conexão com a internet.")
                except requests.exceptions.RequestException as e:
                    st.error("🔌 Erro na comunicação com o servidor de banco de dados.")

st.markdown("<div class='footer-text'>Sistema Corporativo Protegido • Hash SHA-256 Enabled</div>", unsafe_allow_html=True)