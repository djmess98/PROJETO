import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class ExpenseManagerWindow(tk.Toplevel):
    def __init__(self, master, username):
        super().__init__(master)
        self.title("Gestão de Despesas")
        self.geometry("500x400")

        self.username = username

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self)

        expenses_tab = tk.Frame(self.tab_control)
        self.tab_control.add(expenses_tab, text="Despesas")

        budget_tab = tk.Frame(self.tab_control)
        self.tab_control.add(budget_tab, text="Orçamento")

        self.tab_control.pack(expand=True, fill=tk.BOTH)

        self.create_expenses_tab(expenses_tab)
        self.create_budget_tab(budget_tab)

    def create_expenses_tab(self, tab):
        expenses_frame = tk.Frame(tab)
        expenses_frame.pack(pady=10)

        self.category_label = tk.Label(expenses_frame, text="Categoria:")
        self.category_label.grid(row=0, column=0, sticky="e")

        self.category_entry = tk.Entry(expenses_frame)
        self.category_entry.grid(row=0, column=1, padx=10)

        self.description_label = tk.Label(expenses_frame, text="Descrição:")
        self.description_label.grid(row=1, column=0, sticky="e")

        self.description_entry = tk.Entry(expenses_frame)
        self.description_entry.grid(row=1, column=1, padx=10)

        self.value_label = tk.Label(expenses_frame, text="Valor:")
        self.value_label.grid(row=2, column=0, sticky="e")

        self.value_entry = tk.Entry(expenses_frame)
        self.value_entry.grid(row=2, column=1, padx=10)

        self.date_label = tk.Label(expenses_frame, text="Data:")
        self.date_label.grid(row=3, column=0, sticky="e")

        self.date_entry = tk.Entry(expenses_frame)
        self.date_entry.grid(row=3, column=1, padx=10)

        add_expense_button = tk.Button(tab, text="Adicionar Despesa", command=self.add_expense)
        add_expense_button.pack(pady=10)

        filter_button = tk.Button(expenses_frame, text="Filtrar despesas", command=self.open_filter_window)
        filter_button.grid(row=4, column=0, pady=10)

        sort_button = tk.Button(expenses_frame, text="Ordenar despesas por valor", command=self.sort_expenses)
        sort_button.grid(row=4, column=1, pady=10)

        self.expenses_treeview = ttk.Treeview(tab, columns=("User","Category", "Description", "Value", "Date"), show="headings")
        self.expenses_treeview.column("User", width=100)
        self.expenses_treeview.column("Category", width=100)
        self.expenses_treeview.column("Description", width=150)
        self.expenses_treeview.column("Value", width=80, anchor=tk.E)
        self.expenses_treeview.column("Date", width=100)
        self.expenses_treeview.heading("User", text="Utilizador")
        self.expenses_treeview.heading("Category", text="Categoria")
        self.expenses_treeview.heading("Description", text="Descrição")
        self.expenses_treeview.heading("Value", text="Valor")
        self.expenses_treeview.heading("Date", text="Data")
        self.expenses_treeview.pack()

        self.load_expenses()

    def load_expenses(self):
        self.expenses_treeview.delete(*self.expenses_treeview.get_children())

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM expenses WHERE username=?", (self.username,))
        expenses = cursor.fetchall()

        for expense in expenses:
            self.expenses_treeview.insert("", "end", values=expense)

        conn.close()

    def add_expense(self):
        category = self.category_entry.get()
        description = self.description_entry.get()
        value = self.value_entry.get()
        date = self.date_entry.get()

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (username, category, description, value, date) VALUES (?, ?, ?, ?, ?)",
                    (self.username, category, description, value, date))
        conn.commit()
        conn.close()

        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

        self.load_expenses()

    def filter_expenses(self):
        category = self.category_entry.get()
        description = self.description_entry.get()
        value = self.value_entry.get()
        date = self.date_entry.get()

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        query = "SELECT * FROM expenses WHERE username=?"
        params = (self.username,)

        if category:
            query += " AND category=?"
            params += (category,)

        if description:
            query += " AND description=?"
            params += (description,)

        if value:
            query += " AND value=?"
            params += (value,)

        if date:
            query += " AND date=?"
            params += (date,)

        cursor.execute(query, params)
        expenses = cursor.fetchall()

        self.expenses_treeview.delete(*self.expenses_treeview.get_children())

        for expense in expenses:
            self.expenses_treeview.insert("", "end", values=expense)

        conn.close()

    def sort_expenses(self):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM expenses WHERE username=? ORDER BY value", (self.username,))
        expenses = cursor.fetchall()

        self.expenses_treeview.delete(*self.expenses_treeview.get_children())

        for expense in expenses:
            self.expenses_treeview.insert("", "end", values=expense)

        conn.close()

    def create_budget_tab(self, tab):
        budget_frame = tk.Frame(tab)
        budget_frame.pack(pady=10)

        self.budget_label = tk.Label(budget_frame, text="Orçamento:")
        self.budget_label.grid(row=0, column=0, sticky="e")

        self.budget_entry = tk.Entry(budget_frame)
        self.budget_entry.grid(row=0, column=1, padx=10)

        set_budget_button = tk.Button(tab, text="Definir Orçamento", command=self.set_budget)
        set_budget_button.pack(pady=10)

    def set_budget(self):
        budget = self.budget_entry.get()
        # Lógica para definir o orçamento
        messagebox.showinfo("Definir Orçamento", f"Orçamento definido: {budget}")

    def open_filter_window(self):
        filter_window = FilterWindow(self)
        filter_window.filter_by_category()  
    

class FilterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Filtrar Despesas")
        self.geometry("300x200")
        
        self.create_widgets()
        
    def create_widgets(self):
        filter_by_category_button = tk.Button(self, text="Filtrar por Categoria", command=self.filter_by_category)
        filter_by_category_button.pack(pady=10)
        
        filter_by_interval_button = tk.Button(self, text="Filtrar por Intervalo de Tempo", command=self.filter_by_interval)
        filter_by_interval_button.pack(pady=10)

    def filter_by_category(self):
        category = self.category_entry.get()

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        if category:
            cursor.execute("SELECT * FROM expenses WHERE username=? AND category=?", (self.username, category))
            expenses = cursor.fetchall()
        else:
            messagebox.showwarning("Filtrar por Categoria", "Por favor, insira uma categoria.")

        conn.close()

        self.expenses_treeview.delete(*self.expenses_treeview.get_children())

        for expense in expenses:
            self.expenses_treeview.insert("", "end", values=expense)

    def filter_by_interval(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        if start_date and end_date:
            cursor.execute("SELECT * FROM expenses WHERE username=? AND date BETWEEN ? AND ?", (self.username, start_date, end_date))
            expenses = cursor.fetchall()
        else:
            messagebox.showwarning("Filtrar por Intervalo de Tempo", "Por favor, insira um intervalo de tempo.")

        conn.close()

        self.expenses_treeview.delete(*self.expenses_treeview.get_children())

        for expense in expenses:
            self.expenses_treeview.insert("", "end", values=expense)
    


