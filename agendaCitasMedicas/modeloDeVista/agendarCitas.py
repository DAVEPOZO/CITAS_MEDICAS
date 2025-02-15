
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from modelo.bd_citas_centro_medico import get_user_id, get_medico_id


def agendarCitasPaciente(username):
    """Ventana para que el paciente agende una cita médica."""
    schedule_window = tk.Toplevel()
    schedule_window.geometry("600x600+500+100")
    schedule_window.title("Agendar Cita")
    schedule_window.config(bg="#F0F0F0")

    tk.Label(schedule_window, text="Agendar Cita Médica", font=("Arial", 16, "bold"), bg="#F0F0F0", fg="#333333").pack(pady=5)

    # Selección de especialidad
    tk.Label(schedule_window, text="Selecciona una especialidad:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=5)
    specialty_var = tk.StringVar()
    specialty_menu = ttk.Combobox(schedule_window, textvariable=specialty_var, font=("Arial", 12))
    specialty_menu.pack(pady=5)

    # Selección de médico
    tk.Label(schedule_window, text="Selecciona un médico:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=5)
    doctor_var = tk.StringVar()
    doctor_menu = ttk.Combobox(schedule_window, textvariable=doctor_var, font=("Arial", 12))
    doctor_menu.pack(pady=5)

    # Obtener especialidades únicas
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT especialidad FROM medicos")
    specialties = [row[0] for row in cursor.fetchall()]
    conn.close()

    specialty_menu["values"] = specialties  # Asignar especialidades al ComboBox

    def update_doctors(*args):
        """Actualizar la lista de médicos en función de la especialidad seleccionada."""
        selected_specialty = specialty_var.get()
        if not selected_specialty:
            return

        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM medicos WHERE especialidad=?", (selected_specialty,))
        doctors = [row[0] for row in cursor.fetchall()]
        conn.close()

        doctor_menu["values"] = doctors  # Actualizar ComboBox de médicos
        doctor_var.set("")  # Resetear selección

    # Evento para actualizar médicos al seleccionar una especialidad
    specialty_var.trace_add("write", update_doctors)

    # Selección de fecha con tkcalendar
    tk.Label(schedule_window, text="Selecciona una fecha:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=10)
    calendar = Calendar(schedule_window, date_pattern="yyyy-mm-dd", font=("Arial", 12))
    calendar.pack(pady=5)

    # Selección de hora
    tk.Label(schedule_window, text="Selecciona la hora:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=10)
    frame_time = tk.Frame(schedule_window, bg="#F0F0F0")
    frame_time.pack(pady=5)

    hour_var = tk.StringVar(value="08")
    minute_var = tk.StringVar(value="00")

    hour_spinbox = tk.Spinbox(frame_time, from_=0, to=23, width=2, textvariable=hour_var, font=("Arial", 12), format="%02.0f")
    hour_spinbox.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_time, text=":", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(side=tk.LEFT)

    minute_spinbox = tk.Spinbox(frame_time, from_=0, to=59, width=2, textvariable=minute_var, font=("Arial", 12), format="%02.0f")
    minute_spinbox.pack(side=tk.LEFT, padx=5)

    def save_appointment():
        """Guardar la cita en la base de datos."""
        specialty = specialty_var.get()
        doctor = doctor_var.get()
        date = calendar.get_date()
        time = f"{hour_var.get()}:{minute_var.get()}"
        user_id = get_user_id(username)
        doctor_id = get_medico_id(doctor)

        if not specialty or not doctor:
            messagebox.showerror("Error", "Selecciona una especialidad y un médico")
            return

        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO citas (usuario_id, medico_id, fecha, hora, estado) VALUES (?, ?, ?, ?, 'Confirmada')", 
                       (user_id, doctor_id, date, time))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita agendada correctamente")
        schedule_window.destroy()

    # Botón para agendar la cita
    tk.Button(schedule_window, text="Agendar Cita", command=save_appointment, font=("Arial", 14), bg="#4CAF50", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    

def agendarCitasAdministrador():
    """Ventana para agendar citas manualmente desde el administrador."""
    schedule_window = tk.Toplevel()
    schedule_window.geometry("600x600+500+100")
    schedule_window.title("Agendar Cita")
    schedule_window.config(bg="#F0F0F0")  # Fondo gris claro

    # Título
    tk.Label(schedule_window, text="Agendar Cita", font=("Arial", 16), bg="#F0F0F0", fg="#333333").pack(pady=3)

    # Filtro de paciente
    tk.Label(schedule_window, text="Selecciona Paciente:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=3)
    user_var = tk.StringVar()
    user_menu = ttk.Combobox(schedule_window, textvariable=user_var, font=("Arial", 12))
    user_menu.pack(pady=3)

    # Filtro de especialidad
    tk.Label(schedule_window, text="Selecciona Especialidad:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=3)
    specialty_var = tk.StringVar()
    specialty_menu = ttk.Combobox(schedule_window, textvariable=specialty_var, font=("Arial", 12), state="readonly")
    specialty_menu.pack(pady=3)

    # Filtro de médico
    tk.Label(schedule_window, text="Selecciona Médico:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=3)
    doctor_var = tk.StringVar()
    doctor_menu = ttk.Combobox(schedule_window, textvariable=doctor_var, font=("Arial", 12), state="readonly")
    doctor_menu.pack(pady=3)

    # Obtener pacientes
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE role='Paciente'")
    users = [row[0] for row in cursor.fetchall()]
    user_menu['values'] = users

    # Obtener especialidades únicas de los médicos
    cursor.execute("SELECT DISTINCT especialidad FROM medicos")
    specialties = [row[0] for row in cursor.fetchall()]
    specialty_menu['values'] = specialties

    # Función para actualizar médicos según la especialidad seleccionada
    def update_doctors(event):
        selected_specialty = specialty_var.get()
        cursor.execute("SELECT nombre FROM medicos WHERE especialidad=?", (selected_specialty,))
        doctors = [row[0] for row in cursor.fetchall()]
        doctor_menu['values'] = doctors
        doctor_var.set("")  # Limpiar selección anterior

    specialty_menu.bind("<<ComboboxSelected>>", update_doctors)

   ################ se cerro la base de datos

    # Calendario para seleccionar fecha
    tk.Label(schedule_window, text="Selecciona una fecha:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=3)
    calendar = Calendar(schedule_window, date_pattern="yyyy-mm-dd", font=("Arial", 12))
    calendar.pack(pady=3)

    # Frame para hora
    tk.Label(schedule_window, text="Selecciona la hora:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=3)
    frame_time = tk.Frame(schedule_window, bg="#F0F0F0")
    frame_time.pack(pady=3)

    hour_var = tk.StringVar(value="08")  # Hora por defecto
    minute_var = tk.StringVar(value="00")  # Minuto por defecto

    hour_spinbox = tk.Spinbox(frame_time, from_=0, to=23, width=3, textvariable=hour_var, format="%02.0f", font=("Arial", 12))
    hour_spinbox.pack(side=tk.LEFT)

    tk.Label(frame_time, text=":", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(side=tk.LEFT)  # Separador entre hora y minutos

    minute_spinbox = tk.Spinbox(frame_time, from_=0, to=59, width=3, textvariable=minute_var, format="%02.0f", font=("Arial", 12))
    minute_spinbox.pack(side=tk.LEFT)

    def save_appointment():
        """Guarda la nueva cita."""
        username = user_var.get()
        doctor = doctor_var.get()
        date = calendar.get_date()
        time = f"{hour_var.get()}:{minute_var.get()}"

        if not username or not doctor:
            messagebox.showerror("Error", "Selecciona un paciente y un médico")
            return

        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user_id = cursor.fetchone()

        cursor.execute("SELECT id FROM medicos WHERE nombre=?", (doctor,))
        doctor_id = cursor.fetchone()

        if not user_id or not doctor_id:
            messagebox.showerror("Error", "Usuario o Médico no encontrado")
            conn.close()
            return

        cursor.execute("INSERT INTO citas (usuario_id, medico_id, fecha, hora, estado) VALUES (?, ?, ?, ?, 'Confirmada')",
                       (user_id[0], doctor_id[0], date, time))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita agendada correctamente")
        schedule_window.destroy()

    # Botón para agendar cita
    tk.Button(schedule_window, text="Agendar", command=save_appointment, font=("Arial", 14), bg="#2196F3", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=5)