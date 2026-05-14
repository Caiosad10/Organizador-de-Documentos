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

/* HEADER PREMIUM ABAIXO DA BARRA DO STREAMLIT */
.custom-header {
    max-width: 400px;
    margin: auto;
    padding: 28px 26px;
    background: rgba(15, 23, 42, 0.55);
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
}

/* Conteúdo interno */
.custom-header-content {
    display: inline-flex;
    align-items: center;
    gap: 12px;
}

/* Ícone minimalista */
.header-icon {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid #e5e7eb;
    position: relative;
}

.header-icon::before,
.header-icon::after {
    content: "";
    position: absolute;
    left: 4px;
    right: 4px;
    height: 2px;
    background: #e5e7eb;
    border-radius: 2px;
}

.header-icon::before {
    top: 6px;
}

.header-icon::after {
    top: 12px;
}

/* Nome do projeto */
.custom-header-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 0.5px;
    font-family: "Segoe UI", system-ui, sans-serif;
}
            
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
    margin-bottom: 22px;
}
            
/* Botão Selecionar integrado ao card */
.month-select-btn > button {
    width: 100%;
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(148, 163, 184, 0.35);
    color: #e5e7eb;
    border-radius: 14px;
    padding: 6px 0;
    font-size: 0.85rem;
    margin-top: 6px;
    transition: all 0.18s ease-out;
}

.month-select-btn > button:hover {
    background: rgba(30, 41, 59, 0.9);
    border-color: rgba(59, 130, 246, 0.8);
    box-shadow: 0 6px 18px rgba(59, 130, 246, 0.25);
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

/* Inputs menores */
.stTextInput input {
    height: 36px;
    font-size: 0.9rem;
    padding: 6px 10px;
}

/* Botão de login compacto */
.stButton > button {
    height: 38px;
    font-size: 0.9rem;
    border-radius: 10px;
    padding: 0 14px;
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
.stButton > button {
    background: #1e293b;
    border: 1px solid rgba(148, 163, 184, 0.35);
    color: #e2e8f0;
    padding: 8px 14px;
    border-radius: 12px;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #334155;
    border-color: rgba(96, 165, 250, 0.8);
    color: #f8fafc;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.4);
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

st.markdown("""
<div class="custom-header">
    <div class="custom-header-content">
        <div class="header-icon"></div>
        <div class="custom-header-title">Organizador de Documentos</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Empurra o conteúdo para baixo (por causa da barra do Streamlit)
st.write("<br><br>", unsafe_allow_html=True)


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

if "mes_selecionado" not in st.session_state:
    st.session_state["mes_selecionado"] = None

if "dia_selecionado" not in st.session_state:
    st.session_state["dia_selecionado"] = None

def tela_login():

    with st.container():
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)

        st.markdown("<h1 class='main-title' style='text-align:center;'>Login</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle' style='text-align:center;'>Acesse seu painel de documentos organizados.</p>", unsafe_allow_html=True)

        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")

        st.write("")
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

        st.markdown("</div>", unsafe_allow_html=True)

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

MESES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def obter_status_mes(ano: int, mes: int):
    return {
        "dias_com_docs": 0,
        "pendencias": 0,
        "status": "empty"
    }

def dashboard_meses():
    hoje = date.today()
    ano_atual = hoje.year

    st.markdown("<h1 class='main-title'>Seu ano em documentos</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Escolha um mês para visualizar e organizar seus comprovantes, notas e documentos.</p>", unsafe_allow_html=True)

    cols = st.columns(4)

    for idx, nome_mes in enumerate(MESES_PT, start=1):
        col = cols[(idx - 1) % 4]
        with col:
            info = obter_status_mes(ano_atual, idx)

            if info["status"] == "ok":
                status_class = "status-ok"
                status_text = "Tudo em dia"
            elif info["status"] == "pending":
                status_class = "status-pending"
                status_text = "Pendências abertas"
            else:
                status_class = "status-empty"
                status_text = "Nenhum documento ainda"
                

            card_html = f"""
                <div class="month-card" onclick="window.location.href='?mes={idx}'">
                    <div class="month-badge">
                        <span>📅</span>
                        <span>{ano_atual}</span>
                    </div>
                    <div class="month-name">{nome_mes}</div>
                    <div class="month-status">
                        <span>{info["dias_com_docs"]} dias com documentos</span><br/>
                        <span>{info["pendencias"]} pendências</span>
                    </div>
                    <div style="margin-top:10px;">
                        <span class="status-pill {status_class}">
                        {status_text}
                        </span>
                    </div>
                </div>
                """

            st.markdown(card_html, unsafe_allow_html=True)
            
            if st.button("Selecionar", key=f"mes-{idx}", help=nome_mes, type="secondary"):
                st.session_state["mes_selecionado"] = idx
                st.session_state["dia_selecionado"] = None
                st.rerun()

    query_params = st.query_params
    if "mes" in query_params:
        st.session_state["mes_selecionado"] = int(query_params["mes"])
        st.rerun()

    

def tela_calendario_mes():
    mes = st.session_state["mes_selecionado"]
    hoje = date.today()
    ano = hoje.year

    cal = calendar.monthcalendar(ano, mes)

    st.markdown(
        f"<h1 class='main-title'>📅 {MESES_PT[mes-1]} {ano}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p class='subtitle'>Selecione um dia para gerenciar os documentos.</p>",
        unsafe_allow_html=True
    )

    dias_semana = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
    cols = st.columns(7)
    for i, dia in enumerate(dias_semana):
        cols[i].markdown(
            f"<div class='weekday-label'>{dia}</div>",
            unsafe_allow_html=True
        )

    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].write(" ")
            else:
                with cols[i]:
                    st.markdown("<div class='day-card'>", unsafe_allow_html=True)
                    if st.button(str(dia), key=f"dia-{dia}", use_container_width=True):
                        st.session_state["dia_selecionado"] = dia
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
            if st.button("⬅ Voltar aos meses", use_container_width=True):
                st.session_state["mes_selecionado"] = None
                st.session_state["dia_selecionado"] = None
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

def tela_do_dia():
    dia = st.session_state["dia_selecionado"]
    mes = st.session_state["mes_selecionado"]
    hoje = date.today()
    ano = hoje.year

    st.markdown(
        f"<h1 class='main-title'>📂 {dia:02d} de {MESES_PT[mes-1]} {ano}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p class='subtitle'>Aqui você poderá enviar e visualizar os documentos deste dia.</p>",
        unsafe_allow_html=True
    )

    st.info("Aqui futuramente entra o upload real, listagem de documentos e status do dia.")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.button("📤 Upload Documento", use_container_width=True)
    with col2:
        st.button("📁 Ver Documentos", use_container_width=True)

    st.write("")
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("⬅ Voltar ao calendário", use_container_width=True):
        st.session_state["dia_selecionado"] = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    if st.session_state["user"] is None:
        tela_autenticacao()
    else:
        if st.session_state["mes_selecionado"] is None:
            dashboard_meses()
        elif st.session_state["dia_selecionado"] is None:
            tela_calendario_mes()
        else:
            tela_do_dia()
        

if __name__ == "__main__":
    main()