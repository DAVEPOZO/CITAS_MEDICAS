import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from modelo.bd_citas_centro_medico import create_db
from modeloDeVista.login import login
from modeloDeVista.registrar import registar



# Crear base de datos
create_db()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Login - Centro Médico")
root.geometry("500x400+500+100")
root.configure(bg="#f4f4f4")

# Marco para organizar los elementos
frame_main = tk.Frame(root, bg="#f4f4f4", padx=20, pady=20)
frame_main.pack(expand=True)

tk.Label(frame_main, text="Inicio de Sesión", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333").pack(pady=10)

tk.Label(frame_main, text="Usuario:", font=("Arial", 12), bg="#f4f4f4").pack(anchor="w")
entry_username = tk.Entry(frame_main, font=("Arial", 12), width=30)
entry_username.pack(pady=5)

tk.Label(frame_main, text="Contraseña:", font=("Arial", 12), bg="#f4f4f4").pack(anchor="w")
entry_password = tk.Entry(frame_main, show="*", font=("Arial", 12), width=30)
entry_password.pack(pady=5)

# Botón de Login
tk.Button(frame_main, text="Login", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", width=15, height=1, command=lambda :  login(entry_username, entry_password, root)).pack(pady=10)

# Botón de Registro
tk.Button(frame_main, text="Registrar", font=("Arial", 12, "bold"), bg="#FF9800", fg="white", width=15, height=1, command=lambda: registar(root)).pack(pady=5)

root.mainloop()