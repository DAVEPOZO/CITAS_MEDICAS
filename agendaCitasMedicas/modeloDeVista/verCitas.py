
import sqlite3
import tkinter as tk

from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

from modelo.bd_citas_centro_medico import get_user_id


def verCitasPaciente(username):
    """Ventana para que el paciente vea sus citas médicas."""
    view_window = tk.Toplevel()
    view_window.title("Mis Citas")
    view_window.geometry("700x600+500+100")
    view_window.config(bg="#F0F0F0")

    # Título
    tk.Label(view_window, text="Mis Citas Médicas", font=("Arial", 16, "bold"), bg="#F0F0F0", fg="#333333").pack(pady=5)

    # Selección de fecha con calendario
    tk.Label(view_window, text="Selecciona una fecha para ver citas:", font=("Arial", 12), bg="#F0F0F0", fg="#333333").pack(pady=5)
    calendar = Calendar(view_window, date_pattern="yyyy-mm-dd", font=("Arial", 12))
    calendar.pack(pady=10)

    # Tabla para mostrar citas
    tree = ttk.Treeview(view_window, columns=("Fecha", "Hora", "Médico", "Estado"), show='headings', height=5)
    tree.heading("Fecha", text="Fecha")
    tree.heading("Hora", text="Hora")
    tree.heading("Médico", text="Especialidad - Médico")
    tree.heading("Estado", text="Estado")

    # Ajuste de columnas
    tree.column("Fecha", width=100, anchor="center")
    tree.column("Hora", width=80, anchor="center")
    tree.column("Médico", width=250, anchor="w")  # Más ancho para incluir especialidad
    tree.column("Estado", width=120, anchor="center")

    tree.pack(pady=10)

    # Estilo de la tabla
    tree.tag_configure('even', background="#f9f9f9")
    tree.tag_configure('odd', background="#e9e9e9")

    user_id = get_user_id(username)

    def load_appointments():
        """Carga todas las citas del paciente y resalta las fechas en el calendario."""
        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.fecha, c.hora, m.especialidad, m.nombre, c.estado 
            FROM citas c 
            JOIN medicos m ON c.medico_id = m.id 
            WHERE c.usuario_id = ?
        """, (user_id,))

        rows = cursor.fetchall()
        conn.close()

        # Limpiar la tabla antes de agregar nuevas citas
        tree.delete(*tree.get_children())

        # Almacenar fechas con citas
        fechas_con_citas = set()

        for idx, row in enumerate(rows):
            fecha, hora, especialidad, medico, estado = row
            medico_con_especialidad = f"{especialidad} - {medico}"  # Concatenar especialidad y nombre
            tag = 'even' if idx % 2 == 0 else 'odd'  # Alternar color de fila
            tree.insert("", "end", values=(fecha, hora, medico_con_especialidad, estado), tags=(tag,))
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
            fechas_con_citas.add(fecha_dt)

        # Borrar eventos previos del calendario
        calendar.calevent_remove('all')

        # Resaltar los días con citas
        for fecha in fechas_con_citas:
            calendar.calevent_create(fecha, "Cita", "appointment")

        # Aplicar un estilo al resaltado de citas
        calendar.tag_config('appointment', background="red", foreground="white")

    def filter_by_date():
        """Filtra y muestra solo las citas del día seleccionado en el calendario."""
        selected_date = calendar.get_date()

        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.fecha, c.hora, m.especialidad, m.nombre, c.estado 
            FROM citas c 
            JOIN medicos m ON c.medico_id = m.id 
            WHERE c.usuario_id = ? AND c.fecha = ?
        """, (user_id, selected_date))

        rows = cursor.fetchall()
        conn.close()

        tree.delete(*tree.get_children())  # Limpiar la tabla antes de agregar nuevas citas
        for idx, row in enumerate(rows):
            fecha, hora, especialidad, medico, estado = row
            medico_con_especialidad = f"{especialidad} - {medico}"
            tag = 'even' if idx % 2 == 0 else 'odd'
            tree.insert("", "end", values=(fecha, hora, medico_con_especialidad, estado), tags=(tag,))

    # Botón para filtrar citas por fecha
    tk.Button(view_window, text="Filtrar por fecha", command=filter_by_date, font=("Arial", 12), bg="#2196F3", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)
    
    # Botón para ver todas las citas
    tk.Button(view_window, text="Ver todas las citas", command=load_appointments, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=10)

    load_appointments()  # Cargar citas al abrir la ventana
    

