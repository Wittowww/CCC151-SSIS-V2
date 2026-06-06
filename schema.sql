USE student_management;

CREATE TABLE college (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_code VARCHAR(20),
    college_name VARCHAR(100),
    UNIQUE (college_code)
);

CREATE TABLE program (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program_code VARCHAR(20),
    program_name VARCHAR(50),
    college_code VARCHAR(20),
    UNIQUE (program_code),
    FOREIGN KEY(college_code) REFERENCES college(college_code) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(9),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    program_code VARCHAR(20),
    year INT,
    gender VARCHAR(10),
    UNIQUE (student_id),
    CHECK (student_id REGEXP '^[0-9]{4}-[0-9]{4}$'),
    FOREIGN KEY(program_code) REFERENCES program(program_code) ON DELETE SET NULL ON UPDATE CASCADE
);