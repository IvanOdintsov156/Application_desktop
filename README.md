App documentation

Project Description

This application is a graphical user interface designed for registering and authorizing users. It leverages the powerful `tkinter` and `customtkinter` libraries to create a user-friendly interface and facilitate smooth interactions.

Requirements

Python 3.x or later

The following libraries:
   – `tkinter`
   – `customtkinter`
   – \ 'sqlite3` (or any other database module of your choice)

Installation

Make sure you have Python 3.x installed on your system.

Install the required libraries using pip:

```bash
pip install customtkinter
```

Launching the app

To start the application, run the following command in your terminal:

```bash
python main.py
```

Project structure

Here's a sample project structure:

```
project_directory/
├── main.py
├── auth_window.py
├── registration.py
├── dashboard/
│   └── edit_profile.py
├── static/
│   └── icon.ico
└── themes/
└── sky.json
```

Description of functions

main.py

This is the main file responsible for launching the application.

auth_window.py

AuthWindow.login

This function handles user login. It verifies the entered username and password against the database, then redirects the user to the appropriate screen based on the username.

```python
def login(self):
    username = self.entry_username.get()
    password = self.entry_password.get()

    if self.db.check_credentials(username, password):
        self.master.withdraw()
        if username == "2":
            self.open_special_window(username)
        else:
            self.open_application_window(username)
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль", parent=self.master)
        self.entry_username.focus_set()  # Set focus back to username entry field
```

registration.py

RegistrationForm.upload_photo

This function allows users to upload their photos. It prompts the user to select a file and then displays the photo on the screen.

```python
def upload_photo(self):
    self.file_path = filedialog.askopenfilename()
    if self.file_path:
        self.photo_path = self.file_path
        self.display_photo(self.file_path)
        self.show_cross_image()
```

database.py

Database.insert_ticket

This function inserts ticket data into the database. It takes the ticket data as input and executes a SQL query to insert the necessary information into the database table.

```python
def insert_ticket(self, ticket_data):
    created_at = ticket_data.get('created_at', datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S'))
    self.cursor.execute("INSERT INTO tickets (ticket_number, equipment, fault_type, problem_description, client, status, created_at, completion_date) VALUES (?,?,?,?,?,?,?,?)",
                (ticket_data['ticket_number'], ticket_data['equipment'], ticket_data['fault_type'], ticket_data['problem_description'], ticket_data['client'], ticket_data['status'], created_at, ticket_data.get('completion_date', None)))
    self.conn.commit()
```
