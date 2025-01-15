import mysql.connector
import pymysql
import os
from dotenv import load_dotenv
import logging

load_dotenv()


def get_db_connection():
    timeout = 10
    return pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    read_timeout=timeout,
    db=os.getenv("DB_NAME"),
    host=os.getenv("DB_HOST"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    write_timeout=timeout,
    )

def get_order_status(order_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Query to fetch the status
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()        
        if result and 'status' in result:
            return result['status']
        else:
            return None
    except pymysql.MySQLError as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        connection.close()





def save_to_db(order: dict):
    try:
        next_order_id = get_next_order_id()
        for food_item, qunatity in order.items():
            rcode = insert_order_item(
                food_item,
                qunatity,
                next_order_id,
            )
        if rcode == -1:
            return -1

        insert_order_tracking(next_order_id,"In Progress")

        return next_order_id
    except mysql.connector.Error as e:
        return f"Error: {e}"

def get_next_order_id():
    connection = get_db_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Fetch the maximum order_id from the orders table
        query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()       
        if result['MAX(order_id)'] is None:
            return 1
        else:
            return result['MAX(order_id)'] + 1
    except pymysql.MySQLError as e:
        logging.error(f"Error fetching next order ID: {e}")
        return f"Error: {e}"
    finally:
        if cursor:
            cursor.close()
        connection.close()
    



def insert_order_item(food_item, quantity, order_id):
    connection = get_db_connection()
    cursor = None
    try:
        cursor = connection.cursor()

        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        connection.commit()
        cursor.close()
        return 1

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        connection.rollback()
        return -1

def get_total_price(order_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    # Fetching the result
    result = cursor.fetchone()
    cursor.close()

    return result[f'get_total_order_price({order_id})']

def get_item_price(item_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Properly format the item_name as a string with quotes
    query = f"SELECT get_price_for_item('{item_name}')"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()
    cursor.close()

    return result[f"get_price_for_item('{item_name}')"]

# print(get_item_price("samosa"))

def insert_order_tracking(order_id, status):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    connection.commit()

    # Closing the cursor
    cursor.close()

