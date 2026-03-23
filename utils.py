import os
import streamlit as st
from sqlalchemy.orm import sessionmaker
from setup_db import engine, User

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()
