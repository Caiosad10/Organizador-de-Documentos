import calendar 
import streamlit as st
from gotrue import SyncGoTrueClient
from postgrest import SyncPostgrestClient
from storage3 import SyncStorageClient
from datetime import date

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

def tela_login():
    st.title("Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
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
    st.title("Cadastro")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        try:
            res = auth.sign_up({
                "email": email,
                "password": senha
            })
            st.success("Usuário cadastrado! Faça login para continuar.")

        except Exception as e:
            st.error(f'Erro ao registrar usuário: {e}' )

def tela_autenticacao():
    escolha = st.radio("Selecione", ["Login", "Criar Conta"])

    if escolha == "Login":
        tela_login()
    else:
        tela_cadastro()

def main():
    if st.session_state["user"] is None:
        tela_autenticacao()
    else:
        user = st.session_state["user"]
        st.write("Usuario logado:", user.email)
        st.write("Aqui vai o conteúdo protegido da aplicação")
        

if __name__ == "__main__":
    main()