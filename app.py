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
    background: radial-gradient(circle at top, #1f2933 0, #020617 45%, #000 100%);
    color: #e5e7eb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
}

/* Container Principal */
.block-container {
    padding-top: 4rem;
    max-width: 1100px;
}

/* Título */
.main-title {
    text-align: left;
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}

/* Subtitulo */
.month-title {
    text-align: left;
    font-size: 1rem;
    color: #9ca3af;
    margin-bottom: 2rem;
}

/* Cards de Mes */
.month-card {
    background: linear-gradient(145deg, #111827, #020617);
    border-radius: 22px;
    padding: 18px 18px 16px 18px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.75);
    transition: all 0.18s ease-out;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

/* Glow suave no hover */
.month-card: hover {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #e5e7eb;
    background: rgba(15, 23, 42, 0.9);
    border-radius: 999px;
    padding: 4px 10px;
    border: 1px solid rgba(148, 163, 184, 0.4);
}

/* Nome do mes */
.month-name {
    margin-tpo´: 10px;
    font-size: 1.15rem;
    font-weight: 700;
}

/* Linha de status */
.month-status {
    margin-top: 6px;
    font-size: 0.85rem;
    color: #9ca3af;
}

/* Pílulas de status */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    padding: 3px 9px;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    background: rgba(15, 23, 42, 0.85);
    color: #e5e7eb;
}
            
/* Cores de status */
.status-ok {
    border-color: rgba(34, 197, 94, 0.7);
    color: #bbf7d0;
}
.status-pending {
    border-color: rgba(234, 179, 8, 0.7);
    color: #fef9c3;
}
.status-empty {
    border-color: rgba(148, 163, 184, 0.5);
    color: #e5e7eb;
}

/* Botões gerais */
.stButton > button {
    border-radius: 999px;
    background: #2563eb;
    color: white;
    border: none;
    padding: 0.5rem 1.1rem;
    font-weight: 600;
}
.stButton > button:hover {
    background: #1d4ed8;
}

/* Inputs */
.stTextInput input {
    border-radius: 14px;
    background-color: #020617;
    color: white;
    border: 1px solid #1f2937;
}

/* Radio */
.stRadio label {
    color: #e5e7eb;
}
            
/* Calendário: grid de dias */
.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 10px;
    margin-top: 1rem;
}

/* Botão de dia */
.day-card button {
    width: 100%;
    height: 60px;
    border-radius: 18px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    background: rgba(15, 23, 42, 0.9);
    color: #e5e7eb;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.16s ease-out;
}
.day-card button:hover {
    transform: translateY(-3px);
    border-color: rgba(59, 130, 246, 0.9);
    box-shadow: 0 14px 30px rgba(37, 99, 235, 0.45);
}

/* Cabeçalho dos dias da semana */
.weekday-label {
    text-align: center;
    color: #9ca3af;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}

/* Botão voltar */
.back-btn > button {
    background: transparent;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.5);
    color: #e5e7eb;
}
.back-btn > button:hover {
    background: rgba(15, 23, 42, 0.9);
}

/* Info box */
.stAlert {
    border-radius: 18px;
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
    st.markdown("<p class='subtitle'>Acesse seu painel de documentos organizados.</p>", unsafe_allow_html=True)
    

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True) and email and senha:
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
    st.markdown("<p class='subtitle'>Cadastre-se para começar a organizar seus documentos.</p>", unsafe_allow_html=True)

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar", use_container_width=True) and email and senha:
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