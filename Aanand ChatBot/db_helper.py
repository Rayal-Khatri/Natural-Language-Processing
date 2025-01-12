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
    try:
        cursor = connection.cursor()
        
        # Fetch the maximum order_id from the orders table
        query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        if result is None:
            return 1
        else:
            return result + 1
    except mysql.connector.Error as e:
        return f"Error: {e}"
    


def insert_order_item(food_item, quantity, order_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()

        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        connection.commit()
        cursor.close()
        return 1
        
        # Insert the order item into the orders table
        # query = "INSERT INTO orders (order_id, food_item, quantity) VALUES (%s, %s, %s)"
        # cursor.execute(query, (order_id, food_item, quantity))
        
        # connection.commit()
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
  result = cursor.fetchone()[0]

  # Closing the cursor
  cursor.close()

  return result



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

