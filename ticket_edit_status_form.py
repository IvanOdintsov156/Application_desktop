import tkinter as tk
from datetime import datetime
import customtkinter as ctk
class TicketEditStatusForm:
    def __init__(self, master,db, ticket_id, parent_window):
        self.master = master
        self.master.iconbitmap("static/icon.ico")
        self.db = db
        self.ticket_id = ticket_id
        self.parent_window = parent_window

        self.ticket_data = self.db.get_ticket_by_id(ticket_id)

        self.label_status = ctk.CTkLabel(master, text="Статус:")
        self.label_status.grid(row=0,column=0,sticky="e")

        self.status_var = ctk.StringVar(master)
        self.status_var.set("В ожидании")
        self.status_options = ["В ожидании", "В работе", "Выполнено"]
        self.status_dropdown = tk.OptionMenu(master, self.status_var, *self.status_options)
        self.status_dropdown.grid(row=0,column=1)

        self.btn_submit = ctk.CTkButton(master, text="Сохранить", command=self.save)
        self.btn_submit.grid(row=1,column=2)

    def save(self):
        ticket_data = {
        "status": self.status_var.get(),
        "equipment": self.ticket_data[0],
        "fault_type": self.ticket_data[2],
        "problem_description": self.ticket_data[3],
        "client": self.ticket_data[4]
        }
        if ticket_data['status'] == "Выполнено":
            ticket_data['completion_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.db.update_ticket(self.ticket_id, ticket_data)
        self.parent_window.update_tickets_display()
        self.master.destroy()
