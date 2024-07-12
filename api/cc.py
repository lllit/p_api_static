import mysql.connector
from mysql.connector import Error

from albums_data import data_albums

# Conectar a la base de datos
try:
    connection = mysql.connector.connect(
        host='localhost',        # Cambia esto si tu base de datos no está en localhost
        user='root',       # Cambia esto por tu nombre de usuario de MySQL
        password='Homero123', # Cambia esto por tu contraseña de MySQL
        database='lllit_data'       # Cambia esto si tu base de datos tiene otro nombre
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Insertar datos
        insert_query = """
        INSERT INTO albums (name_album, url_spotify, image, release_date)
        VALUES (%s, %s, %s, %s)
        """
        for album in data_albums:
            cursor.execute(insert_query, (album['name_album'], album['url']['spotify'], album['image'], album['release_date']))

        # Confirmar los cambios
        connection.commit()
        print("Datos insertados exitosamente en la tabla albums.")

except Error as e:
    print(f"Error al conectar a MySQL: {e}")

finally:
    try:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada.")
    except NameError:
        print("La conexión no se estableció correctamente.")