import streamlit as st
import pandas as pd
from utils import get_session
from setup_db import Funcionario, Roster

st.set_page_config(page_title="Editar Escalas", layout="wide")
st.title("Editar e Visualizar Escalas")

session = get_session()
user_turno = st.session_state.get("user_turno", "Admin")

# Dashboard
st.write("### Dashboard de Escalas")
if user_turno == "Admin":
    rosters = session.query(Roster).all()
else:
    rosters = session.query(Roster).filter(Roster.turno.like(f"{user_turno}%")).all()

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
    base_turno = r.turno.split(" - ")[0]
    
    st.write(f"Editando Escala: **{r.data_escala}** | Turno: **{r.turno}**")

    # Options for autocomplete
    empos = session.query(Funcionario).filter_by(turno=base_turno).all()
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
        width="stretch",
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
        user_cpf = st.session_state.get("user_cpf", "Sem CPF")
        dias_semana = {0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"}
        data_escala = r.data_escala
        dia_semana_str = dias_semana[data_escala.weekday()]
        target_turno = base_turno
        
        data_list = r.data
        selected_terminal = "Terminal 3" if len(data_list) > 0 and str(data_list[0].get("Posto", "")).startswith("T3") else "Terminal 2"
        terminal_indicador = "T3" if selected_terminal == "Terminal 3" else "T2"

        html_table = edited_df.to_html(index=False, classes="table table-bordered style='width:100%; border-collapse: collapse; text-align: center;'")
        html_content = f"""
<html>
<head>
    <meta charset="utf-8">
    <title>Escala {data_escala} - {target_turno}</title>
    <style>
        body {{ font-family: Arial, sans-serif; font-size: 12px; margin: 0; padding: 10px; }}
        .container {{ width: 100%; max-width: 1000px; margin: 0 auto; }}
        .header-box {{ border: 2px solid black; margin-bottom: 5px; }}
        .header-table {{ width: 100%; border-collapse: collapse; }}
        .header-table td {{ border: 1px solid black; padding: 10px; }}
        .logo-text {{ width: 25%; font-weight: bold; font-style: italic; font-size: 16px; text-align: center; }}
        .title-text {{ text-align: center; font-weight: bold; font-size: 18px; }}
        .info-row {{ width: 100%; border-collapse: collapse; margin-bottom: 15px; border: 2px solid black; }}
        .info-row td {{ border: 1px solid black; padding: 5px 10px; font-weight: bold; font-size: 12px; }}
        .info-label {{ text-transform: uppercase; font-size: 10px; color: #555; }}
        table {{ width: 100%; border: 2px solid black; border-collapse: collapse; }}
        th, td {{ border: 1px solid black; padding: 5px; text-align: center; height: 25px; font-size: 11px; }}
        th {{ background-color: ##f2f2f2; color: #333; }}
        .section-header {{ background-color: #333; color: white; font-weight: bold; text-align: center; padding: 5px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-box">
            <table class="header-table">
                <tr>
                    <td class="title-text">ESCALA DE POSTOS DIÁRIOS - {selected_terminal}</td>
                </tr>
            </table>
        </div>
        <table class="info-row">
            <tr>
                <td><span class="info-label">DATA:</span> {data_escala.strftime('%d/%m/%Y')}</td>
                <td><span class="info-label">DIA DA SEMANA:</span> {dia_semana_str.upper()}</td>
                <td><span class="info-label">TURNO:</span> {target_turno}</td>
                <td><span class="info-label">RESPONSÁVEL:</span> {user_cpf}</td>
            </tr>
        </table>
        {html_table}
    </div>
</body>
</html>
"""
        
        st.download_button(
            label="📄 Imprimir / Download HTML",
            data=html_content,
            file_name=f"escala_{target_turno}_{data_escala}_{terminal_indicador}.html",
            mime="text/html"
        )

session.close()
