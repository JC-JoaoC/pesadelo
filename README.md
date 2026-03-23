# Sistema de Gestão de Escalas

A comprehensive web-based Duty Roster Management System built with Python, Streamlit, Pandas, and SQLAlchemy.

## 🚀 Setup Instructions

### 1. Requisites
Ensure you have **Python 3.8+** installed on your system.
For Windows, it is recommended to use an Anaconda environment or standard python `venv`.

### 2. Create the Virtual Environment
Open your terminal inside the project folder (`pythonEscala`) and run:
```bash
python -m venv venv
```
Activate the environment:
- Windows (Command Prompt): `venv\Scripts\activate.bat`
- Windows (PowerShell): `venv\Scripts\Activate.ps1`
- Git Bash/WSL/Linux: `source venv/Scripts/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database and run ETL 
The system requires `base.csv` to be present in the project directory.

Run the DB setup script to create databases and the admin user:
```bash
python setup_db.py
```

Run the ETL script to process employees from `base.csv`:
```bash
python process_base.py
```

### 5. Run the Application
Finally, start the Streamlit web server:
```bash
streamlit run app.py
```

## 🔐 Initial Login
- **CPF:** `admin`
- **Senha:** `admin123`

You can create more specific Turno logins (Alfa, Bravo, Charlie, Delta) using the "Gerenciar Logins" tab after logging in.

## 🗂 Project Structure
- `app.py`: Main Streamlit entry point.
- `auth.py`: Authentication configuration.
- `setup_db.py`: Database models and initialization.
- `process_base.py`: Pandas base logic for filtering and mapping times to shifts.
- `utils.py`: Database session generator.
- `pages/`: Individual dashboard modules automatically picked up by Streamlit's new `st.navigation`.
