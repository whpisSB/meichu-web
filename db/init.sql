CREATE DATABASE IF NOT EXISTS mydatabase;
-- DROP USER IF EXISTS 'user'@'%';
CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'user'@'%';
FLUSH PRIVILEGES;
USE mydatabase;

DROP TABLE IF EXISTS TSMC_User;
DROP TABLE IF EXISTS Training_Certifications;
DROP TABLE IF EXISTS Pr;
DROP TABLE IF EXISTS Reward;
DROP TABLE IF EXISTS User_Rewards;
DROP TABLE IF EXISTS Icon;

CREATE TABLE TSMC_User (
    Employee_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Github_ID VARCHAR(255),
    Email VARCHAR(255),
    Password VARCHAR(255),
    Line_ID VARCHAR(512),
    Points INT
);

CREATE TABLE Training_Certifications (
    Employee_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Training_Name VARCHAR(50) ,
    Completion_Date VARCHAR(50) ,
    Expire_Date VARCHAR(50) 
    -- FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID),
    -- PRIMARY KEY (Employee_ID, Training_Name, Completion_Date)
);

CREATE TABLE Pr (
    PrID BIGINT PRIMARY KEY AUTO_INCREMENT,
    RepositoryID VARCHAR(255),
    GithubID VARCHAR(255),
    CommitCount INT,
    Additions INT,
    Deletions INT,
    Total INT,
    Summary VARCHAR(10240),
    Reviewers VARCHAR(255)
);

CREATE TABLE Reward(
    RewardID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255),
    ThumbnailImage VARCHAR(1024),
    Description VARCHAR(1024),
    Points INT
);

-- New table to link users and rewards
CREATE TABLE User_Rewards (
    ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Line_ID VARCHAR(512),
    RewardID BIGINT
);

CREATE TABLE Icon (
    ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Employee_ID BIGINT,
    Icon VARCHAR(1024) -- An URL --
);

INSERT INTO Icon (Employee_ID, Icon) VALUES
    (1, 'https://google.com');

INSERT INTO User_Rewards (Line_ID, RewardID) VALUES
    ("line_id_ycy", 1),
    ("line_id_ycy", 2),
    ("line_id_amber", 2),
    ("Ua0e4d2058f68cfb9c16953c29bac8399", 1),
    ("Ua0e4d2058f68cfb9c16953c29bac8399", 2);

INSERT INTO TSMC_User (Name, Github_ID, Email, Password, Line_ID, Points) VALUES
    ('ycy.yo', 'ycy.yo', 'ycy.yo@gmail.com', 'password', "line_id_ycy", 200),
    ('amber chen', 'amber', 'amber@world', 'password', "line_id_amber", 200),
    ('weiling','weiling','aaa','password','Ua0e4d2058f68cfb9c16953c29bac8399',200);

INSERT INTO Reward (Title, ThumbnailImage, Description, Points) VALUES
    ('Keyboard', 'https://i.imgur.com/5HBQx1m.jpeg', 'good keyboard', 100),
    ('Apple Watch', 'https://i.imgur.com/ql0l1t5.jpeg', 'good watch', 200),
    ('Personal Icon','https://i.imgur.com/eZVZtaL.png','personal icon',200);

INSERT INTO Training_Certifications (Employee_ID, Training_Name, Completion_Date, Expire_Date) VALUES
    ('100001', 'Git & Github', '2024-01-01', '2025-01-01'),
    ('100002', 'SQL', '2024-01-01', '2025-01-01');

INSERT INTO Pr (RepositoryID, GithubID, CommitCount, Additions, Deletions, Total, Summary, Reviewers) VALUES
    ('repo', 'ycy.yo', 10, 10, 10, 10, 'summary', 'reviewers');