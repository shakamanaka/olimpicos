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

# Lista de esquemas y usuarios
esquemas = [f"equipo{i}" for i in range(1, 11)]
usuarios = [f"admin{i}" for i in range(1, 11)]



# Comienza una transacción
conn.autocommit = False
cursor = conn.cursor()

try:
    # Crear los esquemas
    for esquema in esquemas:
        for i, usuario in enumerate(usuarios):
          grant_lectura_referencias_sql = f"""
          GRANT USAGE ON SCHEMA {esquema} TO {usuario};
          GRANT SELECT ON ALL TABLES IN SCHEMA {esquema} TO {usuario};
          GRANT REFERENCES ON ALL TABLES IN SCHEMA {esquema} TO {usuario};
          """
          cursor.execute(grant_lectura_referencias_sql)
    
    conn.commit()
    print("Privilegios guardados")

except Exception as e:
    # Si ocurre algún error, revierte la transacción
    conn.rollback()
    print(f"Error: {e}")

finally:
    # Cierra la conexión
    cursor.close()
    conn.close()
