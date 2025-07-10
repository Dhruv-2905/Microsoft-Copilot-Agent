from typing import List
from connection.database_connection import connect_to_postgresql
from query.models import UserResponse , StatusCountResponse


def get_users_by_name(name: str) -> List[UserResponse]:
    connection, cursor = connect_to_postgresql()

    try:
        query = f"SELECT * FROM testing.userdata WHERE name = %s;"
        cursor.execute(query, (name,))
        result = cursor.fetchone()

        if not result:
            raise ValueError("No users found with this name")

        users = UserResponse(user_id=result[0], name=result[1], email=result[2], balance=result[3], po_status=result[4], po_value=result[5],po_number=result[6], supplier=result[7], quantity=result[8], order_description=result[9])


        return users

    finally:
        cursor.close()
        connection.close()

def get_users_by_status(status: str, name: str) -> List[UserResponse]:
    
    connection, cursor = connect_to_postgresql()

    try:
        if name:
            query = """
                SELECT *
                FROM testing.userdata
                WHERE po_status = %s AND name = %s;
            """
            cursor.execute(query, (status, name))
        
        rows = cursor.fetchall()
        users = [UserResponse(
                    user_id=row[0],
                    name=row[1],
                    email=row[2],
                    balance=row[3],
                    po_status=row[4],
                    po_value=row[5],
                    po_number=row[6],
                    supplier=row[7],
                    quantity=row[8],
                    order_description=row[9]
                ) for row in rows]
        
        return users   

    finally:
        cursor.close()
        connection.close()
        
def get_users_by_first_name(name: str) -> List[int]:
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    try:
        query = "query for getting user name from table = %s;"
        cursor.execute(query, (name,))
        
        rows = cursor.fetchall()
        vendor_ids = ', '.join(str(row[0]) for row in rows)
        
        return vendor_ids
    finally:
        cursor.close()
        conn.close()
        
