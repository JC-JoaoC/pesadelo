import streamlit as st
from auth import login, logout, is_authenticated

def main():
    if not is_authenticated():
        st.markdown(
            """
            <style>
                [data-testid="stSidebar"] { display: none; }
                [data-testid="collapsedControl"] { display: none; }
                [data-testid="InputInstructions"] { display: none; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        login()
        return

    user_cpf = st.session_state["user_cpf"]
    user_turno = st.session_state["user_turno"]

    st.sidebar.title(f"Bem-vindo, {user_turno}")
    if st.sidebar.button("Sair"):
        logout()

    pages = {
        "Menu Principal": [
            st.Page("pages/1_Criar_Escala.py", title="Criar Escala", icon="📝"),
            st.Page("pages/2_Editar_Escalas.py", title="Editar Escalas", icon="✏️"),
            st.Page("pages/3_Editar_Funcionarios.py", title="Editar Funcionários", icon="👥"),
        ]
    }

    if user_turno == "Admin":
        pages["Administração"] = [
            st.Page("pages/4_Editar_Login.py", title="Gerenciar Logins", icon="⚙️")
        ]

    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main()