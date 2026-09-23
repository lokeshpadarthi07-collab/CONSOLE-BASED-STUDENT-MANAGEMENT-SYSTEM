-- ====================================================================
-- DATABASE-DRIVEN STUDENT MANAGEMENT SYSTEM - SCHEMA & SQL PRACTICE
-- Task 2: PostgreSQL Schema DDL, DML, and Advanced SQL Queries
-- ====================================================================

-- --------------------------------------------------------------------
-- 1. CREATE TABLE STATEMENT
-- Demonstrates PRIMARY KEY, UNIQUE, NOT NULL, CHECK constraints, and DEFAULTs.
-- --------------------------------------------------------------------
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    course VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL DEFAULT 1 CHECK (year >= 1 AND year <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for high performance lookups
CREATE INDEX idx_students_student_id ON students(student_id);
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_students_course ON students(course);


-- --------------------------------------------------------------------
-- 2. ALTER TABLE STATEMENTS
-- Demonstrates modifying existing database schemas.
-- --------------------------------------------------------------------
-- Add a status column to track enrollment standing
ALTER TABLE students ADD COLUMN status VARCHAR(20) DEFAULT 'Active';

-- Add a check constraint for valid status values
ALTER TABLE students ADD CONSTRAINT chk_student_status 
    CHECK (status IN ('Active', 'Graduated', 'Suspended', 'Withdrawn'));

-- Alter column data type or constraints
ALTER TABLE students ALTER COLUMN phone SET NOT NULL;


-- --------------------------------------------------------------------
-- 3. INSERT STATEMENTS
-- Demonstrates populating normalized tables with initial data.
-- --------------------------------------------------------------------
INSERT INTO students (student_id, first_name, last_name, email, phone, date_of_birth, course, year, status)
VALUES
('STU1001', 'Alexander', 'Hamilton', 'alexander@university.edu', '+12025550101', '2001-01-11', 'Computer Science', 3, 'Active'),
('STU1002', 'Elizabeth', 'Schuyler', 'elizabeth@university.edu', '+12025550102', '2002-08-09', 'Data Science', 2, 'Active'),
('STU1003', 'Aaron', 'Burr', 'aaron.burr@university.edu', '+12025550103', '2000-02-06', 'Law & Governance', 4, 'Active'),
('STU1004', 'Angelica', 'Church', 'angelica@university.edu', '+12025550104', '1999-02-20', 'Computer Science', 4, 'Graduated'),
('STU1005', 'Marquis', 'Lafayette', 'lafayette@university.edu', '+12025550105', '2003-09-06', 'Mechanical Engineering', 1, 'Active');


-- --------------------------------------------------------------------
-- 4. UPDATE STATEMENTS
-- Demonstrates updating existing records with WHERE clauses.
-- --------------------------------------------------------------------
-- Update student phone and academic year
UPDATE students
SET phone = '+12025559999',
    year = 4,
    updated_at = CURRENT_TIMESTAMP
WHERE student_id = 'STU1001';

-- Update status for all 4th year students transitioning to graduation
UPDATE students
SET status = 'Graduated'
WHERE year = 5;


-- --------------------------------------------------------------------
-- 5. DELETE STATEMENTS
-- Demonstrates removing records based on criteria.
-- --------------------------------------------------------------------
-- Delete a student with a specific ID
DELETE FROM students
WHERE student_id = 'STU1005';


-- --------------------------------------------------------------------
-- 6. SELECT, WHERE, ORDER BY, & LIMIT STATEMENTS
-- Demonstrates filtering, sorting, and pagination.
-- --------------------------------------------------------------------
-- Basic SELECT with Column Aliases
SELECT 
    student_id AS "ID",
    first_name || ' ' || last_name AS "Full Name",
    email AS "Contact Email",
    course AS "Major",
    year AS "Year Level"
FROM students;

-- WHERE with AND, OR, LIKE, and BETWEEN filters
SELECT * 
FROM students
WHERE course = 'Computer Science' 
  AND year >= 2 
  AND email LIKE '%@university.edu';

-- ORDER BY and LIMIT (Pagination)
SELECT student_id, first_name, last_name, course, created_at
FROM students
ORDER BY created_at DESC
LIMIT 3 OFFSET 0;


-- --------------------------------------------------------------------
-- 7. GROUP BY & HAVING STATEMENTS
-- Demonstrates aggregations and group filtering.
-- --------------------------------------------------------------------
-- Count students per course and calculate average year level
SELECT 
    course,
    COUNT(id) AS total_students,
    MIN(year) AS lowest_year,
    MAX(year) AS highest_year,
    ROUND(AVG(year), 2) AS average_year
FROM students
GROUP BY course
HAVING COUNT(id) >= 1
ORDER BY total_students DESC;


-- --------------------------------------------------------------------
-- 8. JOIN STATEMENTS (RELATIONAL DATABASE DEMONSTRATION)
-- Demonstrates multi-table relational queries using INNER and LEFT JOINs.
-- --------------------------------------------------------------------
-- Secondary Table: Courses
CREATE TABLE courses (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    credits INTEGER DEFAULT 3
);

INSERT INTO courses (course_id, course_name, department, credits) VALUES
('CS101', 'Intro to Computer Science', 'Computer Science', 4),
('DS201', 'Data Structures & Algorithms', 'Data Science', 4),
('LAW301', 'Constitutional Law', 'Law & Governance', 3);

-- Tertiary Table: Enrollments
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) REFERENCES students(student_id) ON DELETE CASCADE,
    course_id VARCHAR(10) REFERENCES courses(course_id) ON DELETE CASCADE,
    grade VARCHAR(2),
    enrolled_at DATE DEFAULT CURRENT_DATE
);

INSERT INTO enrollments (student_id, course_id, grade) VALUES
('STU1001', 'CS101', 'A'),
('STU1001', 'DS201', 'A-'),
('STU1002', 'DS201', 'B+'),
('STU1003', 'LAW301', 'A');

-- Multi-table INNER JOIN query
SELECT 
    s.student_id,
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_id,
    c.course_name,
    c.department,
    e.grade
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
ORDER BY s.student_id;

-- LEFT JOIN to show all students whether enrolled in specific courses or not
SELECT 
    s.student_id,
    s.first_name || ' ' || s.last_name AS student_name,
    COALESCE(e.course_id, 'Not Enrolled') AS course_code,
    COALESCE(e.grade, 'N/A') AS final_grade
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id;
