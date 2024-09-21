import psycopg2
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de conexión a la base de datos
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

# Lista de esquemas y usuarios que se van a borrar
esquemas = [f"equipo{i}" for i in range(1, 11)]
usuarios = [f"admin{i}" for i in range(1, 11)]

# Comienza una transacción
conn.autocommit = False
cursor = conn.cursor()

try:
    # Borrar todos los esquemas generados
    for esquema in esquemas:
        drop_esquema_sql = f"DROP SCHEMA IF EXISTS {esquema} CASCADE;"
        cursor.execute(drop_esquema_sql)
        print(f"Esquema {esquema} eliminado.")

    # Borrar todos los usuarios generados
    for usuario in usuarios:
        drop_usuario_sql = f"DROP USER IF EXISTS {usuario};"
        cursor.execute(drop_usuario_sql)
        print(f"Usuario {usuario} eliminado.")

    # Confirma la transacción
    conn.commit()
    print("Todos los esquemas y usuarios han sido eliminados con éxito.")

except Exception as e:
    # Si ocurre algún error, revierte la transacción
    conn.rollback()
    print(f"Error: {e}")

finally:
    # Cierra la conexión
    cursor.close()
    conn.close()
