CREATE DATABASE IF NOT EXISTS mydatabase;
DROP USER IF EXISTS 'user'@'%';
CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'user'@'%';
FLUSH PRIVILEGES;
USE mydatabase;

DROP TABLE IF EXISTS Staff_Info;
DROP TABLE IF EXISTS Dish_Info;
DROP TABLE IF EXISTS Restaurant_Info;
DROP TABLE IF EXISTS Order_Dish;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Review;

CREATE TABLE Employee (
    Employee_ID VARCHAR(10) PRIMARY KEY NOT NULL,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    Date_Of_Birth DATE,
    Hire_Date DATE NOT NULL,
    Termination_Date DATE,
    Status ENUM('Active', 'Terminated') NOT NULL
);

CREATE TABLE Training_Certifications (
    Employee_ID VARCHAR(10) NOT NULL,
    Training_Name VARCHAR(100) NOT NULL,
    Completion_Date DATE NOT NULL,
    Expire_Date DATE,
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
    PRIMARY KEY (Employee_ID, Training_Name, Completion_Date)
);

CREATE TABLE Performance_Reviews (
    Employee_ID VARCHAR(10) NOT NULL,
    Review_Date DATE NOT NULL,
    Reviewer_ID VARCHAR(10) NOT NULL,
    Performance_Score DECIMAL(4,2) NOT NULL,
    Feedback TEXT,
    PRIMARY KEY (Employee_ID, Review_Date),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
    FOREIGN KEY (Reviewer_ID) REFERENCES Employee(Employee_ID)
);

CREATE TABLE Awards (
    Employee_ID VARCHAR(10) NOT NULL,
    Award_Name VARCHAR(100) NOT NULL,
    Award_Description TEXT,
    Award_Date DATE NOT NULL,
    PRIMARY KEY (Employee_ID, Award_Name, Award_Date),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

CREATE TABLE Skills (
    Employee_ID VARCHAR(10) NOT NULL,
    Skill_Name VARCHAR(100) NOT NULL,
    Skill_Level ENUM('Beginner', 'Intermediate', 'Advanced', 'Expert') NOT NULL,
    PRIMARY KEY (Employee_ID, Skill_Name),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

CREATE TABLE Disciplinary_Records (
    Employee_ID VARCHAR(10) NOT NULL,
    Incident_Date DATE NOT NULL,
    Incident_Type ENUM('Verbal Warning', 'Written Warning', 'Suspension', 'Termination') NOT NULL,
    Incident_Description TEXT,
    Disciplinary_Action_Taken VARCHAR(100) NOT NULL,
    Disciplinary_Action_Date DATE NOT NULL,
    PRIMARY KEY (Employee_ID, Incident_Date),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

INSERT into Employee(Employee_ID, First_Name, Last_Name, Date_Of_Birth, Hire_Date, Termination_Date, Status) VALUES
    ('100001', 'adam', 'zheng', '2000-01-01', '2024-01-01', NULL, 'Active'),
    ('100002', 'detaomega', 'Yang', '2000-01-01', '2024-01-01', NULL, 'Active'),
    ('100003', 'supervisor', 'supervisor', '2000-01-01', '2024-01-01', NULL, 'Active');

INSERT INTO Training_Certifications (Employee_ID, Training_Name, Completion_Date, Expire_Date) VALUES
    ('100001', 'Git & Github', '2024-01-01', '2025-01-01'),
    ('100002', 'SQL', '2024-01-01', '2025-01-01');

INSERT INTO Performance_Reviews (Employee_ID, Review_Date, Reviewer_ID, Performance_Score, Feedback) VALUES
    ('100001', '2024-01-01', '100003', 4.5, 'Good job'),
    ('100002', '2024-01-01', '100003', 4.5, 'Good job');

INSERT INTO Awards (Employee_ID, Award_Name, Award_Description, Award_Date) VALUES
    ('100001', 'Employee of the Month', 'Good job', '2024-01-01'),
