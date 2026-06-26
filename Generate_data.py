from DATA.database import GetConnection
import random

colleges = [
    ("COE", "College of Engineering"),
    ("CSM", "College of Science and Mathematics"),
    ("CED", "College of Education"),
    ("CASS", "College of Arts and Social Sciences"),
    ("CHS", "College of Health Sciences"),
    ("CEBA", "College of Economics, Business and Accountancy"),
    ("CCS", "College of Computer Studies"),
]

programs = [
    ("BSMETE", "Bachelor of Science in Metallurgical Engineering", "COE"),
    ("BET-CHET", "Bachelor of Engineering Technology Major in Chemical Engineering Technology", "COE"),
    ("BET-ELET", "Bachelor of Engineering Technology Major in Electrical Engineering Technology", "COE"),
    ("BSME", "Bachelor of Science in Mechanical Engineering", "COE"),
    ("BSEM", "Bachelor of Science in Mining Engineering", "COE"),
    ("BET-MET", "Bachelor of Engineering Technology Major in Mechanical Engineering Technology", "COE"),
    ("BSEE", "Bachelor of Science in Electrical Engineering", "COE"),
    ("BET-ESET", "Bachelor of Engineering Technology Major in Electronics Engineering Technology", "COE"),
    ("BSCE", "Bachelor of Science in Civil Engineering", "COE"),
    ("BSCERE", "Bachelor of Science in Ceramic Engineering", "COE"),
    ("BSCHE", "Bachelor of Science in Chemical Engineering", "COE"),
    ("BSEsE", "Bachelor of Science in Electronics Engineering", "COE"),
    ("BSEnE", "Bachelor of Science in Environmental Engineering", "COE"),
    ("BET-MMT", "Bachelor of Engineering Technology Major in Metallurgical and Materials Engineering Technology", "COE"),
    ("BSCPE", "Bachelor of Science in Computer Engineering", "COE"),
    ("BSIAM", "Bachelor of Science in Industrial Automation and Mechatronics", "COE"),
    ("BET-CET", "Bachelor of Engineering Technology Major in Civil Engineering Technology", "COE"),
    ("BS-MB", "Bachelor of Science in Marine Biology", "CSM"),
    ("BSBio-AB", "Bachelor of Science in Biology Major in Animal Biology", "CSM"),
    ("BSStat", "Bachelor of Science in Statistics", "CSM"),
    ("BSBio-PB", "Bachelor of Science in Biology Major in Plant Biology", "CSM"),
    ("BSChem", "Bachelor of Science in Chemistry", "CSM"),
    ("BSBio-Micro", "Bachelor of Science in Biology Major in Microbiology", "CSM"),
    ("BSMath", "Bachelor of Science in Mathematics", "CSM"),
    ("BSBio-Bdv", "Bachelor of Science in Biology Major in Biodiversity", "CSM"),
    ("BSPhys", "Bachelor of Science in Physics", "CSM"),
    ("BTLEd-IA", "Bachelor of Technology and Livelihood Education Major in Industrial Arts", "CED"),
    ("CPRT", "Certificate Program in Radiologic Technology", "CED"),
    ("BEEd-SM", "Bachelor of Elementary Education Major in Science and Mathematics", "CED"),
    ("BSEd-Phys", "Bachelor of Secondary Education Major in Physics", "CED"),
    ("BSEd-Math", "Bachelor of Secondary Education Major in Mathematics", "CED"),
    ("BSEd-Chem", "Bachelor of Secondary Education Major in Chemistry", "CED"),
    ("BTLEd-HE", "Bachelor of Technology and Livelihood Education Major in Home Economics", "CED"),
    ("BEEd-LE", "Bachelor of Elementary Education Major in Language Education", "CED"),
    ("BPEd", "Bachelor of Physical Education", "CED"),
    ("BSEd-Fil", "Bachelor of Secondary Education Major in Filipino", "CED"),
    ("BSEd-Bio", "Bachelor of Secondary Education Major in Biology", "CED"),
    ("BTVTEd-DT", "Bachelor of Technical-Vocational Teacher Education Major in Drafting Technology", "CED"),
    ("BAELS", "Bachelor of Arts in English Language Studies", "CASS"),
    ("BAPos", "Bachelor of Arts in Political Science", "CASS"),
    ("BSPsych", "Bachelor of Science in Psychology", "CASS"),
    ("BAPsych", "Bachelor of Arts in Psychology", "CASS"),
    ("BASoc", "Bachelor of Arts in Sociology", "CASS"),
    ("BSPhil", "Bachelor of Science in Philosophy Applied Ethics", "CASS"),
    ("BAPan", "Batsilyer ng Sining sa Panitikan", "CASS"),
    ("BAHis", "Bachelor of Arts in History", "CASS"),
    ("BALCS", "Bachelor of Arts in Literary and Cultural Studies", "CASS"),
    ("BAFil", "Batsilyer ng Sining sa Filipino", "CASS"),
    ("BSN", "Bachelor of Science in Nursing", "CHS"),
    ("BSA", "Bachelor of Science in Accountancy", "CEBA"),
    ("BSBA-BE", "Bachelor of Science in Business Administration Major in Business Economics", "CEBA"),
    ("BSBA-MM", "Bachelor of Science in Business Administration Major in Marketing Management", "CEBA"),
    ("BSHM", "Bachelor of Science in Hospitality Management", "CEBA"),
    ("BSEcon", "Bachelor of Science in Economics", "CEBA"),
    ("BSEntrep", "Bachelor of Science in Entrepreneurship", "CEBA"),
    ("BSCS", "Bachelor of Science in Computer Science", "CCS"),
    ("BSIT", "Bachelor of Science in Information Technology", "CCS"),
    ("BSIS", "Bachelor of Science in Information System", "CCS"),
    ("BSCA", "Bachelor of Science in Computer Application", "CCS"),
]

