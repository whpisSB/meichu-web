CREATE DATABASE IF NOT EXISTS mydatabase;
-- DROP USER IF EXISTS 'user'@'%';
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
DROP TABLE IF EXISTS Training_Certifications;

CREATE TABLE Staff_Info (
    StaffID BIGINT PRIMARY KEY,
    StaffName VARCHAR(255),
    Position VARCHAR(255),
    Gmail VARCHAR(255),
    Password VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Paid BOOLEAN,
    Email VARCHAR(255)
);

CREATE TABLE Dish_Info(
    DishID BIGINT PRIMARY KEY AUTO_INCREMENT,
    RestaurantID BIGINT,
    Name VARCHAR(255),
    Description VARCHAR(1000),
    Combo BOOLEAN,
    Picture VARCHAR(255),
    Price INT,
    Available BOOLEAN,
    TimesOfOrder INT,
    RatingCnt INT,
    Rating FLOAT
);

CREATE TABLE Restaurant_Info (
    RestaurantID BIGINT PRIMARY KEY AUTO_INCREMENT,
    RestaurantName VARCHAR(255),
    PhoneNumber VARCHAR(20),
    OpenTime TIME,
    CloseTime TIME,
    Description VARCHAR(1000),
    Picture VARCHAR(255),
    RatingCnt INT,
    Rating FLOAT
);

CREATE TABLE Order_Dish(
    SerialID BIGINT PRIMARY KEY AUTO_INCREMENT,
    OrderID BIGINT,
    DishID BIGINT,
    Number INT
);

CREATE TABLE Orders (
    OrderID BIGINT PRIMARY KEY AUTO_INCREMENT,
    CustomerID BIGINT,
    RestaurantID BIGINT,
    TotalPrice INT,
    OrderTime TIMESTAMP,
    Finish BOOLEAN,
    Reviewed BOOLEAN
);

CREATE TABLE Review(
    SerialID BIGINT PRIMARY KEY AUTO_INCREMENT,
    OrderID BIGINT,
    CustomerID BIGINT,
    DishID BIGINT, -- DishID = 0 means review the whole restaurant
    Rating BIGINT,
    Time TIMESTAMP
);

CREATE TABLE TSMC_User (
    Employee_ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Line_ID VARCHAR(255),
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
    Line_ID VARCHAR(255),
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
    ("line_id_ycy", 1);

INSERT INTO TSMC_User (Name, Email, Line_ID, Points) VALUES
    ('ycy.yo', 'ycy.yo@gmail.com', "line_id_ycy", 200),
    ('amber chen', 'amber@world', "line_id_amber", 200);

INSERT INTO Reward (Title, ThumbnailImage, Description, Points) VALUES
    ('Keyboard', 'https://i.imgur.com/5HBQx1m.jpeg', 'good keyboard', 100),
    ('Apple Watch', 'https://i.imgur.com/ql0l1t5.jpeg', 'good watch', 200);

INSERT INTO Training_Certifications (Employee_ID, Training_Name, Completion_Date, Expire_Date) VALUES
    ('100001', 'Git & Github', '2024-01-01', '2025-01-01'),
    ('100002', 'SQL', '2024-01-01', '2025-01-01');

INSERT INTO Pr (RepositoryID, GithubID, CommitCount, Additions, Deletions, Total, Summary, Reviewers) VALUES
    ('repo', 'ycy.yo', 10, 10, 10, 10, 'summary', 'reviewers');

INSERT INTO Staff_Info (StaffID, StaffName, Position, Gmail, Password, PhoneNumber, Paid) VALUES
    (100001, 'ycy.yo', 'restaurant_1', 'ycy.yo@gmail.com', 'test', '0909090909', FALSE),
    (100002, 'amber chen', 'admin', 'hello@world', 'test', '0910101010', FALSE),
    (100003, 'whoami', 'restaurant_2', 'who@ami', 'test', '0911111111', FALSE),
    (100004, 'benson', 'worker', 'benson@gmail.com', 'test', '0912345678', FALSE),
    (100005, 'detaomega', 'worker', 'detaomega@gmail.com', 'test', '0912345678', FALSE),
    (100006, 'BruceLin', 'worker', 'bruce@gmail.com', 'test', '0943134344', FALSE);

INSERT INTO Dish_Info (RestaurantID, Name, Description, Combo, Picture, Price, Available, TimesOfOrder, RatingCnt, Rating) VALUES
    (1, 'Fried Chicken', 'Delicious', FALSE, 'chicken.jpg', 200, TRUE, 1, 0, 0),
    (1, 'Hamburger', 'Delicious', FALSE, 'chicken.jpg', 150, TRUE, 1, 0, 0),
    (1, 'French Fries', 'Delicious', FALSE, 'chicken.jpg', 100, TRUE, 0, 0, 0),
    (1, 'Six Nuggets with Coke', 'Delicious', TRUE, 'chicken.jpg', 150, TRUE, 0, 0, 0),
    (2, 'Cookie', 'Delicious', FALSE, 'chicken.jpg', 30, TRUE, 1, 1, 5),
    (2, 'Veggie Delite', 'Delicious', FALSE, 'chicken.jpg', 150, FALSE, 0, 0, 0),
    (2, 'Tuna', 'Delicious', FALSE, 'chicken.jpg', 170, TRUE, 0, 0, 0),
    (3, 'Pepperoni Pizza', 'Delicious', FALSE, 'chicken.jpg', 200, TRUE, 1, 1, 3),
    (3, 'Hawaiian Pizza', 'Delicious', FALSE, 'chicken.jpg', 150, TRUE, 2, 1, 4),
    (3, 'Cheese Pizza', 'Delicious', FALSE, 'chicken.jpg', 100, FALSE, 0, 0, 0);

INSERT INTO Restaurant_Info  (RestaurantName, PhoneNumber, OpenTime, CloseTime, Description, Picture, RatingCnt, Rating) VALUES
    ('KFC', '0912345678', '12:00:00', '22:00:00', 'Fast Food Restaurant', 'kfc.png', 0, 0),
    ('Subway', '0912345678', '08:00:00', '22:00:00', 'Sandwich', 'kfc.png', 1, 5),
    ('Pizza Hut', '0912345678', '08:00:00', '22:00:00', 'Pizza', 'kfc.png', 1, 4);

INSERT INTO Order_Dish (OrderID, DishID, Number) VALUES
    (1, 1, 1),
    (1, 2, 1),
    (2, 5, 1),
    (3, 8, 1),
    (3, 9, 2);

INSERT INTO Orders (CustomerID, RestaurantID, TotalPrice, OrderTime, Finish, Reviewed) VALUES
    (100003, 1, 350, CURRENT_TIMESTAMP, FALSE, FALSE),
    (100006, 2, 30, '2024-06-01 12:00:00', TRUE, TRUE),
    (100005, 3, 500, '2024-06-01 20:00:00', TRUE, TRUE);

INSERT INTO Review (OrderID, CustomerID, DishID, Rating, Time) VALUES
    (3, 100005, 8, 3, '2024-06-01 21:00:00'),
    (3, 100005, 9, 4, '2024-06-01 21:00:00'),
    (3, 100005, 0, 4, '2024-06-01 21:00:00'),
    (2, 100006, 5, 5, '2024-06-01 15:00:00'),
    (2, 100006, 0, 5, '2024-06-01 15:00:00');