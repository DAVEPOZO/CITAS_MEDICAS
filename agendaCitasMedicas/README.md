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
    python loginC.py

### Estuctura ###
/agendaCitas
├── dashboardAdmin.py         # Código para el panel de administración
├── dashboardPaciente.py      # Código para el panel del paciente
├── loginC.py                 # Código para el inicio de sesión
├── bd_citas_centro_medico.py # Código para gestionar la base de datos
├── requirements.txt          # Dependencias del proyecto

### Tecnologias usadas ###
Python 3
Tkinter
SQLite