import sqlite3
import tkinter as tk
from tkinter import messagebox
from vista.dashboardPaciente import abrir_Paciente_dashboard
from vista.dashboardAdmin import abrir_admin_dashboard


# Función de login
def login(entry_username, entry_password, root):
    username = entry_username.get()
    password = entry_password.get()
    
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Bienvenido", f"Login exitoso como {user[0]}")
        
        # Cerrar la ventana de login
        #root.destroy()
        # Dependiendo del rol, abrir el dashboard correspondiente
        if user[0] == "Paciente":
            root.withdraw() 

            abrir_Paciente_dashboard(username,root)  # Puedes pasar el nombre de usuario o cualquier dato necesario
            entry_username.delete(0, tk.END)  # Elimina todo el texto en el campo de usuario
            entry_password.delete(0, tk.END) 
        else:
            root.withdraw()

            abrir_admin_dashboard(username,root)
            entry_username.delete(0, tk.END)  # Elimina todo el texto en el campo de usuario
            entry_password.delete(0, tk.END) 
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")
