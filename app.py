import calendar 
import streamlit as st

from gotrue import SyncGoTrueClient
from postgrest import SyncPostgrestClient
from storage3 import SyncStorageClient
from datetime import date

#Estilização 

st.set_page_config(
    page_title="Calendario",
    page_icon="📅",
    layout="centered"
)

st.markdown("""
<style>

/* Fundo geral */
.stApp {
    background: linear-gradient(135deg, #0b1220, #0e1117);
    color: white;
}

/* Remove padding exagerado */
.block-container {
    padding-top: 4rem;
}

/* Título */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

/* Subtitulo */
.month-title {
    text-align: center;
    font-size: 1.5rem;
    color: #cbd5e1;
    margin-bottom: 2rem;
}

/* Grid do calendário */
.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 14px;
    max-width: 700px;
    margin: auto;
}

/* Card dos dias */
.day-card button {
    width: 100%;
    height: 70px;

    border-radius: 20px;

    border: 1px solid rgba(255,255,255,0.08);

    background: rgba(17, 24, 39, 0.85);

    color: white;

    font-size: 18px;
    font-weight: 600;

    transition: all 0.2s ease-in-out;

    backdrop-filter: blur(10px);
}

/* Hover */
.day-card button:hover {
    transform: translateY(-4px) scale(1.03);

    border: 1px solid #3b82f6;

    background: rgba(30, 41, 59, 0.95);

    box-shadow: 0 8px 25px rgba(59,130,246,0.25);
}

/* Botão voltar */
.stButton > button {
    border-radius: 14px;
}

/* Inputs */
.stTextInput input {
    border-radius: 14px;
    background-color: #111827;
    color: white;
}

/* Radio */
.stRadio label {
    color: white;
}

</style>
""", unsafe_allow_html=True)


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

AUTH_URL = f'{SUPABASE_URL}/auth/v1'
REST_URL = f'{SUPABASE_URL}/rest/v1'
STORAGE_URL = f'{SUPABASE_URL}/storage/v1'

auth = SyncGoTrueClient(url = AUTH_URL, headers={"apikey": SUPABASE_KEY})
db = SyncPostgrestClient(REST_URL, headers={"apikey": SUPABASE_KEY})
storage = SyncStorageClient(STORAGE_URL, headers={"apikey": SUPABASE_KEY})


if "user" not in st.session_state:
    st.session_state["user"] = None

if "session" not in st.session_state:
    st.session_state["session"] = None

if "dia_selecionado" not in st.session_state:
    st.session_state["dia_selecionado"] = None

def tela_login():
    st.markdown("<h1 class='main-title'>Login</h1>", unsafe_allow_html=True)
    

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):
        try:
            res = auth.sign_in_with_password({
                "email": email,
                "password": senha
            })
            st.session_state["user"] = res.user
            st.session_state["session"] = res.session
            st.rerun()
            
        except Exception as e:
            st.error(f"Email ou senha incorretos: {e}")

def tela_cadastro():
    st.markdown("<h1 class='main-title'>Cadastro</h1>", unsafe_allow_html=True)

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar", use_container_width=True):
        try:
            res = auth.sign_up({
                "email": email,
                "password": senha
            })
            st.success("Usuário cadastrado! Faça login para continuar.")

        except Exception as e:
            st.error(f'Erro ao registrar usuário: {e}' )

def tela_autenticacao():
    escolha = st.radio("Selecione", ["Login", "Criar Conta"], horizontal=True)

    st.divider()

    if escolha == "Login":
        tela_login()
    else:
        tela_cadastro()

def dashbord():
    st.markdown("<h1 class='main-title'>📅 Calendário de Documentos</h1>", unsafe_allow_html=True)



    hoje = date.today()
    ano = hoje.year
    mes = hoje.month

    cal = calendar.monthcalendar(ano, mes)

    st.markdown(f"<div class ='month-title'>{calendar.month_name[mes]} {ano}</div>", unsafe_allow_html=True)

    dias_semana= ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]

    cols = st.columns(7)

    for i, dia in enumerate(dias_semana):
        cols[i].markdown(
            f"<div style='text-align:center; color:#94a3b8; font-weight:600'>{dia}</div>", unsafe_allow_html=True
        )

    st.write("")

    for semana in cal:
        cols = st.columns(7)

        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].write("")
            else:
                with cols[i]:
                    st.markdown("<div class='day-card'>", unsafe_allow_html=True)

                    if st.button(str(dia), key=f'dia-{dia}',use_container_width=True):

                        st.session_state["dia_selecionado"] = dia
                        st.rerun()

                    st.markdown("</div>", unsafe_allow_html=True)

def tela_do_dia():
    dia = st.session_state["dia_selecionado"]
    st.markdown(f"<h1 class='main-title'>📂 Dia {dia}</h1>", unsafe_allow_html=True)

    st.info("Aqui deve ser feito os uploads dos seus arquivos. Eles ficaram visiveis")

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.button("📤 Upload Documento", use_container_width=True)

    with col2:
        st.button("📁 Ver Documentos", use_container_width=True)

    st.write("")
    st.write("")


    if st.button("⬅ Voltar", use_container_width=True):
        st.session_state["dia_selecionado"] = None
        st.rerun()

def main():
    if st.session_state["user"] is None:
        tela_autenticacao()
    else:
        if st.session_state["dia_selecionado"] is None:
            dashbord()
        else:
            tela_do_dia()
        

if __name__ == "__main__":
    main()