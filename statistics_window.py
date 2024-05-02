import tkinter as tk
from tkinter import ttk
from datetime import datetime
from collections import Counter

def create_statistics_window(db):
    statistics_window = tk.Toplevel()
    statistics_window.title("Статистика")

    # Стилизация
    style = ttk.Style()
    style.theme_use('clam')  # Выбираем одну из доступных тем
    style.configure("TButton", foreground="white", background="#4CAF50", font=("Arial", 12))
    style.configure("TLabel", background="#eee", font=("Arial", 12))

    style.map("TButton",
        foreground=[('pressed', 'white'), ('active', 'white')],
        background=[('pressed', '#388E3C'), ('active', '#66BB6A')],
        font=[('pressed', ("Arial", 12, 'bold')), ('active', ("Arial", 12, 'bold'))]
    )

    label_datetime = ttk.Label(statistics_window, style="TLabel", text="")
    label_datetime.pack()

    def update_datetime():
        current_datetime = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        label_datetime.config(text=current_datetime)
        statistics_window.after(1000, update_datetime)
    update_datetime()

    # Создание виджета прокрутки для таблицы заявок
    tree_tickets_frame = ttk.Frame(statistics_window)
    tree_tickets_frame.pack(expand=True, fill="both")

    tree_tickets_scrollbar = ttk.Scrollbar(tree_tickets_frame, orient="vertical")
    tree_tickets_scrollbar.pack(side="right", fill="y")

    tree_tickets = ttk.Treeview(tree_tickets_frame, style="TLabel", yscrollcommand=tree_tickets_scrollbar.set)
    tree_tickets_scrollbar.config(command=tree_tickets.yview)

    tree_tickets["columns"] = ("№", "Оборудование", "Тип неисправности", "Описание", "Клиент", "Статус", "Дата и время создания", "Выполнение", "Время выполнения")

    for col in tree_tickets["columns"]:
        tree_tickets.heading(col, text=col)
        tree_tickets.column(col, anchor="center", width=150, stretch=tk.NO)  # Adjust the width as needed, prevent stretching
    tree_tickets.pack(side="left", expand=True, fill="both")

    # Создание виджета прокрутки для таблицы типов неисправностей
    tree_fault_types_frame = ttk.Frame(statistics_window)
    tree_fault_types_frame.pack(expand=True, fill="both")

    tree_fault_types_scrollbar = ttk.Scrollbar(tree_fault_types_frame, orient="vertical")
    tree_fault_types_scrollbar.pack(side="right", fill="y")

    tree_fault_types = ttk.Treeview(tree_fault_types_frame, style="TLabel", yscrollcommand=tree_fault_types_scrollbar.set)
    tree_fault_types_scrollbar.config(command=tree_fault_types.yview)

    tree_fault_types["columns"] = ("Тип неисправности", "Количество выполненных заявок")

    for col in tree_fault_types["columns"]:
        tree_fault_types.heading(col, text=col)
        tree_fault_types.column(col, anchor="center", width=200, stretch=tk.NO)  # Adjust the width as needed, prevent stretching
    tree_fault_types.pack(side="left", expand=True, fill="both")

    tickets = db.get_all_tickets()  # Assuming get_all_tickets() returns a list of tickets with the specified structure

    if tickets:
        for num, ticket in enumerate(tickets, 1):
            if ticket[6] == "Выполнено" and ticket[8]:
                creation_time = datetime.strptime(ticket[7], '%Y-%m-%d %H:%M:%S')
                completion_time = datetime.strptime(ticket[8], '%Y-%m-%d %H:%M:%S')
                execution_time = completion_time - creation_time
                execution_time_str = str(execution_time)
            else:
                execution_time_str = "Не указано"

            tree_tickets.insert("", "end", values=(num, ticket[2], ticket[3], ticket[4], ticket[5], ticket[6], ticket[7], '' if ticket[8] is None else ticket[8], execution_time_str))

        fault_type_counter = Counter(ticket[3] for ticket in tickets if ticket[6] == "Выполнено")

        for fault_type, count in fault_type_counter.items():
            tree_fault_types.insert("", "end", values=(fault_type, count))

    else:
        tree_tickets.insert("", "end", text="Нет данных", values=[""]*9)
        tree_fault_types.insert("", "end", text="Нет данных", values=[""]*2)

    statistics_window.mainloop()
