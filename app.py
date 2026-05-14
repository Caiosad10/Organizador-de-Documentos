import calendar 
import streamlit as st

from gotrue import SyncGoTrueClient
from postgrest import SyncPostgrestClient
from storage3 import SyncStorageClient
from datetime import date
import uuid

#Confifuração da pagina

st.set_page_config(
    page_title="Organizador Financeiro",
    page_icon="📂",
    layout="centered"
)

#Estilização

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

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
    background: radial-gradient(circle at top, #0f1f3d 0%, #020617 50%, #000 100%);
    color: #e5e7eb;
    font-family: 'DM Sans', system-ui, sans-serif;
}

/* Container Principal */
.block-container {
    padding-top: 2rem;
    max-width: 1000px;
}

/* Esconde barra superior do streamlit */            
header[data-testid="stHeader"] {
    background: transparent;            
}

/* HEADER */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: rgba(15, 31, 61, 0.6);
    border-radius: 18px;
    border: 1px solid rgba(59, 130, 246, 0.15);
    backdrop-filter: blur(12px);
    margin-bottom: 2rem;
}            

.app-header-title {
    font-size: 1rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 0.3px            
}
            
.app-header-user {
    font-size: 0.8rem;
    color: #64748b;
}

/* Título */
.main-title {
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.25rem;
}
            
.subtitle {
    font-size: 0.9rem;
    color: #64748b;
    margin-bottom: 2rem;
}

/* Cards de Mes */
.month-card {
    background: linear-gradient(145deg, #0f1f3d, #060f1e);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(59, 130, 246, 0.12);
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.4);
    min-height: 130px;
    margin-bottom: 16px;
}

/* Nome do mes */
.month-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 6px;
}
            
.month-year {
    font-size: 0.75rem;
    color: #475569;
    margin-bottom: 12px;
}

/* Linha de status */
.month-status {
    margin-bottom: 10px;
    font-size: 0.8rem;
    color: #64748b;
}

/* Pílulas de status */
.status-pill {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    border: 1px solid;
}
            
/* Cores de status */
.status-ok {
    border-color: rgba(34, 197, 94, 0.5);
    color: #86efac;
    background: rgba(34, 197, 94, 0.08);
}
.status-pending {
    border-color: rgba(234, 179, 8, 0.5);
    color: #fde047;
    background: rgba(234, 179, 8, 0.08);
}

.status-urgent {
    border-color: rgba(239, 68, 68, 0.5);
    color: #fca5a5;
    background: rgba(239, 68, 68, 0.08);
}

.status-empty {
    border-color: rgba(100, 116, 139, 0.4);
    color: #94a3b8;
    background: rgba(100, 116, 139, 0.06);
}

/* Botões gerais */
.stButton > button {
    border-radius: 12px;
    background: rgba(37, 99, 235, 0.15);
    color: #93c5fd;
    border: 1px solid rgba(59, 130, 246, 0.3);
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.15 ease;
}
.stButton > button:hover {
    background: rgba(37, 99, 235, 0.3);
    border-color: rgba(59, 130, 246, 0.7);
    color: #bfdbfe;
    box-shadow: 0 0 16px rgba(59, 130, 246, 0.2);
}

/* ── INPUTS ── */
.stTextInput input, .stSelectbox select {
    background: rgba(15, 31, 61, 0.8);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 10px;
    color: #e5e7eb;
    font-size: 0.9rem;
}
 
.stTextInput input:focus {
    border-color: rgba(59, 130, 246, 0.6);
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
}

/* ── LOGIN ── */
.login-wrap {
    max-width: 380px;
    margin: 3rem auto 0 auto;
}

/* Botão primário (Entrar, Cadastrar) */
.btn-primary > button {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 12px;
}
            
.btn-primary > button:hover {
    background: #1d4ed8;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4);
}
            
/* ── RADIO ── */
.stRadio label {
    color: #94a3b8;
    font-size: 0.9rem;
}
            
