# import sqlite3
import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk
# from tkcalendar import Calendar
# from datetime import datetime
from modeloDeVista.export_pdf import exportar_citas_a_pdf
# from bd_citas_centro_medico import get_user_id, get_medico_id
from modeloDeVista.agendarCitas import agendarCitasPaciente
from modeloDeVista.verCitas import verCitasPaciente
from modeloDeVista.editarCancelarCitas import cancelarCitasPaciente

def abrir_Paciente_dashboard(username, root):
    dashboard = tk.Tk() 
    dashboard.geometry("600x500+500+100")
    dashboard.title("Dashboard Paciente")
    dashboard.config(bg="#F0F0F0")  # Fondo gris claro

    # Título
    tk.Label(dashboard, text=f"Bienvenido, {username}", font=("Arial", 16, "bold"), bg="#F0F0F0", fg="#333333").pack(pady=20)

    # Botón Agendar Cita
    tk.Button(dashboard, text="Agendar Cita", command=lambda: agendarCitasPaciente(username),
              font=("Arial", 14), bg="#4CAF50", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)

    # Botón Ver Citas
    tk.Button(dashboard, text="Ver Citas", command=lambda: verCitasPaciente(username),
              font=("Arial", 14), bg="#2196F3", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)

    # Botón Cancelar Cita
    tk.Button(dashboard, text="Cancelar Cita", command=lambda: cancelarCitasPaciente(username),
              font=("Arial", 14), bg="#F44336", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    
    
    tk.Button(dashboard, text="Exportar Citas a PDF", command=lambda: exportar_citas_a_pdf(username),
              font=("Arial", 14), bg="#FF9800", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    def logout():
        dashboard.destroy()  # Cierra la ventana del Dashboard
        root.deiconify() 

    tk.Button(dashboard, text="Cerrar sesión", command=logout, font=("Arial", 14), bg="#FF5722", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    