first_names = [
    "John", "Mary", "James", "Patricia", "Robert", "Jennifer",
    "Michael", "Linda", "William", "Barbara", "David", "Susan",
    "Richard", "Jessica", "Joseph", "Sarah", "Thomas", "Karen",
    "Charles", "Lisa", "Christopher", "Nancy", "Daniel", "Betty",
    "Matthew", "Margaret", "Anthony", "Sandra", "Mark", "Ashley"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
    "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez",
    "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
    "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
]


def insert_colleges(cursor):
    inserted = 0
    skipped = 0
    for college_code, college_name in colleges:
        try:
            cursor.execute("""
                INSERT INTO college (college_code, college_name)
                VALUES (%s, %s)
            """, (college_code, college_name))
            inserted += 1
        except Exception as e:
            print(f"  Skipped college {college_code}: {e}")
            skipped += 1
    print(f"Colleges  — Inserted: {inserted} | Skipped: {skipped}")


def insert_programs(cursor):
    inserted = 0
    skipped = 0
    for program_code, program_name, college_code in programs:
        try:
            cursor.execute("""
                INSERT INTO program (program_code, program_name, college_code)
                VALUES (%s, %s, %s)
            """, (program_code, program_name, college_code))
            inserted += 1
        except Exception as e:
            print(f"  Skipped program {program_code}: {e}")
            skipped += 1
    print(f"Programs  — Inserted: {inserted} | Skipped: {skipped}")


def insert_students(cursor, count=5000):
    inserted = 0
    skipped = 0

    # Get all valid program codes instead of ids
    cursor.execute("SELECT program_code FROM program")
    program_codes = [row[0] for row in cursor.fetchall()]

    if not program_codes:
        print("  No programs found! Skipping students.")
        return

    genders = ["Male", "Female"]
    years = [1, 2, 3, 4]

    for i in range(1, count + 1):
        student_id = [f"2023-{str(i).zfill(4)}", f"2024-{str(i).zfill(4)}", f"2025-{str(i).zfill(4)}", f"2026-{str(i).zfill(4)}"][random.randint(0, 3)]
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        gender = random.choice(genders)
        year = random.choice(years)
        program_code = random.choice(program_codes)  # ← random program code

        try:
            cursor.execute("""
                INSERT INTO students (student_id, first_name, last_name, gender, year, program_code)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (student_id, first_name, last_name, gender, year, program_code))
            inserted += 1
        except Exception as e:
            print(f"  Skipped student {student_id}: {e}")
            skipped += 1
    print(f"Students  — Inserted: {inserted} | Skipped: {skipped}")

def insert_all():
    conn = GetConnection()
    cursor = conn.cursor()

    print("Starting data insertion...")
    print("─" * 40)

    insert_colleges(cursor)
    conn.commit()

    insert_programs(cursor)
    conn.commit()

    insert_students(cursor, count=5000)
    conn.commit()

    conn.close()
    print("─" * 40)
    print("All done!")

insert_all()