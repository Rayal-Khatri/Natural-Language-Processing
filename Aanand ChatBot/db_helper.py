import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Doramon9841',
        database='pandeyji_eatery'
    )

def get_order_status(order_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Query to fetch the status
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as e:
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()