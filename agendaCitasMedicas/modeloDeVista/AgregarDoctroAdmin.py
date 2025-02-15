import sqlite3
import tkinter as tk
from tkinter import messagebox



def agregarDoctorAdmin():
    add_doctor_window = tk.Toplevel()
    add_doctor_window.geometry("400x300+500+100")
    add_doctor_window.title("Agregar Doctor")
    add_doctor_window.config(bg="#F0F0F0")  # Fondo gris claro

    frame = tk.Frame(add_doctor_window, bg="#F0F0F0", padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Nombre del Doctor:", font=("Arial", 12), bg="#F0F0F0").pack(anchor="w")
    entry_name = tk.Entry(frame, font=("Arial", 12), width=30)
    entry_name.pack(pady=5)
    tk.Label(frame, text="Especialidad:", font=("Arial", 12), bg="#F0F0F0").pack(anchor="w")
    entry_specialty = tk.Entry(frame, font=("Arial", 12), width=30)
    entry_specialty.pack(pady=5)

    def save_doctor():
        name = entry_name.get()
        specialty = entry_specialty.get()

        if not name or not specialty:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Guardar doctor en la base de datos
        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicos (nombre, especialidad) VALUES (?, ?)", (name, specialty))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Doctor agregado exitosamente")
        add_doctor_window.destroy()  # Cerrar la ventana después de guardar

    tk.Button(frame, text="Guardar Doctor", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15, height=1, command=save_doctor).pack(pady=10)

    
