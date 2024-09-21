import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de conexión para el superusuario de PostgreSQL
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

# Conectar a PostgreSQL sin especificar la base de datos para crearla
try:
    conn = psycopg2.connect(
        dbname='postgres',  # Conectar a la base de datos por defecto
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Necesario para crear la BD
    cursor = conn.cursor()

    # Comando para verificar si la base de datos ya existe
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}';")
    exists = cursor.fetchone()

    if not exists:
        # Si la base de datos no existe, crearla
        cursor.execute(f"CREATE DATABASE {dbname};")
        print(f"Base de datos '{dbname}' creada con éxito.")
    else:
        print(f"La base de datos '{dbname}' ya existe.")

except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
