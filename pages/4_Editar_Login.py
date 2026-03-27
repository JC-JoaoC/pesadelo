import streamlit as st
import pandas as pd
from werkzeug.security import generate_password_hash
from utils import get_session
from setup_db import User

st.set_page_config(page_title="Gerenciar Logins", layout="wide")

if st.session_state.get("user_turno") != "Admin":
    st.error("Acesso Negado. Apenas administradores podem acessar esta página.")
    st.stop()

st.title("Gerenciamento de Usuários do Sistema")

session = get_session()

# User List (READ and DELETE)
st.write("### Usuários Cadastrados")

users = session.query(User).all()
df_users = pd.DataFrame([{"ID": u.id, "CPF": u.cpf, "Turno": u.turno} for u in users])

if not df_users.empty:
    edited_df = st.data_editor(
        df_users,
        width="stretch",
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn(disabled=True),
            "CPF": st.column_config.TextColumn(disabled=True),
            "Turno": st.column_config.TextColumn(disabled=True)
        }
    )
    
    del_id = st.number_input("ID do Usuário para Deletar", min_value=0, step=1)
    if st.button("Deletar Usuário", type="primary"):
        u_del = session.query(User).filter_by(id=del_id).first()
        if u_del:
            if u_del.cpf == "admin":
                st.error("O usuário administrador principal não pode ser deletado.")
            else:
                session.delete(u_del)
                session.commit()
                st.success(f"Usuário ID {del_id} deletado com sucesso!")
                st.rerun()
        else:
            st.warning("Usuário não encontrado.")
            
st.divider()

# CREATE / UPDATE formularip
st.write("### Criar ou Atualizar Usuário")
st.write("Se o nome do usuário já existir, a senha do usuário e/ou o turno serão atualizados.")

with st.form("user_form"):
    cpf = st.text_input("Nome do Supervisor")
    turno = st.selectbox("Turno Associado", ["Admin", "Alfa", "Bravo", "Charlie", "Delta"])
    password = st.text_input("Senha", type="password")
    confirm_password = st.text_input("Confirmar Senha", type="password")
    
    submit = st.form_submit_button("Salvar Usuário")
    
    if submit:
        if not cpf or not password:
            st.error("CPF e Senha são obrigatórios.")
        elif password != confirm_password:
            st.error("As senhas não coincidem.")
        else:
            pw_hash = generate_password_hash(password)
            existing_user = session.query(User).filter_by(cpf=cpf).first()
            if existing_user:
                existing_user.password_hash = pw_hash
                existing_user.turno = turno
                st.success("Usuário atualizado com sucesso!")
            else:
                new_user = User(cpf=cpf, password_hash=pw_hash, turno=turno)
                session.add(new_user)
                st.success("Usuário criado com sucesso!")
            session.commit()
            st.rerun()

session.close()
