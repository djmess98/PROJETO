import os
import sqlite3

def create_tables():
    # Obtém o diretório atual
    current_directory = os.getcwd()

    # Define o caminho completo para o arquivo expenses.db
    expenses_db_path = os.path.join(current_directory, "expenses.db")

    # Define o caminho completo para o arquivo budgets.db
    budgets_db_path = os.path.join(current_directory, "budgets.db")

    # Conecta ao banco de dados expenses.db
    conn_expenses = sqlite3.connect(expenses_db_path)
    cursor_expenses = conn_expenses.cursor()

    # Conecta ao banco de dados budgets.db
    conn_budgets = sqlite3.connect(budgets_db_path)
    cursor_budgets = conn_budgets.cursor()

    # Cria a tabela de users
    cursor_expenses.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            nif TEXT
        )
    """)
    conn_expenses.commit()

    # Cria a tabela expenses se ela não existir
    cursor_expenses.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            username TEXT,
            category TEXT,
            description TEXT,
            value TEXT,
            date TEXT
        )
    """)
    conn_expenses.commit()

    # Criação da tabela "budgets"
    cursor_budgets.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            username TEXT,
            budget INTEGER,
            PRIMARY KEY (username)
        )
    """)
    conn_budgets.commit()

    # Fecha as conexões com os bancos de dados
    conn_expenses.close()
    conn_budgets.close()