/* ── DIVIDER ── */
hr {
    border-color: rgba(59, 130, 246, 0.1);
    margin: 1.5rem 0;
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

/* ── CALENDÁRIO ── */
.weekday-label {
    text-align: center;
    color: #475569;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 6px 0;
}
 
.day-empty {
    height: 44px;
}

/* Botão de voltar */
.btn-back > button {
    background: transparent;
    border: 1px solid rgba(100, 116, 139, 0.3);
    color: #64748b;
    font-size: 0.8rem;
}
            
.btn-back > button:hover {
    border-color: rgba(100, 116, 139, 0.6);
    color: #94a3b8;
}

/* ── ALERTAS ── */
.stAlert {
    border-radius: 14px;
    font-size: 0.85rem;
}
            
            /* ── DOCUMENTO CARD ── */
.doc-card {
    background: rgba(15, 31, 61, 0.5);
    border: 1px solid rgba(59, 130, 246, 0.12);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
 
.doc-card-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #cbd5e1;
    margin-bottom: 4px;
}
 
.doc-card-meta {
    font-size: 0.75rem;
    color: #475569;
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

def get_db():
    token = st.session_state["session"].access_token
    return SyncPostgrestClient(REST_URL, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}"
    })

def get_storage():
    token = st.session_state["session"].access_token
    return SyncStorageClient(STORAGE_URL, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}"
    })

# SESSION STATE - Inicializa variaves de controle

