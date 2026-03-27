import streamlit as st
import pandas as pd
import json
import datetime
from utils import get_session
from setup_db import Funcionario, Roster

st.set_page_config(page_title="Criar Escala", layout="wide")

st.title("Criar Nova Escala")

session = get_session()
user_turno = st.session_state.get("user_turno", "Admin")

# Filtro 
if user_turno == "Admin":
    target_turno = st.selectbox("Selecione o Turno da Escala", ["Alfa", "Bravo", "Charlie", "Delta"])
else:
    target_turno = user_turno
    st.info(f"Criando escala para o Turno: **{target_turno}**")

data_escala = st.date_input("Data da Escala", datetime.date.today())
postos_layout_t2 = {
    "NACIONAL 1 - FAST": [1, 1, 1, 1, 1, 1],
    "NACIONAL 1 - Nº 1": [1, 1, 1, 1, 0, 0],
    "NACIONAL 1 - Nº 2": [1, 1, 1, 1, 1, 1],
    "NACIONAL 1 - BCBP:": [1, 0, 0, 0, 0, 0],
    "NACIONAL 1 - PORTÃO C1": [1, 1, 1, 1, 0, 0],
    "": [0],
    "NACIONAL 2 - Nº 3": [1, 1, 1, 1, 1, 1],
    "NACIONAL 2 - Nº 4": [1, 1, 1, 1, 0, 0],
    "NACIONAL 2 - Nº 5": [1, 1, 1, 1, 1, 1],
    "NACIONAL 2 - Nº 6": [1, 1, 1, 1, 0, 0],
    "NACIONAL 2 - Nº 7": [1, 1, 1, 1, 1, 1],
    "NACIONAL 2 - Nº 8": [1, 1, 1, 1, 0, 0],
    "NACIONAL 2 - Nº 9": [1, 1, 1, 1, 1, 1],
    "NACIONAL 2 - Nº 10": [1, 1, 1, 1, 0, 0],
    "NACIONAL 2 - Nº 11": [1, 1, 1, 1, 1, 1],
    "NACIONAL 2 - Nº 12": [1, 1, 1, 1, 0, 0],
    "NACIONAL 2 - Nº 13": [1, 1, 1, 1, 1, 1],
    "NACIONAL 2 - Nº 14": [1, 1, 1, 1, 0, 0],
    "NACIONAL 2 - Nº 15": [1, 1, 1, 1, 1, 1],
    "NACIONAL 2 - Nº 16": [1, 1, 1, 1, 0, 0],
    "NACIONAL 2 - BCBP": [1, 1, 1, 1, 1, 1],
    "": [0],
    "INTERNACIONAL 2 - Nº 1": [1, 1, 1, 1, 1, 1],
    "INTERNACIONAL 2 - Nº 2": [1, 1, 1, 1, 0, 0],
    "INTERNACIONAL 2 - Nº 3": [1, 1, 1, 1, 0, 0],
    "INTERNACIONAL 2 - Nº 4": [1, 1, 1, 1, 0, 0],
    "INTERNACIONAL 2 - Nº 5": [1, 1, 1, 1, 1, 1],
    "INTERNACIONAL 2 - Nº 6": [1, 1, 1, 1, 0, 0],
    "INTERNACIONAL 2 - BCBP/12:": [1, 1, 1, 1, 0, 0],
    "": [0],
    "PORTÃO CHARLIE - ENTRADA": [1, 1, 0, 1, 1, 1],
    "PORTÃO CHARLIE - SAÍDA": [1, 1, 0, 0, 0, 0],
    "": [0],
    "TECA - BLOQUEIO": [1, 1, 1, 1, 0, 1],
    "TECA - ARMAZÉM": [1, 1, 1, 1, 1, 0],
    "TECA - CENTRAL": [1, 1, 1, 1, 1, 0],
    "": [0],
    "CONTRATOS - CNX 35": [1, 1, 1, 1, 0, 0],
    "CONTRATOS - CNX 36": [1, 1, 1, 1, 1, 1],
    "": [0],
    "CONTRATOS - FAST PASS:": [1, 1, 1, 1, 1, 1],
    "CONTRATOS - MERCADORIAS": [1, 1, 1, 1, 0, 0]
}

postos_layout_t3 = {
    "INTERNACIONAL 3 - Nº 01": [1, 1, 1, 1, 1, 1],
    "INTERNACIONAL 3 - Nº 02": [1, 1, 1, 1, 0, 0],
    "INTERNACIONAL 3 - Nº 03": [0, 0, 0, 0, 0, 0],
    "INTERNACIONAL 3 - Nº 04": [1, 1, 1, 1, 1, 1],
    "INTERNACIONAL 3 - Nº 05": [1, 1, 1, 1, 0, 0],
    "INTERNACIONAL 3 - Nº 07": [1, 1, 1, 1, 1, 1],
    "INTERNACIONAL 3 - Nº 08": [1, 1, 1, 1, 0, 0],
    "INTERNACIONAL 3 - Nº 09": [1, 1, 1, 1, 1, 1],
    "INTERNACIONAL 3 - Nº 10": [1, 1, 1, 1, 0, 0],
    "": [0],
    "FAST PASS - FAST PASS": [1, 1, 1, 1, 1, 1],
    "": [0],
    "CONEXÕES - Nº 01": [1, 1, 1, 1, 0, 1],
    "CONEXÕES - Nº 02": [1, 1, 1, 0, 0, 0],
    "CONEXÕES - Nº 03": [1, 1, 1, 1, 0, 1],
    "CONEXÕES - Nº 04": [1, 1, 1, 0, 0, 0],
    "CONEXÕES - Nº 05": [0, 0, 0, 0, 0, 0],
    "": [0],
    "ACESSOS T3 - ACESSO DE FUNCIONÁRIOS": [1, 1, 1, 1, 0, 1],
    "ACESSOS T3 - PISO 0": [1, 1, 0, 0, 0, 0],
    "": [0],
    "PISO -1 - PORTÃO C": [1, 1, 1, 1, 0, 1],
    "PISO -1 - RESÍDUOS": [1, 0, 0, 0, 0, 1],
    "": [0],
    "BCBP - INTER 3": [1, 1, 1, 0, 0, 0],
    "BCBP - FAST PASS": [0, 0, 0, 0, 0, 0],
    "RFB - RF": [0, 0, 0, 0, 0, 0],
    "RFB - CURRIER": [0, 0, 0, 0, 0, 0]
}

