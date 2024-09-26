import tkinter as tk
import datetime
import customtkinter as ctk
class TicketForm:
    def __init__(self, master,db, application_window, creation_time = None):
        self.master = master
        self.master.iconbitmap("static/icon.ico")
        self.db = db
        self.application_window = application_window
        self.creation_time = creation_time

        master.config(width=400, height=300) 

        self.label_ticket_number = ctk.CTkLabel(master, text="Заявка №")
        self.label_ticket_number.grid(row=0, column=0, sticky="e", padx=10, pady=5)

        self.entry_ticket_number = ctk.CTkEntry(master)
        self.entry_ticket_number.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        self.label_equipment = ctk.CTkLabel(master, text="Оборудование:")
        self.label_equipment.grid(row=1, column=0, sticky="e", padx=10, pady=5)

        self.entry_equipment = ctk.CTkEntry(master)
        self.entry_equipment.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        self.fault_type = ctk.CTkLabel(master, text="Тип неисправности:")
        self.fault_type.grid(row=2, column=0, sticky="e", padx=10, pady=5)

        self.entry_fault_type = ctk.CTkEntry(master)
        self.entry_fault_type.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        self.problem_description = ctk.CTkLabel(master, text="Описание проблемы:")
        self.problem_description.grid(row=3, column=0, sticky="e", padx=10, pady=5)

        self.entry_problem_description = ctk.CTkEntry(master)
        self.entry_problem_description.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        self.label_client = ctk.CTkLabel(master, text="Клиент:")
        self.label_client.grid(row=4, column=0, sticky="e", padx=10, pady=5)

        self.entry_client = ctk.CTkEntry(master)
        self.entry_client.grid(row=4, column=1, sticky="e", padx=10, pady=5)

        self.label_status = ctk.CTkLabel(master, text="Статус:")
        self.label_status.grid(row=5, column=0, sticky="e", padx=10, pady=5)

        self.status_var = tk.StringVar(master)
        self.status_var.set("В ожидании")
        self.status_options = ["В ожидании", "В работе", "Выполнено"]
        self.status_dropdown = tk.OptionMenu(master, self.status_var, *self.status_options)
        self.status_dropdown.grid(row=5, column=1, sticky="e", padx=10, pady=5)

        self.btn_submit = ctk.CTkButton(master, text="Отправить", command=self.submit)
        self.btn_submit.grid(row=6, column=1, padx=10, pady=5)
    def submit(self):
        created_at = self.creation_time.strftime('%Y-%m-%d %H:%M:%S') if self.creation_time else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        ticket_data = {
            "ticket_number": self.entry_ticket_number.get(),
            "equipment": self.entry_equipment.get(),
            "fault_type": self.entry_fault_type.get(),
            "problem_description": self.entry_problem_description.get(),
            "client": self.entry_client.get(),
            "status": self.status_var.get(),
            "created_at": created_at
        }
        
        self.db.insert_ticket(ticket_data)
        self.application_window.update_ticket_info()
        self.master.destroy()
