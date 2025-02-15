import sqlite3
import tkinter as tk
from tkinter import messagebox


# Función para abrir la ventana de registro
def registar(root):
    register_window = tk.Toplevel(root)
    register_window.geometry("500x400+500+100")
    register_window.title("Registro de Usuario")
    register_window.configure(bg="#f4f4f4")  # Color de fondo

    frame = tk.Frame(register_window, bg="#f4f4f4", padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="#f4f4f4").pack(anchor="w")
    reg_entry_username = tk.Entry(frame, font=("Arial", 12), width=30)
    reg_entry_username.pack(pady=5)

    tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="#f4f4f4").pack(anchor="w")
    reg_entry_password = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    reg_entry_password.pack(pady=5)

    tk.Label(frame, text="Rol:", font=("Arial", 12), bg="#f4f4f4").pack(anchor="w")
    reg_role_var = tk.StringVar()
    tk.Radiobutton(frame, text="Paciente", variable=reg_role_var, value="Paciente", font=("Arial", 12), bg="#f4f4f4").pack(anchor="w")
    tk.Radiobutton(frame, text="Admin", variable=reg_role_var, value="Admin", font=("Arial", 12), bg="#f4f4f4").pack(anchor="w")

    def register():
        username = reg_entry_username.get()
        password = reg_entry_password.get()
        role = reg_role_var.get()
        
        if not username or not password or not role:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
            register_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe")
        conn.close()


    tk.Button(frame, text="Registrar", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15, height=1, command=register).pack(pady=10)

