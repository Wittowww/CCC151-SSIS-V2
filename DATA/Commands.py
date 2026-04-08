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
        cursor.execute (
            """DELETE FROM college WHERE id = %s """,
            (college_id,)
        )
        connection.commit()
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
            JOIN college c ON p.college_code = c.college_code
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
                p.program_code
            FROM students s
            JOIN program p ON s.program_code = p.program_code
        """)
        return cursor.fetchall()
    finally:
        connection.close()


def add_students(students_id, first_name, last_name, gender, year, program_code):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """INSERT INTO students (students_id, first_name, last_name, gender, year, program_code) VALUES (%s, %s, %s, %s, %s, %s) """,
            (students_id, first_name, last_name, gender, year, program_code)
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
    finally:
        connection.close()

def update_students(students_id, first_name, last_name, gender, year, program_code, student_id):
    connection = GetConnection()
    try:
        cursor = connection.cursor()
        cursor.execute (
            """UPDATE students 
            SET 
            students_id = %s,
            first_name = %s,
            last_name = %s,
            gender = %s,
            year = %s,
            program_code = %s
            WHERE 
            id = %s """,
            (students_id, first_name, last_name, gender, year, program_code, student_id)
            )
        connection.commit()
    finally:
        connection.close()