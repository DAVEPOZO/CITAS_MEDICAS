
import tkinter as tk
from modeloDeVista.agendarCitas import agendarCitasAdministrador
from modeloDeVista.export_pdf import exportar_citas_a_pdf
# from tkinter import ttk, messagebox
from modeloDeVista.verCitas import verCitasAdmin
from modeloDeVista.editarCancelarCitas import cancelarCitaAdmin
from modeloDeVista.AgregarDoctroAdmin import agregarDoctorAdmin

def abrir_admin_dashboard(username,root):
    """Abre el panel de administrador"""
    admin_window = tk.Tk() 
    admin_window.geometry("600x500+500+100")
    admin_window.title("Dashboard Administrador")
    admin_window.config(bg="#F0F0F0")  # Fondo gris claro

    # Título del panel
    tk.Label(admin_window, text=f"Panel de Administrador, {username}", font=("Arial", 18, "bold"), bg="#F0F0F0", fg="#333333").pack(pady=20)

    # Botones con estilo
    tk.Button(admin_window, text="Agregar un Doctor",command=agregarDoctorAdmin,font=("Arial", 12), bg="#0e813c", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    tk.Button(admin_window, text="Ver Citas", command=verCitasAdmin, font=("Arial", 12), bg="#2196F3", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    tk.Button(admin_window, text="Agendar Cita", command=agendarCitasAdministrador, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    tk.Button(admin_window, text="Editar o Cancelar Cita", command=cancelarCitaAdmin, font=("Arial", 12), bg="#F44336", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    tk.Button(admin_window, text="Exportar Citas a PDF", command=lambda: exportar_citas_a_pdf(username), font=("Arial", 12), bg="#FF9800", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)


    def logout():
        admin_window.destroy()  # Cierra la ventana del Dashboard
        root.deiconify() 

    tk.Button(admin_window, text="Cerrar sesión", command=logout, font=("Arial", 12), bg="#FF5722", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    