def verCitasAdmin():
    """Ventana para ver todas las citas con filtros."""
    view_window = tk.Toplevel()
    view_window.geometry("800x600+500+100")  # Ajustar tamaño para la nueva columna
    view_window.title("Todas las Citas")
    view_window.config(bg="#F0F0F0")  # Fondo gris claro

    # Título
    tk.Label(view_window, text="Filtrar por fecha:", font=("Arial", 14), bg="#F0F0F0", fg="#333333").pack(pady=10)

    selected_date = tk.StringVar(value="")

    def on_date_selected(event):
        selected_date.set(calendar.get_date())

    # Calendario para seleccionar la fecha
    calendar = Calendar(view_window, date_pattern="yyyy-mm-dd", background="lightblue", foreground="black", font=("Arial", 12))
    calendar.pack(pady=5)
    calendar.bind("<<CalendarSelected>>", on_date_selected)

    # Filtro por médico
    tk.Label(view_window, text="Filtrar por médico:", font=("Arial", 14), bg="#F0F0F0", fg="#333333").pack(pady=5)
    doctor_var = tk.StringVar()
    doctor_menu = ttk.Combobox(view_window, textvariable=doctor_var, font=("Arial", 12))
    doctor_menu.pack(pady=5)

    # Obtener médicos disponibles
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM medicos")
    doctors = [row[0] for row in cursor.fetchall()]
    conn.close()
    doctor_menu['values'] = doctors

    # Tabla de citas con Especialidad
    tree = ttk.Treeview(view_window, columns=("ID", "Paciente", "Fecha", "Hora", "Médico", "Especialidad", "Estado"), show="headings", height=5)
    tree.heading("ID", text="ID")
    tree.heading("Paciente", text="Paciente")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Hora", text="Hora")
    tree.heading("Médico", text="Médico")
    tree.heading("Especialidad", text="Especialidad")  # Nueva columna
    tree.heading("Estado", text="Estado")

    # Establecer el tamaño de las columnas y su alineación
    tree.column("ID", width=60, anchor="center")
    tree.column("Paciente", width=100, anchor="center")
    tree.column("Fecha", width=100, anchor="center")
    tree.column("Hora", width=80, anchor="center")
    tree.column("Médico", width=180, anchor="w")  
    tree.column("Especialidad", width=150, anchor="center")  # Nueva columna
    tree.column("Estado", width=120, anchor="center")

    tree.pack(pady=5)

    # Estilo de la tabla
    tree.tag_configure('even', background="#f9f9f9")
    tree.tag_configure('odd', background="#e9e9e9")

    def load_appointments():
        """Carga todas las citas o aplica filtros."""
        conn = sqlite3.connect("medical_center.db")
        cursor = conn.cursor()

        query = """
            SELECT c.id, u.username, c.fecha, c.hora, m.nombre, m.especialidad, c.estado 
            FROM citas c
            JOIN users u ON c.usuario_id = u.id
            JOIN medicos m ON c.medico_id = m.id
        """
        filters = []
        params = []

        if selected_date.get():
            filters.append("c.fecha = ?")
            params.append(selected_date.get())

        if doctor_var.get():
            filters.append("m.nombre = ?")
            params.append(doctor_var.get())

        if filters:
            query += " WHERE " + " AND ".join(filters)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        tree.delete(*tree.get_children())  # Limpiar tabla antes de cargar nuevos datos

        fechas_con_citas = set()

        for row in rows:
            tree.insert("", "end", values=row)
            fecha_dt = datetime.strptime(row[2], "%Y-%m-%d").date()
            fechas_con_citas.add(fecha_dt)

        # Resaltar los días con citas en el calendario
        calendar.calevent_remove('all')  
        for fecha in fechas_con_citas:
            calendar.calevent_create(fecha, "Cita", "appointment")

        calendar.tag_config('appointment', background="red", foreground="white")

    def reset_filters():
        selected_date.set("")
        doctor_var.set("")
        load_appointments()

    # Botones con estilo
    tk.Button(view_window, text="Filtrar", command=load_appointments, font=("Arial", 12), bg="#2196F3", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=6)
    tk.Button(view_window, text="Ver Todas", command=reset_filters, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, height=2, bd=0, relief="flat").pack(pady=6)

    load_appointments() 