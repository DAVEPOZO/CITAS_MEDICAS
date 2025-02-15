import sqlite3



def create_db():
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL CHECK(role IN ('Paciente', 'Admin'))
                    )''')
    
    # Crear tabla de médicos
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        especialidad TEXT NOT NULL
                    )''')
    
    # Crear tabla de citas
    cursor.execute('''CREATE TABLE IF NOT EXISTS citas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario_id INTEGER NOT NULL,
                        medico_id INTEGER NOT NULL,
                        fecha DATE NOT NULL,
                        hora TIME NOT NULL,
                        estado TEXT NOT NULL CHECK(estado IN ('Confirmada', 'Cancelada')),
                        FOREIGN KEY(usuario_id) REFERENCES users(id),
                        FOREIGN KEY(medico_id) REFERENCES medicos(id)
                    )''')
    
    # Insertar médicos predeterminados si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM medicos")
    if cursor.fetchone()[0] == 0:
        medicos_predeterminados = [
            ("Dr. Juan Pérez", "Cardiología"),
            ("Dra. Ana Gómez", "Pediatría"),
            ("Dr. Carlos Ramírez", "Dermatología"),
            ("Dra. Laura Torres", "Neurología")
        ]
        cursor.executemany("INSERT INTO medicos (nombre, especialidad) VALUES (?, ?)", medicos_predeterminados)
    
    conn.commit()
    conn.close()

def get_user_id(username):
    """Obtiene el ID del usuario a partir del nombre de usuario."""
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

def get_medico_id(doctor_name):
    """Obtiene el ID del médico a partir de su nombre."""
    conn = sqlite3.connect("medical_center.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM medicos WHERE nombre=?", (doctor_name,))
    doctor_id = cursor.fetchone()
    conn.close()
    return doctor_id[0] if doctor_id else None