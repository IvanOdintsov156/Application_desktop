import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ticket_edit_status_form import TicketEditStatusForm
import auth_window
class SpecialWindow:
    def __init__(self, master, database, current_user, authentication_window):
        self.master = master
        self.current_user = current_user
        self.authentication_window = authentication_window
        self.database = database
    
        self.welcome_label = tk.Label(master, text="Добро пожаловать, {}!".format(self.current_user), font=("Arial", 12))
        self.welcome_label.pack()
        self._create_widgets()
        self.update_datetime()

    def _create_widgets(self):
        self.master.title("Управление заявками")
        self.master.geometry("800x600")

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
        # Верхняя панель с кнопками
        self.top_frame = tk.Frame(self.master, bg="#333")
        self.top_frame.pack(fill=tk.X)

        self.back_to_main_button = ttk.Button(self.top_frame, text="Назад", command=self.back_to_main)
        self.back_to_main_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.logout_button = ttk.Button(self.top_frame, text="Выйти", command=self.logout)
        self.logout_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # Панель поиска
        # Search panel
        self.search_frame = tk.Frame(master=self.master, bg="#333")
        self.search_frame.pack(fill=tk.X)


        self.search_label = ttk.Label(self.search_frame, text="Поиск заявок", style="TLabel")
        self.search_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.search_entry = ttk.Entry(self.search_frame, style="TEntry", textvariable="Поиск")
        
        self.search_entry.pack(side=tk.LEFT, padx=(10, 0), pady=5, fill=tk.X, expand=True)  # Corrected padding to the left only


        # Search button
        self.search_button = ttk.Button(self.search_frame, text="Найти", command=self.search_tickets).pack(side=tk.RIGHT, padx=10, pady=5)

        # Виджет для отображения текущей даты и времени
        self.datetime_label = ttk.Label(self.master, text="", style="TLabel")
        self.datetime_label.pack(pady=10)

        # Фрейм для отображения заявок
        self.ticket_frame = tk.Frame(self.master, bg="#eee")
        self.ticket_frame.pack(fill=tk.BOTH, expand=True)

    # ... (другие методы остаются без изменений)


    def _create_label(self, text, style):
        label = ttk.Label(self.master, text=text, style=style)
        label.pack(padx=5, pady=5, fill=tk.X)
        return label

    def _create_button(self, text, command, style):
        button = ttk.Button(self.master, text=text, command=command, style=style)
        button.pack(padx=5, pady=5)
        return button

    def update_datetime(self):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.datetime_label.config(text=current_datetime)
        self.master.after(1000, self.update_datetime)

    def search_tickets(self):
        search_query = self.search_entry.get()
        
        tickets = self.database.search_tickets(search_query)
        self.update_tickets_display(tickets)

    def update_tickets_display(self):
        # Очищаем фрейм перед обновлением
        for widget in self.ticket_frame.winfo_children():
            widget.destroy()


        tickets = self.database.get_all_tickets()
        self._display_tickets(tickets)

    def _display_tickets(self, tickets):
        for ticket in tickets:
            ticket_info = f"Заявка №: {ticket[0]}\nОборудование: {ticket[1]}\nТип неисправности: {ticket[2]}\nОписание проблемы: {ticket[3]}\nКлиент: {ticket[4]}\nСтатус: {ticket[5]}\nДата и время создания: {ticket[6]}"
            if ticket[8]:
                ticket_info += f"\nДата и время выполнения: {ticket[8]}"
            
            label = tk.Label(self.ticket_frame, text=ticket_info, bg="#eee", font=("Arial", 12))
            label.pack(fill=tk.X, padx=10, pady=5)

            button = tk.Button(self.ticket_frame, text="Изменить статус", command=lambda ticket_id=ticket[0]: self.edit_ticket_status(ticket_id))
            button.pack(side=tk.LEFT, padx=10, pady=5)

    def edit_ticket_status(self, ticket_id):
        ticket_edit_status_window = tk.Toplevel(self.master)
        
        ticket_edit_status_window.configure(bg="#f0f0f0")
        ticket_edit_status_window.title("Изменение статуса заявки")
        ticket_edit_status_form = TicketEditStatusForm(ticket_edit_status_window, self.database, 
                                                       ticket_id, self)

    def back_to_main(self):
        self.master.destroy()
        self.authentication_window.deiconify()

    def logout(self):
        self.master.destroy()
        self.authentication_window.destroy()