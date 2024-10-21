import mysql.connector

def get_db_connection():
    """Returns a connection to the database."""
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="Alumnat",
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    return connection