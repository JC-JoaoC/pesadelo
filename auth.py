import streamlit as st
from werkzeug.security import check_password_hash
from utils import get_session
from setup_db import User

def login():
    st.set_page_config(page_title="Sistema de Escalas", layout="centered")
    st.title("Sistema de Gestão de Escalas")
    
    with st.form("login_form"):
        cpf = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            session = get_session()
            user = session.query(User).filter_by(cpf=cpf).first()
            session.close()
            
            if user and check_password_hash(user.password_hash, password):
                st.session_state["authenticated"] = True
                st.session_state["user_cpf"] = user.cpf
                st.session_state["user_turno"] = user.turno
                st.session_state["user_id"] = user.id
                st.rerun()
            else:
                st.error("CPF ou Senha incorretos.")

def logout():
    for key in ["authenticated", "user_cpf", "user_turno", "user_id"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def is_authenticated():
    return st.session_state.get("authenticated", False)
