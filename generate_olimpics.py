import psycopg2
import secrets
import string
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Función para generar contraseñas aleatorias
def generar_password(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for i in range(longitud))

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

# Archivo para guardar las contraseñas
archivo_passwords = "passwords_usuarios.txt"

# Comienza una transacción
conn.autocommit = False
cursor = conn.cursor()

# Diccionario para almacenar usuarios y contraseñas
usuarios_passwords = {}

try:
    # Crear los esquemas
    for esquema in esquemas:
        crear_esquema_sql = f"CREATE SCHEMA IF NOT EXISTS {esquema};"
        cursor.execute(crear_esquema_sql)
        default_privileges_sql = f"ALTER DEFAULT PRIVILEGES IN SCHEMA {esquema} GRANT SELECT, REFERENCES ON TABLES TO PUBLIC;"
        cursor.execute(default_privileges_sql)

    with open(archivo_passwords, 'w') as archivo:
        for i, usuario in enumerate(usuarios):
            # Generar una contraseña aleatoria para cada usuario
            password = generar_password()
            usuarios_passwords[usuario] = password

            # Crear el usuario con restricciones (NOCREATEDB, NOCREATEROLE)
            crear_usuario_sql = f"CREATE USER {usuario} WITH PASSWORD %s NOCREATEDB NOCREATEROLE;"
            cursor.execute(crear_usuario_sql, (password,))

            # Darle acceso solo a la base de datos olimpicos
            grant_connect_sql = f"GRANT CONNECT ON DATABASE olimpicos TO {usuario};"
            cursor.execute(grant_connect_sql)

            # Asignar todos los privilegios en el esquema correspondiente (su propio esquema)
            esquema = esquemas[i]
            grant_privilegios_sql = f"GRANT ALL PRIVILEGES ON SCHEMA {esquema} TO {usuario};"
            cursor.execute(grant_privilegios_sql)

            # Revocar permisos para crear bases de datos
            revoke_create_db_sql = f"REVOKE CREATE ON DATABASE olimpicos FROM {usuario};"
            cursor.execute(revoke_create_db_sql)

            # Otorgar permisos en otros esquemas (USAGE, SELECT, REFERENCES)
            for esquema_lectura in esquemas:
                if esquema_lectura != esquema:
                    grant_lectura_referencias_sql = f"""
                    GRANT USAGE ON SCHEMA {esquema_lectura} TO {usuario};
                    GRANT SELECT ON ALL TABLES IN SCHEMA {esquema_lectura} TO {usuario};
                    GRANT REFERENCES ON ALL TABLES IN SCHEMA {esquema_lectura} TO {usuario};
                    """
                    cursor.execute(grant_lectura_referencias_sql)

            # Establecer permisos predeterminados para futuras tablas creadas por este usuario
            for esquema_predeterminado in esquemas:
                if esquema_predeterminado != esquema:
                    alter_default_privileges_sql = f"""
                    ALTER DEFAULT PRIVILEGES FOR ROLE {usuario} IN SCHEMA {esquema_predeterminado}
                    GRANT SELECT, REFERENCES ON TABLES TO {usuario};
                    """
                    cursor.execute(alter_default_privileges_sql)

            # Revocar conexión a otras bases de datos (template0, template1, postgres)
            revoke_connect_template0_sql = f"REVOKE CONNECT ON DATABASE template0 FROM {usuario};"
            cursor.execute(revoke_connect_template0_sql)
            revoke_connect_template1_sql = f"REVOKE CONNECT ON DATABASE template1 FROM {usuario};"
            cursor.execute(revoke_connect_template1_sql)
            revoke_connect_postgres_sql = f"REVOKE CONNECT ON DATABASE postgres FROM {usuario};"
            cursor.execute(revoke_connect_postgres_sql)

            # Revocar cualquier acceso a esquemas y objetos que no sean equipoX
            revoke_privileges_public_schema_sql = f"REVOKE ALL PRIVILEGES ON SCHEMA public FROM {usuario};"
            cursor.execute(revoke_privileges_public_schema_sql)
            revoke_privileges_public_tables_sql = f"REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {usuario};"
            cursor.execute(revoke_privileges_public_tables_sql)

            # Escribir el usuario y contraseña en el archivo
            archivo.write(f"Usuario: {usuario}, Contraseña: {password}\n")

    # Confirma la transacción
    conn.commit()
    print("Esquemas, usuarios y permisos creados con éxito. Contraseñas almacenadas en", archivo_passwords)

except Exception as e:
    # Si ocurre algún error, revierte la transacción
    conn.rollback()
    print(f"Error: {e}")

finally:
    # Cierra la conexión
    cursor.close()
    conn.close()
