from DATA.database import GetConnection

# COLLEGE COMMANDS
def get_all_college():
    connection = GetConnection()
    try:
        cursor = connection.cursor(dictionary = True)
        cursor.execute ("SELECT * FROM college")
        return cursor.fetchall()
    finally:
        connection.close()

def add_college(college_name, college_code):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """INSERT INTO college (college_code, college_name) VALUES (%s, %s) """,
            (college_code, college_name)
        )
        connection.commit()
    finally:
        connection.close()

def delete_college(college_id):
    connection = GetConnection()
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT college_code FROM college WHERE id = %s", (college_id,))
        row = cursor.fetchone()
        if not row:
            return False
        
        college_code = row[0]

        cursor.execute(
            "UPDATE program SET college_code = 'N/A' WHERE college_code = %s",
            (college_code,)
        )

        cursor.execute("DELETE FROM college WHERE id = %s", (college_id,))

        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Delete college error: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def update_college(college_id, college_name, college_code):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """UPDATE college 
            SET 
            college_name = %s, 
            college_code = %s 
            WHERE 
            id = %s """,
            (college_name, college_code, college_id)
            )
        connection.commit()
    finally:
        connection.close()


# PROGRAM COMMANDS
def get_all_program():
    connection = GetConnection()
    try:
        cursor = connection.cursor(dictionary = True)
        cursor.execute ("""
            SELECT 
                p.id,
                p.program_code,
                p.program_name,
                c.college_code
            FROM program p
            LEFT JOIN college c ON p.college_code = c.college_code
        """)
        return cursor.fetchall()
    finally:
        connection.close()

def add_program(program_code, program_name, college_code):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """INSERT INTO program (program_code, program_name, college_code) VALUES (%s, %s, %s) """,
            (program_code, program_name, college_code)
            )
        connection.commit()
    finally:
        connection.close()

def delete_program(program_id):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """DELETE FROM program WHERE id = %s """,
            (program_id,)
            )
        connection.commit()
        rows_affected = cursor.rowcount
        return rows_affected > 0
    finally:
        connection.close()

def update_program(program_name, program_code, college_code, program_id):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """UPDATE program 
            SET 
            program_name = %s, 
            program_code = %s,
            college_code = %s
            WHERE 
            id = %s """,
            (program_name, program_code, college_code, program_id)
            )
        connection.commit()
    finally:
        connection.close()


# STUDENTS COMMANDS
def get_all_students():
    connection = GetConnection()
    try:
        cursor = connection.cursor(dictionary = True)
        cursor.execute ("""
            SELECT 
                s.id,
                s.student_id,
                s.first_name,
                s.last_name,
                s.gender,
                s.year,
                COALESCE(s.program_code, 'N/A') AS program_code
            FROM students s
            LEFT JOIN program p ON s.program_code = p.program_code
        """)
        return cursor.fetchall()
    finally:
        connection.close()


def add_students(student_id, first_name, last_name, gender, year, program_code):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """INSERT INTO students (student_id, first_name, last_name, gender, year, program_code) VALUES (%s, %s, %s, %s, %s, %s) """,
            (student_id, first_name, last_name, gender, year, program_code)
            )
        connection.commit()
    finally:
        connection.close()

def delete_students(student_id):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """DELETE FROM students WHERE id = %s """,
            (student_id,)
            )
        connection.commit()
        rows_affected = cursor.rowcount
        return rows_affected > 0
    finally:
        connection.close()

def update_students(student_id, first_name, last_name, gender, year, program_code,strecord_id):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """UPDATE students 
            SET 
            student_id = %s,
            first_name = %s,
            last_name = %s,
            gender = %s,
            year = %s,
            program_code = %s
            WHERE 
            id = %s """,
            (student_id, first_name, last_name, gender, year, program_code,strecord_id)
            )
        connection.commit()
    finally:
        connection.close()