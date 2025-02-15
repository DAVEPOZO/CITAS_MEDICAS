import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from tkinter import filedialog, messagebox

def exportar_citas_a_pdf(username):

    # Conectar a la base de datos para obtener el user_id y el rol
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, role FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()

    if not user_data:
        messagebox.showerror("Error", "Usuario no encontrado en la base de datos.")
        conn.close()
        return
    
    user_id, role = user_data  # Extraer ID y rol del usuario

    # Construir consulta SQL según el rol
    if role == "Admin":
        query = """
            SELECT c.id, u.username, m.nombre, m.especialidad, c.fecha, c.hora, c.estado 
            FROM citas c
            JOIN users u ON c.usuario_id = u.id
            JOIN medicos m ON c.medico_id = m.id
        """
        cursor.execute(query)
        title_text = "Resumen de Citas Médicas (Todas)"
    else:  # Paciente
        query = """
            SELECT c.id, u.username, m.nombre, m.especialidad, c.fecha, c.hora, c.estado 
            FROM citas c
            JOIN users u ON c.usuario_id = u.id
            JOIN medicos m ON c.medico_id = m.id
            WHERE c.usuario_id = ?
        """
        cursor.execute(query, (user_id,))
        title_text = "Mis Citas Médicas"

    citas = cursor.fetchall()
    conn.close()

    if not citas:
        messagebox.showinfo("Sin datos", "No hay citas disponibles para exportar.")
        return

    # Pedir ubicación para guardar el archivo
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return  # Si el usuario cancela, salir

    # Crear PDF
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    # Título
    title = [[title_text]]
    title_table = Table(title, colWidths=[500])
    title_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 14),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12)
    ]))
    elements.append(title_table)

    # Encabezados de la tabla
    table_data = [["ID", "Paciente", "Doctor", "Especialidad", "Fecha", "Hora", "Estado"]]

    # Agregar citas a la tabla
    for cita in citas:
        table_data.append(list(cita))

    # Crear tabla con formato
    table = Table(table_data, colWidths=[40, 80, 100, 100, 80, 60, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Construir PDF
    pdf.build(elements)

    messagebox.showinfo("Éxito", "El resumen de citas ha sido guardado como PDF.")
