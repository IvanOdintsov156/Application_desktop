import tkinter as tk
import datetime
import customtkinter as ctk
class TicketEditForm:
    def __init__(self, master,db, ticket_id, parent_window):
        self.master = master
        self.db = db
        self.ticket_id = ticket_id
        self.parent_window = parent_window

        self.ticket_data = self.db.get_ticket_by_id(ticket_id)

        self.label_ticket_number = ctk.CTkLabel(master, text="Заявка №")
        self.label_ticket_number.grid(row=0,column=0,sticky="e")

        self.entry_ticket_number = ctk.CTkEntry(master)
        self.entry_ticket_number.insert(tk.END, self.ticket_data[1])
        self.entry_ticket_number.grid(row=0,column=1)

        self.label_equipment = ctk.CTkLabel(master, text="Оборудование:")
        self.label_equipment.grid(row=1,column=0,sticky="e")

        self.entry_equipment = ctk.CTkEntry(master)
        self.entry_equipment.insert(tk.END, self.ticket_data[2])
        self.entry_equipment.grid(row=1,column=1)

        self.fault_type = ctk.CTkLabel(master, text="Тип неисправности:")
        self.fault_type.grid(row=2,column=0,sticky="e")

        self.entry_fault_type = ctk.CTkEntry(master)
        self.entry_fault_type.insert(tk.END, self.ticket_data[3])
        self.entry_fault_type.grid(row=2,column=1)

        self.problem_description = ctk.CTkLabel(master, text="Описание проблемы:")
        self.problem_description.grid(row=3,column=0,sticky="e")

        self.entry_problem_description = ctk.CTkEntry(master)
        self.entry_problem_description.insert(tk.END, self.ticket_data[4])
        self.entry_problem_description.grid(row=3,column=1)

        self.label_client = ctk.CTkLabel(master, text="Клиент:")
        self.label_client.grid(row=4,column=0,sticky="e")

        self.entry_client = ctk.CTkEntry(master)
        self.entry_client.insert(tk.END, self.ticket_data[5])
        self.entry_client.grid(row=4,column=1)

        self.label_status = ctk.CTkLabel(master, text="Статус:")
        self.label_status.grid(row=5,column=0,sticky="e")

        self.status_var = tk.StringVar(master)
        self.status_var.set("В ожидании")
        self.status_options = ["В ожидании", "В работе", "Выполнено"]
        self.status_dropdown = tk.OptionMenu(master, self.status_var, *self.status_options)
        self.status_dropdown.grid(row=5,column=1)

        self.btn_submit = ctk.CTkButton(master, text="Сохранить", command=self.save)
        self.btn_submit.grid(row=6,column=2)

    def save(self):
        ticket_data = {
            "ticket_number": self.entry_ticket_number.get(),
            "equipment": self.entry_equipment.get(),
            "fault_type": self.entry_fault_type.get(),
            "problem_description": self.entry_problem_description.get(),
            "client": self.entry_client.get(),
            "status": self.status_var.get()
        }
        if ticket_data['status'] == "Выполнено":
            ticket_data['completion_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.db.update_ticket(self.ticket_id, ticket_data)
        self.parent_window.update_ticket_info()
        self.master.destroy()