-- Create the ai_development database
CREATE DATABASE IF NOT EXISTS ai_development;
USE ai_development;

-- Create students table
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    semester INT NOT NULL,
    CHECK (semester BETWEEN 1 AND 4)
);

-- Create marks table
CREATE TABLE marks (
    mark_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    semester INT NOT NULL,
    gpa DECIMAL(3,2) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    CHECK (semester BETWEEN 1 AND 4),
    CHECK (gpa BETWEEN 0.00 AND 4.00)
);

-- Create fees table
CREATE TABLE fees (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    semester INT NOT NULL,
    paid DECIMAL(10,2) DEFAULT 0.00,
    pending DECIMAL(10,2) DEFAULT 0.00,
    total DECIMAL(10,2) GENERATED ALWAYS AS (paid + pending) STORED,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    CHECK (semester BETWEEN 1 AND 4)
);

-- Insert sample data into students
INSERT INTO students (student_name, semester) VALUES
('Peter Pandey', 1),
('Peter Pandey', 2),
('Jane Smith', 1),
('Jane Smith', 2);

-- Insert sample data into marks
INSERT INTO marks (student_id, semester, gpa) VALUES
(1, 1, 3.70),
(1, 2, 3.50),
(2, 1, 3.90),
(2, 2, 3.80);

-- Insert sample data into fees
INSERT INTO fees (student_id, semester, paid, pending) VALUES
(1, 1, 5000.00, 2000.00),
(1, 2, 6000.00, 1500.00),
(2, 1, 5500.00, 1800.00),
(2, 2, 6200.00, 1200.00);

-- Create stored procedure get_marks
DELIMITER //
CREATE PROCEDURE get_marks(
    IN student_name VARCHAR(100),
    IN semester INT,
    IN operation VARCHAR(10)
)
BEGIN
    DECLARE student_exists INT;

    -- Check if student exists for the given semester
    SELECT COUNT(*) INTO student_exists
    FROM students s
    WHERE s.student_name = student_name AND s.semester = semester;

    IF student_name = '' AND operation IN ('max', 'min', 'avg') THEN
        -- Aggregate queries
        IF operation = 'max' THEN
            SELECT MAX(gpa) as result
            FROM marks m
            JOIN students s ON m.student_id = s.student_id
            WHERE m.semester = semester;
        ELSEIF operation = 'min' THEN
            SELECT MIN(gpa) as result
            FROM marks m
            JOIN students s ON m.student_id = s.student_id
            WHERE m.semester = semester;
        ELSEIF operation = 'avg' THEN
            SELECT AVG(gpa) as result
            FROM marks m
            JOIN students s ON m.student_id = s.student_id
            WHERE m.semester = semester;
        END IF;
    ELSEIF student_exists > 0 THEN
        -- Individual student GPA
        SELECT gpa
        FROM marks m
        JOIN students s ON m.student_id = s.student_id
        WHERE s.student_name = student_name AND m.semester = semester;
    ELSE
        SELECT -1 as result;
    END IF;
END //
DELIMITER ;

-- Create stored procedure get_fees
DELIMITER //
CREATE PROCEDURE get_fees(
    IN student_name VARCHAR(100),
    IN semester INT,
    IN fees_type VARCHAR(10)
)
BEGIN
    DECLARE student_exists INT;

    -- Check if student exists for the given semester
    SELECT COUNT(*) INTO student_exists
    FROM students s
    WHERE s.student_name = student_name AND s.semester = semester;

    IF student_name = '' AND fees_type IN ('total') THEN
        -- Total fees for all students in the semester
        SELECT SUM(total) as result
        FROM fees f
        JOIN students s ON f.student_id = s.student_id
        WHERE f.semester = semester;
    ELSEIF student_exists > 0 THEN
        -- Individual student fees
        IF fees_type = 'paid' THEN
            SELECT paid as result
            FROM fees f
            JOIN students s ON f.student_id = s.student_id
            WHERE s.student_name = student_name AND f.semester = semester;
        ELSEIF fees_type = 'pending' THEN
            SELECT pending as result
            FROM fees f
            JOIN students s ON f.student_id = s.student_id
            WHERE s.student_name = student_name AND f.semester = semester;
        ELSEIF fees_type = 'total' THEN
            SELECT total as result
            FROM fees f
            JOIN students s ON f.student_id = s.student_id
            WHERE s.student_name = student_name AND f.semester = semester;
        ELSE
            SELECT -1 as result;
        END IF;
    ELSE
        SELECT -1 as result;
    END IF;
END //
DELIMITER ;
