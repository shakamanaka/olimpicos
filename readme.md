
# Proyecto de Base de Datos Olímpicos

Este proyecto tiene como objetivo crear un entorno colaborativo para el desarrollo de una base de datos de los Juegos Olímpicos. Está diseñado para ser gestionado por 10 equipos diferentes, cada uno con acceso a su propio esquema y privilegios personalizados dentro de la base de datos. Los scripts en este repositorio facilitan la creación y administración de la base de datos y los usuarios asociados.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos en tu entorno:

- Python 3.x
- Librerías necesarias (puedes instalarlas con el archivo `requirements.txt` si es necesario)
- Acceso a una base de datos (por ejemplo, PostgreSQL, MySQL, etc.)

## Configuración del Proyecto

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/shakamanaka/olimpicos.git
   cd olimpicos
   ```

2. **Configurar las variables de entorno**:

   Copia el archivo `.env.example` a un archivo llamado `.env` y ajusta las variables necesarias para tu entorno de base de datos.

   ```bash
   cp .env.example .env
   ```

   Abre el archivo `.env` y modifica las siguientes variables:

   ```bash
   DB_HOST=localhost
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_NAME=nombre_de_la_base_de_datos
   ```

## Scripts Disponibles

Este proyecto incluye cuatro scripts en Python que deben ejecutarse en el siguiente orden:

1. **`crear_db.py`**: Este script crea la estructura de la base de datos. Es el primer script que debe ejecutarse.

   ```bash
   python crear_db.py
   ```

2. **`generate_olimpics.py`**: Este script genera los usuarios y esquemas necesarios en la base de datos. Ejecuta este script una vez que la base de datos haya sido creada.

   ```bash
   python generate_olimpics.py
   ```

3. **`privileges.py`**: Otorga los privilegios necesarios a los usuarios creados en el paso anterior, permitiendo que cada equipo pueda operar en su respectivo esquema.

   ```bash
   python privileges.py
   ```

4. **`borrar.py`**: Este script es opcional y sirve para eliminar datos o limpiar la base de datos si es necesario.

   ```bash
   python borrar.py
   ```

## Contribuyendo

Este proyecto es colaborativo. Si deseas contribuir, asegúrate de seguir las convenciones de estilo de código y de hacer pruebas exhaustivas antes de enviar un pull request.
