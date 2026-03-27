import os
import sqlite3
import pandas as pd
import re

def to_mins(hhmm):
    h, m = map(int, hhmm.split(':'))
    return h * 60 + m

def get_min_set(start_str, end_str):
    start = to_mins(start_str)
    end = to_mins(end_str)
    if end <= start:
        end += 1440
    return {(m % 1440) for m in range(start, end)}

def map_turno(horario_str):
    horario_str = str(horario_str).upper()
    if '23:00' in horario_str and '05:00' in horario_str: return 'Alfa'
    if '05:00' in horario_str and '11:00' in horario_str: return 'Bravo'
    if '11:00' in horario_str and '17:00' in horario_str: return 'Charlie'
    if '17:00' in horario_str and '23:00' in horario_str: return 'Delta'
    
    times = re.findall(r'(\d{2}:\d{2})', horario_str)
    if len(times) >= 2:
        try:
            worker_mins = get_min_set(times[0], times[1])
            shifts = {
                'Alfa': get_min_set('23:00', '05:00'),
                'Bravo': get_min_set('05:00', '11:00'),
                'Charlie': get_min_set('11:00', '17:00'),
                'Delta': get_min_set('17:00', '23:00')
            }
            best_shift = max(shifts.items(), key=lambda x: len(worker_mins.intersection(x[1])))
            if len(worker_mins.intersection(best_shift[1])) > 0:
                return best_shift[0]
        except Exception as e:
            pass
    return 'Charlie' # "FLEXIVEL"

def process_name(full_name):
    parts = str(full_name).strip().split()
    if len(parts) >= 2:
        return f"{parts[0]} {parts[1]}".upper()
    elif len(parts) == 1:
        return parts[0].upper()
    return ""

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'base.csv')
    db_path = os.path.join(base_dir, 'escala.db')

    print(f"Reading {csv_path}...")
    try:
        df = pd.read_csv(csv_path, sep=',', header=0)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Remova os nomes das colunas para evitar problemas com espaços em branco
    df.columns = df.columns.str.strip()

    required_cols = ['CHAPA', 'NOME COMPLETO', 'FUNÇÃO', 'HORÁRIO DE JORNADA', 'STATUS']
    for col in required_cols:
        if col not in df.columns:
            print(f"Missing required col: {col}. Available: {df.columns}")
            return

    # filtro dos ativos
    df = df[df['STATUS'] == 'A']

    # filtro da FUNÇÃO
    valid_funcs = ['ATENDENTE', 'AGENTE DE PROTECAO', 'AGENTE LIDER DE PROTECAO']
    df = df[df['FUNÇÃO'].str.upper().isin(valid_funcs)]
    
    # Drop duplicates to prevent UNIQUE constraint failures on matricula (CHAPA)
    df = df.drop_duplicates(subset=['CHAPA'])

    # Transform columns
    processed_records = []
    
    for idx, row in df.iterrows():
        try:
            matricula = int(row['CHAPA'])
        except:
            continue
            
        nome_completo = row['NOME COMPLETO']
        nome_curto = process_name(nome_completo)
        
        funcao = str(row['FUNÇÃO']).upper()
        horario = row['HORÁRIO DE JORNADA']
        turno = map_turno(horario)
        
        processed_records.append((matricula, nome_curto, funcao, turno))

    if not processed_records:
        print("No records to insert after processing.")
        return

    # Connect to DB and insert
    print("Connecting to DB...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Clear previous funcionarios data if we are re-running
    cursor.execute("DELETE FROM funcionarios")
    
    insert_query = "INSERT INTO funcionarios (matricula, nome_curto, funcao, turno) VALUES (?, ?, ?, ?)"
    cursor.executemany(insert_query, processed_records)
    
    conn.commit()
    conn.close()
    
    print(f"Successfully inserted {len(processed_records)} employees into the database.")

if __name__ == "__main__":
    main()
