import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

from modelo.bd_citas_centro_medico import get_user_id

def cancelarCitasPaciente(username):
    """Ventana para cancelar una cita médica."""
    cancel_window = tk.Toplevel()
    cancel_window.title("Cancelar Cita")
    cancel_window.geometry("600x500+500+100")
    cancel_window.config(bg="#F0F0F0")

    # Título de la ventana
    tk.Label(cancel_window, text="Cancelar Cita Médica", font=("Arial", 16, "bold"), bg="#F0F0F0", fg="#333333").pack(pady=20)

    # Instrucción
    tk.Label(cancel_window, text="Selecciona una cita a cancelar:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=10)

    # Tabla para mostrar citas
    tree = ttk.Treeview(cancel_window, columns=("ID", "Fecha", "Hora", "Médico"), show='headings', height=8)
    tree.heading("ID", text="ID")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Hora", text="Hora")
    tree.heading("Médico", text="Especialidad - Médico")  # Se cambia el encabezado

    # Establecer el ancho de las columnas y su alineación
    tree.column("ID", width=80, anchor="center")
    tree.column("Fecha", width=120, anchor="center")
    tree.column("Hora", width=100, anchor="center")
    tree.column("Médico", width=250, anchor="w")  # Más ancho para incluir especialidad

    # Estilo de la tabla
    tree.tag_configure('even', background="#f9f9f9")
    tree.tag_configure('odd', background="#e9e9e9")

    tree.pack(pady=10)

    # Cargar las citas del usuario
    user_id = get_user_id(username)

    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, c.fecha, c.hora, m.especialidad, m.nombre 
        FROM citas c 
        JOIN medicos m ON c.medico_id = m.id 
        WHERE c.usuario_id = ? AND c.estado = 'Confirmada'
    """, (user_id,))

    for idx, row in enumerate(cursor.fetchall()):
        cita_id, fecha, hora, especialidad, medico = row
        medico_con_especialidad = f"{especialidad} - {medico}"  # Concatenar especialidad y nombre
        tag = 'even' if idx % 2 == 0 else 'odd'  # Alternar color de fila
        tree.insert("", "end", values=(cita_id, fecha, hora, medico_con_especialidad), tags=(tag,))

    conn.close()

    # Función para cancelar una cita seleccionada
    def cancel_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita")
            return

        item = tree.item(selected_item)
        appointment_id = item['values'][0]

        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE citas SET estado = 'Cancelada' WHERE id = ?", (appointment_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita cancelada correctamente")
        cancel_window.destroy()

    # Botón para cancelar la cita seleccionada
    tk.Button(cancel_window, text="Cancelar Cita", command=cancel_selected, font=("Arial", 12), bg="#F44336", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=20)
    
    
    
def cancelarCitaAdmin():
    """Ventana para editar, cancelar o reactivar citas."""
    edit_window = tk.Toplevel()
    edit_window.geometry("900x400+400+100")
    edit_window.title("Administrar Citas")
    edit_window.config(bg="#F0F0F0")

    # Título
    tk.Label(edit_window, text="Administrar Citas", font=("Arial", 16), bg="#F0F0F0", fg="#333333").pack(pady=10)

    # Tabla para mostrar citas
    columns = ("ID", "Paciente", "Fecha", "Hora", "Médico", "Especialidad", "Estado")
    tree = ttk.Treeview(edit_window, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    tree.pack(pady=10, padx=10, fill="both", expand=True)

    # Obtener citas de la base de datos
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, u.username, c.fecha, c.hora, m.nombre, m.especialidad, c.estado 
        FROM citas c
        JOIN users u ON c.usuario_id = u.id
        JOIN medicos m ON c.medico_id = m.id
    """)
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)

    # Función para cancelar cita
    def cancel_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita")
            return

        item = tree.item(selected_item)
        appointment_id = item['values'][0]

        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE citas SET estado='Cancelada' WHERE id=?", (appointment_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita cancelada correctamente")
        edit_window.destroy()

    # Función para reactivar cita
    def reactivate_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita")
            return

        item = tree.item(selected_item)
        appointment_id = item['values'][0]

        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE citas SET estado='Confirmada' WHERE id=?", (appointment_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cita reactivada correctamente")
        edit_window.destroy()

    # Función para editar cita
    def edit_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita")
            return

        item = tree.item(selected_item)
        appointment_id = item['values'][0]
        current_date = item['values'][2]
        current_time = item['values'][3]
        current_doctor = item['values'][4]

        edit_popup = tk.Toplevel()
        edit_popup.geometry("500x600+500+100")
        edit_popup.title("Editar Cita")
        edit_popup.config(bg="#F0F0F0")

        tk.Label(edit_popup, text="Editar Cita", font=("Arial", 14), bg="#F0F0F0", fg="#333333").pack(pady=10)

        tk.Label(edit_popup, text="Nueva Fecha:", font=("Arial", 12), bg="#F0F0F0").pack(pady=5)
        calendar = Calendar(edit_popup, date_pattern="yyyy-mm-dd")
        calendar.pack(pady=5)
        calendar.selection_set(current_date)

        tk.Label(edit_popup, text="Nueva Hora:", font=("Arial", 12), bg="#F0F0F0").pack(pady=5)
        frame_time = tk.Frame(edit_popup, bg="#F0F0F0")
        frame_time.pack(pady=5)

        hour_var = tk.StringVar(value=current_time.split(":")[0])
        minute_var = tk.StringVar(value=current_time.split(":")[1])

        tk.Spinbox(frame_time, from_=0, to=23, width=3, textvariable=hour_var, format="%02.0f", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Label(frame_time, text=":", font=("Arial", 12), bg="#F0F0F0").pack(side=tk.LEFT)
        tk.Spinbox(frame_time, from_=0, to=59, width=3, textvariable=minute_var, format="%02.0f", font=("Arial", 12)).pack(side=tk.LEFT)

        # Cargar especialidades en un Combobox
        tk.Label(edit_popup, text="Especialidad:", font=("Arial", 12), bg="#F0F0F0").pack(pady=5)
        specialty_var = tk.StringVar()
        specialty_menu = ttk.Combobox(edit_popup, textvariable=specialty_var, font=("Arial", 12))
        specialty_menu.pack(pady=5)

        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT especialidad FROM medicos")
        specialties = [row[0] for row in cursor.fetchall()]
        conn.close()
        specialty_menu['values'] = specialties

        # Cargar médicos según la especialidad seleccionada
        tk.Label(edit_popup, text="Nuevo Médico:", font=("Arial", 12), bg="#F0F0F0").pack(pady=5)
        doctor_var = tk.StringVar(value="")
        doctor_menu = ttk.Combobox(edit_popup, textvariable=doctor_var, font=("Arial", 12))
        doctor_menu.pack(pady=5)

        def update_doctors(event):
            selected_specialty = specialty_var.get()
            conn = sqlite3.connect("medical_center.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM medicos WHERE especialidad=?", (selected_specialty,))
            doctors = [row[0] for row in cursor.fetchall()]
            conn.close()
            doctor_menu['values'] = doctors
            

        specialty_menu.bind("<<ComboboxSelected>>", update_doctors)

        def save_changes():
            new_date = calendar.get_date()
            new_time = f"{hour_var.get()}:{minute_var.get()}"
            new_doctor = doctor_var.get()

            if not new_date or not new_time or not new_doctor:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            conn = sqlite3.connect("medical_center.db")
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM medicos WHERE nombre=?", (new_doctor,))
            doctor_id = cursor.fetchone()

            if not doctor_id:
                messagebox.showerror("Error", "Médico no encontrado")
                conn.close()
                return

            cursor.execute("""
                UPDATE citas 
                SET fecha=?, hora=?, medico_id=?
                WHERE id=?
            """, (new_date, new_time, doctor_id[0], appointment_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Cita actualizada correctamente")
            edit_popup.destroy()
            edit_window.destroy()

        tk.Button(edit_popup, text="Guardar Cambios", command=save_changes, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, bd=0, relief="flat").pack(pady=20)

    
    
    # Botones
    button_frame = tk.Frame(edit_window, bg="#F0F0F0")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Editar Cita", command=edit_selected, font=("Arial", 12), bg="#FFC107", fg="black", width=15, bd=0, relief="flat").grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Cancelar Cita", command=cancel_selected, font=("Arial", 12), bg="#F44336", fg="white", width=15, bd=0, relief="flat").grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Reactivar Cita", command=reactivate_selected, font=("Arial", 12), bg="#2196F3", fg="white", width=15, bd=0, relief="flat").grid(row=0, column=2, padx=10)
    
    