layouts = {
    "Terminal 2": postos_layout_t2,
    "Terminal 3": postos_layout_t3
}

selected_terminal = st.radio("Selecione o Terminal", list(layouts.keys()), horizontal=True)
postos_layout = layouts.get(selected_terminal, postos_layout_t2)

# Fazer o busca e preencher tudo aleatorio 
empos = session.query(Funcionario).filter_by(turno=target_turno).all()
options = [""] + [f"{e.matricula} - {e.nome_curto}" for e in empos]
options_lideres = [""] + [f"{e.matricula} - {e.nome_curto}" for e in empos if e.funcao == "AGENTE LIDER DE PROTECAO"]

import random

if "roster_grid" not in st.session_state or st.session_state.get("last_turno") != target_turno or st.session_state.get("last_terminal") != selected_terminal:
    postos = list(postos_layout.keys())
    default_data = {"Posto": postos}
    
    for i in range(1, 7):
        default_data[f"FUNÇÃO {i}"] = ["" if (postos_layout[posto][i-1] if i-1 < len(postos_layout[posto]) else 0) else "-" for posto in postos]
        
    st.session_state["roster_grid"] = default_data
    st.session_state["last_turno"] = target_turno
    st.session_state["last_terminal"] = selected_terminal

st.write("### Grid de Escalonamento")

st.caption("Clique nas células para selecionar os funcionários manualmente.")

if st.button("🔄 Escala Aleatória", help="Preenche as posições aleatoriamente com a lista de funcionários"):
        available_empos = list(empos)
        random.shuffle(available_empos)
        lideres = [e for e in available_empos if e.funcao == "AGENTE LIDER DE PROTECAO"]
        outros = [e for e in available_empos if e.funcao != "AGENTE LIDER DE PROTECAO"]
        
        postos = list(postos_layout.keys())
        new_data = {"Posto": postos}
        for i in range(1, 7):
            func_list = []
            for posto in postos:
                layout_list = postos_layout[posto]
                is_active = layout_list[i-1] if i-1 < len(layout_list) else 0
                if is_active:
                    if i == 6 and lideres:
                        emp = lideres.pop()
                        func_list.append(f"{emp.matricula} - {emp.nome_curto}")
                    elif i != 6 and outros:
                        emp = outros.pop()
                        func_list.append(f"{emp.matricula} - {emp.nome_curto}")
                    elif i != 6 and lideres:
                        emp = lideres.pop()
                        func_list.append(f"{emp.matricula} - {emp.nome_curto}")
                    else:
                        func_list.append("")
                else:
                    func_list.append("-")
            new_data[f"FUNÇÃO {i}"] = func_list
        
        st.session_state["roster_grid"] = new_data
        st.rerun()

df = pd.DataFrame(st.session_state["roster_grid"])

column_config = {
    "Posto": st.column_config.TextColumn("Posto", disabled=True)
}
for i in range(1, 7):
    col_options = options_lideres if i == 6 else options
    column_config[f"FUNÇÃO {i}"] = st.column_config.SelectboxColumn(
        f"FUNÇÃO {i}",
        help="Selecione o funcionário",
        options=col_options
    )

edited_df = st.data_editor(
    df,
    column_config=column_config,
    hide_index=True,
    num_rows="dynamic",
    width="stretch"
)

if st.button("Salvar Escala", type="primary"):
    data_json = edited_df.to_dict(orient="records")
    
    # Analisar as celulas vazias
    total_cells = len(edited_df) * 6
    filled_cells = 0
    for row in data_json:
        for i in range(1, 7):
            val = row.get(f"FUNÇÃO {i}")
            if val and str(val).strip() != "":
                filled_cells += 1
                
    status = "Completa" if filled_cells >= total_cells * 0.5 else "Incompleta" # Arbitrary completeness logic

    terminal_indicador = "T2" if selected_terminal == "Terminal 2" else "T3"
    new_roster = Roster(
        data_escala=data_escala,
        turno=f"{target_turno} - {terminal_indicador}",
        criado_por_id=st.session_state.get("user_id"),
        data=data_json,
        status=status
    )
    session.add(new_roster)
    session.commit()
    st.success(f"Escala do turno {target_turno} - {selected_terminal} para {data_escala} salva com sucesso como {status}!`")

session.close()
