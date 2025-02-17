# Sistema de Gestión de Citas Médicas

Este proyecto es una aplicación de escritorio para la gestión de citas médicas. Permite a los pacientes y administradores gestionar las citas médicas, agregar doctores y más. La aplicación está construida con Python y utiliza una base de datos SQLite para almacenar los datos.

## Cómo configurar y ejecutar el proyecto

### Requisitos previos:
1. **Python**: Tener instalado Python 3.13.0 o superior.
2. **Instalar dependencias**: Instalar las dependencias necesarias utilizando `pip`. Desde el directorio del proyecto, ejecuta:
   ```bash
   pip install -r requirements.txt

### Ejecutar El proyecto ###
Una vez que hayas configurado el entorno, simplemente ejecuta el siguiente comando desde la terminal o desde un editor de codigo:
    python -m main.py

### Estuctura ###
/agendaCitas
│── modelo/                  # Lógica de base de datos y consultas
│   ├── bd_citas_centro_medico.py  # Creación y gestión de la base de datos
│
│── modeloDeVista/           # Lógica de la aplicación (acciones del usuario)
│   ├── agendarCitas.py
│   ├── AgregarDoctroAdmin.py
│   ├── editarCancelarCitas.py
│   ├── export_pdf.py
│   ├── login.py
│   ├── registrar.py
│   ├── verCitas.py
│
│── vista/                   # Interfaz gráfica de usuario (Tkinter)
│   ├── dashboardAdmin.py
│   ├── dashboardPaciente.py
│   │── main.py                # Archivo principal para ejecutar la app
│── medical_center.db          # Base de datos SQLite
│── README.md                  # Documentación del proyecto
│── requirements.txt           # Dependencias necesarias




### Tecnologias usadas ###
Python 3
Tkinter
SQLite
reportlab
