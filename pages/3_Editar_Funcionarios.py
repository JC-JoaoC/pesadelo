import streamlit as st
import pandas as pd
from utils import get_session
from setup_db import Funcionario

st.set_page_config(page_title="Editar Funcionários", layout="wide")
st.title("Gestão de Funcionários")

session = get_session()
user_turno = st.session_state.get("user_turno", "Admin")

# Dashboard 
st.write("### Distribuição da Força de Trabalho")

if user_turno == "Admin":
    st.info("Visualizando e editando funcionários (Modo Admin).")
    target_turno = st.selectbox("Filtrar por Turno", ["Todos", "Alfa", "Bravo", "Charlie", "Delta"])
    if target_turno == "Todos":
        empos = session.query(Funcionario).all()
    else:
        empos = session.query(Funcionario).filter_by(turno=target_turno).all()
else:
    st.info(f"Visualizando e editando funcionários do Turno: **{user_turno}**")
    empos = session.query(Funcionario).filter_by(turno=user_turno).all()
df_empos = pd.DataFrame([{
    "Matrícula": e.matricula,
    "Nome": e.nome_curto,
    "Função": e.funcao,
    "Turno": e.turno
} for e in empos])

if not df_empos.empty:
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Contagem por Função**")
        st.bar_chart(df_empos["Função"].value_counts())
    with col2:
        st.write("**Distribuição nos Turnos**")
        st.bar_chart(df_empos["Turno"].value_counts())

st.divider()

st.write("### Editar Cadastro de Funcionários")
st.caption("As edições feitas na tabela abaixo serão atualizadas no banco de dados.")

edited_df = st.data_editor(
    df_empos,
    key="empos_editor",
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Matrícula": st.column_config.NumberColumn("Matrícula", disabled=True),
        "Turno": st.column_config.SelectboxColumn("Turno", options=["Alfa", "Bravo", "Charlie", "Delta", "Admin"])
    }
)

if st.button("Salvar Alterações de Funcionários", type="primary"):
    # Determine updates/deletes/inserts based on differences.
    # The simplest reliable way for Streamlit is to clear and rewrite everything (if it's not huge),
    # or compare dataframes.
    # Since matricula is PK and disabled, we just update records.
    for index, row in edited_df.iterrows():
        emp = session.query(Funcionario).filter_by(matricula=row["Matrícula"]).first()
        if emp:
            emp.nome_curto = row["Nome"]
            emp.funcao = row["Função"]
            emp.turno = row["Turno"]
    session.commit()
    st.success("Dados dos funcionários atualizados!")

session.close()
