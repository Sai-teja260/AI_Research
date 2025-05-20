import mysql.connector

def get_db_connection():
    """Establish a connection to the MySQL database."""
    connection = mysql.connector.connect(
        host="82.29.165.165",  # Change if your database is hosted elsewhere
        user="test",  # Replace with your database username
        password="Test@553311",  # Replace with your actual password
        database="ai_development"  # Replace with your database name
    )
    return connection

def get_marks(params):
    """Call the get_marks stored procedure with the given parameters."""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Prepare parameters for the stored procedure
        student_name = params.get("student_name", "")
        semester = params["semester"]
        operation = params.get("operation", "")

        # Call the stored procedure
        cursor.callproc("get_marks", [student_name, semester, operation])

        # Fetch the result
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                return row[0]  # Assuming the GPA is the first column
            else:
                return -1  # No record found
    finally:
        cursor.close()
        connection.close()

def get_fees(params):
    """Call the get_fees stored procedure with the given parameters."""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Prepare parameters for the stored procedure
        student_name = params.get("student_name", "")
        semester = params["semester"]
        fees_type = params.get("fees_type", "")

        # Call the stored procedure
        cursor.callproc("get_fees", [student_name, semester, fees_type])

        # Fetch the result
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                return row[0]  # Assuming the fees are the first column
            else:
                return -1  # No record found
    finally:
        cursor.close()
        connection.close()
