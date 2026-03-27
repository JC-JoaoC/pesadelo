import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Date, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash

# Define the local database file path
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "escala.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(14), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    turno = Column(String(20), nullable=False) # Admin, Alfa, Bravo, Charlie, Delta

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    matricula = Column(Integer, primary_key=True)
    nome_curto = Column(String(100), nullable=False)
    funcao = Column(String(100), nullable=False)
    turno = Column(String(20), nullable=False)

class Roster(Base):
    __tablename__ = 'rosters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_escala = Column(Date, nullable=False)
    turno = Column(String(20), nullable=False)
    status = Column(String(50), default="Incomplete")
    criado_por_id = Column(Integer, ForeignKey('users.id'))
    data = Column(JSON, nullable=False)

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if admin user exists, if not create one
    admin = session.query(User).filter_by(cpf='admin').first()
    if not admin:
        admin_password = generate_password_hash('admin')
        admin_user = User(cpf='admin', password_hash=admin_password, turno='Admin')
        session.add(admin_user)
        session.commit()
        print("Admin user created (CPF: admin, PW: admin)")
    else:
        print("Admin user already exists.")
    session.close()

if __name__ == "__main__":
    init_db()