defaults = {
    "user": None,
    "session": None,
    "mes_selecionado": None,
    "dia_selecionado": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# CONSTANTES

MESES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

TIPOS_DOCUMENTO = ["comprovante", "boleto", "nota_fiscal", "PC", "recibo", "outro"]

BUCKET = "documents"

# Header com Perfil

def render_header():
    user = st.session_state["user"]
    email = user.email if user else ""

    col_title, col_user = st.columns([3, 1])

    with col_title:
        st.markdown("""
            <div style="padding: 14px 0 6px 0;">
                <span style="font-size:1rem; font-weight:700; color:#f1f5f9;">📂 Organizador Financeiro</span>
            </div>
        """, unsafe_allow_html=True)

    with col_user:
        with st.expander(f"👤 Perfil"):
            st.markdown(f"<span style='font-size:0.8rem; color:#64748b;'>{email}</span>", unsafe_allow_html=True)
            st.write("")
            if st.button("Sair", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
 
    st.divider()

# AUTENTICAÇÃO

def tela_login():

    with st.container():
        st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)

        st.markdown("<h2 class='main-title'>Login</h2>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Acesse seu painel de documentos organizados.</p>", unsafe_allow_html=True)

        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")

        st.write("")
        st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
        if st.button("Entrar", use_container_width=True):
            if email and senha:
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
            else:
                st.warning("Preencha email e senha")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def tela_cadastro():
    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown("<h2 class='main-title'>Criar Conta</h2>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Cadastre-se para começar a organizar seus documentos.</p>", unsafe_allow_html=True)

    email = st.text_input("Email", key="cad_email")
    senha = st.text_input("Senha", type="password", key="cad_senha")
    st.write("")

    st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
    if st.button("Cadastrar", use_container_width=True):
        if email and senha:
            try:
                auth.sign_up({"email": email, "password": senha})
                st.success("Usuário cadastrado! Faça login para continuar.")

            except Exception as e:
                st.error(f'Erro ao registrar usuário: {e}' )
        else:
            st.warning("Preencha todos os campos.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def tela_autenticacao():
    st.markdown("<br>", unsafe_allow_html=True)
    escolha = st.radio("", ["Login", "Criar Conta"], horizontal=True, label_visibility="collapsed")
    st.divider()

    if escolha == "Login":
        tela_login()
    else:
        tela_cadastro()

# DADOS DO BANCO

def obter_status_mes(ano: int, mes: int) -> dict:
    try:
        db = get_db()
        hoje = date.today()

        inicio = f"{ano}-{mes:02d}-01"
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        fim = f"{ano}-{mes:02d}-{ultimo_dia}"

        res = (
            db.table("documents")
            .select("id, date, type")
            .gte("date", inicio)
            .lte("date", fim)
            .execute()
        )

        docs = res.data if res.data else []

        if not docs:
            return {"dias_com_docs": 0, "pendencias": 0, "status": "empty"}
        
        # Dias únicos que têm algum documento
        dias_com_docs = len(set(d["date"] for d in docs))
 
        # IDs de comprovantes do mês
        ids_comprovantes = [d["id"] for d in docs if d["type"] == "comprovante"]
 
        pendencias = 0
        if ids_comprovantes:
            # Busca quais comprovantes têm pelo menos um vínculo
            links_res = (
                db.table("links")
                .select("comprovante_id")
                .in_("comprovante_id", ids_comprovantes)
                .execute()
            )
            ids_com_link = set(l["comprovante_id"] for l in (links_res.data or []))
            pendencias = len([i for i in ids_comprovantes if i not in ids_com_link])

        # Define status baseado no dia do mês e pendências
        if pendencias == 0:
            status = "ok" if ids_comprovantes else "empty"
        elif hoje.month == mes and hoje.year == ano and hoje.day >= 28:
            status = "urgent"
        elif hoje.month == mes and hoje.year == ano and hoje.day >= 25:
            status = "pending"
        else:
            status = "pending"
 
        return {"dias_com_docs": dias_com_docs, "pendencias": pendencias, "status": status}
 
    except Exception:
        return {"dias_com_docs": 0, "pendencias": 0, "status": "empty"}    

# DASHBOARD - MES

def dashboard_meses():
    render_header()

    hoje = date.today()
    ano_atual = hoje.year

    st.markdown("<h1 class='main-title'>Seu ano em documentos</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Escolha um mês para visualizar e organizar seus comprovantes, notas e documentos.</p>", unsafe_allow_html=True)

    # Alerta de urgência — aparece se o mês atual já passou do dia 28
    if hoje.day >= 28:
        st.error(f"⚠️ Fechamento de {MESES_PT[hoje.month - 1]} se aproxima! Verifique as pendências.")
    elif hoje.day >= 25:
        st.warning(f"📋 Faltam poucos dias para o fechamento de {MESES_PT[hoje.month - 1]}. Confira os documentos pendentes.")

    cols = st.columns(4)

    for idx, nome_mes in enumerate(MESES_PT, start=1):
        col = cols[(idx - 1) % 4]
        with col:
            info = obter_status_mes(ano_atual, idx)

            status_map = {
                "ok":      ("status-ok",      "✓ Tudo em dia"),
                "pending": ("status-pending", "⚠ Pendências"),
                "urgent":  ("status-urgent",  "🔴 Urgente"),
                "empty":   ("status-empty",   "— Sem documentos"),
            }
            status_class, status_text = status_map[info["status"]]
                

            st.markdown(f"""
                <div class="month-card">
                    <div class="month-year">{ano_atual}</div>
                    <div class="month-name">{nome_mes}</div>
                    <div class="month-stats">
                        {info["dias_com_docs"]} dias com documentos<br/>
                        {info["pendencias"]} pendência(s)
                    </div>
                    <span class="status-pill {status_class}">{status_text}</span>
                </div>
            """, unsafe_allow_html=True)
 
            if st.button("Abrir", key=f"mes-{idx}", use_container_width=True):
                st.session_state["mes_selecionado"] = idx
                st.session_state["dia_selecionado"] = None
                st.rerun()


def tela_calendario_mes():
    render_header()

    mes = st.session_state["mes_selecionado"]
    hoje = date.today()
    ano = hoje.year

    cal = calendar.monthcalendar(ano, mes)

    st.markdown(
        f"<h1 class='main-title'>{MESES_PT[mes-1]} {ano}</h1>",
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

    try:
        db = get_db()
        inicio = f"{ano}-{mes:02d}-01"
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        fim = f"{ano}-{mes:02d}-{ultimo_dia}"
        res = db.table("documents").select("date").gte("date", inicio).lte("date", fim).execute()
        dias_com_doc = set(
            int(d["date"].split("-")[2]) for d in (res.data or [])
        )
    except Exception:
        dias_com_doc = set()

    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            with cols[i]:
                if dia == 0:
                    st.markdown("<div class='day-empty'></div>", unsafe_allow_html=True)
                else:
                    # Indicador visual se o dia já tem documentos
                    indicador = " 🔵" if dia in dias_com_doc else ""
                    label = f"{dia}{indicador}"
                    if st.button(label, key=f"dia-{dia}", use_container_width=True):
                        st.session_state["dia_selecionado"] = dia
                        st.rerun()

    st.write("")
    st.markdown("<div class='btn-back'>", unsafe_allow_html=True)
    if st.button("← Voltar aos meses", use_container_width=True):
        st.session_state["mes_selecionado"] = None
        st.session_state["dia_selecionado"] = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Tela do dia

def fazer_upload(arquivo, user_id: str, data: str, tipo: str) -> str | None:
    
    try:
        storage = get_storage()
        extensao = arquivo.name.split(".")[-1]
        nome_arquivo = f"{uuid.uuid4()}.{extensao}"
        caminho = f"{user_id}/{data}/{nome_arquivo}"
 
        storage.from_(BUCKET).upload(
            path=caminho,
            file=arquivo.getvalue(),
            file_options={"content-type": arquivo.type}
        )
        return caminho
    except Exception as e:
        st.error(f"Erro no upload: {e}")
        return None
 
def salvar_documento(user_id: str, data: str, tipo: str, file_path: str):
    
    try:
        db = get_db()
        db.table("documents").insert({
            "user_id": user_id,
            "date": data,
            "type": tipo,
            "file_path": file_path,
            "tags": []
        }).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar no banco: {e}")
        return False
 
def listar_documentos_do_dia(data: str) -> list:
    
    try:
        db = get_db()
        res = db.table("documents").select("*").eq("date", data).order("created_at").execute()
        return res.data or []
    except Exception:
        return []

def tela_do_dia():
    render_header()

    dia = st.session_state["dia_selecionado"]
    mes = st.session_state["mes_selecionado"]
    hoje = date.today()
    ano = hoje.year
    data_str = f"{ano}-{mes:02d}-{dia:02d}"
    user_id = str(st.session_state["user"].id)

    st.markdown(
        f"<h1 class='main-title'>📂 {dia:02d} de {MESES_PT[mes-1]} {ano}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p class='subtitle'>Gerencie os documentos deste dia.</p>",
        unsafe_allow_html=True
    )

    with st.expander("➕ Adicionar documento", expanded=False):
        tipo = st.selectbox("Tipo do documento", TIPOS_DOCUMENTO)
        arquivo = st.file_uploader(
            "Selecione o arquivo",
            type=["pdf", "png", "jpg", "jpeg"],
            key=f"upload-{data_str}"
        )
 
        st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
        if st.button("Salvar documento", use_container_width=True):
            if arquivo:
                with st.spinner("Enviando..."):
                    caminho = fazer_upload(arquivo, user_id, data_str, tipo)
                    if caminho:
                        ok = salvar_documento(user_id, data_str, tipo, caminho)
                        if ok:
                            st.success("Documento salvo com sucesso!")
                            st.rerun()
            else:
                st.warning("Selecione um arquivo antes de salvar.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("**Documentos do dia**")
    docs = listar_documentos_do_dia(data_str)

    if not docs:
        st.markdown(
            "<p style='color:#475569; font-size:0.85rem;'>Nenhum documento adicionado ainda.</p>",
            unsafe_allow_html=True
        )
    else:
        # Separa comprovantes dos demais
        comprovantes = [d for d in docs if d["type"] == "comprovante"]
        vinculados   = [d for d in docs if d["type"] != "comprovante"]

    if comprovantes:
            st.markdown(
                "<p style='font-size:0.8rem; color:#64748b; margin-bottom:6px;'>COMPROVANTES</p>",
                unsafe_allow_html=True
            )
            for doc in comprovantes:
                nome = doc["file_path"].split("/")[-1]
                st.markdown(f"""
                    <div class="doc-card">
                        <div class="doc-card-title">🧾 {nome}</div>
                        <div class="doc-card-meta">Adicionado em {doc["created_at"][:10]}</div>
                    </div>
                """, unsafe_allow_html=True)

    if vinculados:
            st.markdown(
                "<p style='font-size:0.8rem; color:#64748b; margin-bottom:6px; margin-top:14px;'>DOCUMENTOS VINCULADOS</p>",
                unsafe_allow_html=True
            )
            for doc in vinculados:
                nome = doc["file_path"].split("/")[-1]
                tipo_label = doc["type"].replace("_", " ").upper()
                st.markdown(f"""
                    <div class="doc-card">
                        <div class="doc-card-title">📄 {nome}</div>
                        <div class="doc-card-meta">{tipo_label} · {doc["created_at"][:10]}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='btn-back'>", unsafe_allow_html=True)
    if st.button("← Voltar ao calendário", use_container_width=True):
        st.session_state["dia_selecionado"] = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# MAIN

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