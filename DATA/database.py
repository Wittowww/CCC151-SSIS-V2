import mysql.connector
from mysql.connector import pooling
from config import DB_CONFIG

try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name = "student_management_pool",
        pool_size = 5,
        **DB_CONFIG
    )
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    connection_pool = None

def GetConnection():
    return connection_pool.get_connection() 