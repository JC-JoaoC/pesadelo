import streamlit as st
import pandas as pd
from utils import get_session
from setup_db import Funcionario, Roster

st.set_page_config(page_title="Editar Escalas", layout="wide")
st.title("Editar e Visualizar Escalas")

session = get_session()
user_turno = st.session_state.get("user_turno", "Admin")

# Dashboard metrics
st.write("### Dashboard de Escalas")
if user_turno == "Admin":
    rosters = session.query(Roster).all()
else:
    rosters = session.query(Roster).filter_by(turno=user_turno).all()

col1, col2, col3 = st.columns(3)
col1.metric("Total de Escalas", len(rosters))
completes = sum(1 for r in rosters if r.status == "Completa")
col2.metric("Escalas Completas", completes)
col3.metric("Escalas Incompletas", len(rosters) - completes)

st.divider()

if not rosters:
    st.info("Nenhuma escala encontrada.")
else:
    # Selector
    roster_options = {f"{r.data_escala} - Turno {r.turno} ({r.status})": r for r in rosters}
    selected_roster_name = st.selectbox("Selecione uma Escala para Editar", list(roster_options.keys()))
    r = roster_options[selected_roster_name]
    
    st.write(f"Editando Escala: **{r.data_escala}** | Turno: **{r.turno}**")

    # Options for autocomplete
    empos = session.query(Funcionario).filter_by(turno=r.turno).all()
    options = [""] + [f"{e.matricula} - {e.nome_curto}" for e in empos]
    
    df = pd.DataFrame(r.data)
    
    column_config = {
        "Posto": st.column_config.TextColumn("Posto", disabled=True)
    }
    for i in range(1, 7):
        func_col = f"FUNÇÃO {i}"
        if func_col not in df.columns:
            df[func_col] = "" # ensure column exists
        column_config[func_col] = st.column_config.SelectboxColumn(
            func_col,
            help="Selecione o funcionário",
            options=options
        )

    edited_df = st.data_editor(
        df,
        column_config=column_config,
        hide_index=True,
        num_rows="dynamic",
        use_container_width=True,
        key=f"editor_{r.id}"
    )

    colA, colB = st.columns([1, 8])
    with colA:
        if st.button("Salvar Alterações", type="primary"):
            data_json = edited_df.to_dict(orient="records")
            r.data = data_json
            session.commit()
            st.success("Alterações salvas com sucesso!")
            
    with colB:
        # Generate HTML table for print
        html_table = edited_df.to_html(index=False, classes="table table-bordered style='width:100%; border-collapse: collapse; text-align: center;'")
        html_content = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>Escala {r.data_escala} - {r.turno}</title>
            <style>
                table, th, td {{ border: 1px solid black; border-collapse: collapse; padding: 5px; }}
                th {{ background-color: #f2f2f2; text-align: center; }}
                body {{ font-family: Arial, sans-serif; }}
                h2 {{ text-align: center; }}
            </style>
        </head>
        <body>
            <h2>Escala de Trabalho - Turno {r.turno}</h2>
            <h3>Data: {r.data_escala}</h3>
            {html_table}
        </body>
        </html>
        """
        st.download_button(
            label="📄 Imprimir / Download HTML",
            data=html_content,
            file_name=f"escala_{r.turno}_{r.data_escala}.html",
            mime="text/html"
        )

session.close()
