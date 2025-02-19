from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class TSMC_User(db.Model):
    __tablename__ = 'TSMC_User'
    Employee_ID = db.Column(db.Integer, primary_key=True)
    Github_ID = db.Column(db.String(255))
    Name = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Line_ID = db.Column(db.String(512))
    Points = db.Column(db.Integer)
    Total_Points = db.Column(db.Integer)
    _Group = db.Column(db.String(255))

class Training_Certifications(db.Model):
    __tablename__ = 'Training_Certifications'

    Employee_ID = db.Column(db.Integer, primary_key=True)
    Training_Name = db.Column(db.String(255))
    Completion_Date = db.Column(db.String(255))
    Expire_Date = db.Column(db.String(255))

    def __repr__(self):
        return f"<Training_Certifications {self.Employee_ID}>"

class Pr(db.Model):
    __tablename__ = 'Pr'

    PrID = db.Column(db.Integer, primary_key=True)
    RepositoryID = db.Column(db.String(255))
    GithubID = db.Column(db.String(255))
    CommitCount = db.Column(db.Integer)
    Additions = db.Column(db.Integer)
    Deletions = db.Column(db.Integer)
    Total = db.Column(db.Integer)
    Summary = db.Column(db.String(10240))
    Reviewers = db.Column(db.String(255))

    def __repr__(self):
        return f"<Pr {self.PrID}>"

class Reward(db.Model):
    __tablename__ = 'Reward'

    RewardID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    ThumbnailImage = db.Column(db.String(1024))
    Description = db.Column(db.String(1024))
    Points = db.Column(db.Integer)

    def __repr__(self):
        return f"<Reward {self.RewardID}>"

class User_Rewards(db.Model):
    __tablename__ = 'User_Rewards'

    ID = db.Column(db.Integer, primary_key=True)
    Line_ID = db.Column(db.String(512))
    RewardID = db.Column(db.Integer)

    def __repr__(self):
        return f"<User_Rewards {self.ID}>"

class Dish_Info(db.Model):
    __tablename__ = 'Dish_Info'

    DishID = db.Column(db.Integer, primary_key=True)
    RestaurantID = db.Column(db.Integer)
    Name = db.Column(db.String(255))
    Description = db.Column(db.String(1000))
    Combo = db.Column(db.Boolean)
    Picture = db.Column(db.String(255))
    Price = db.Column(db.Integer)
    Available= db.Column(db.Boolean)
    TimesOfOrder = db.Column(db.Integer)
    RatingCnt = db.Column(db.Integer)
    Rating = db.Column(db.Float)

    def __repr__(self):
        return f"<Dish_Information {self.Name}>"

class Restaurant_Info(db.Model):
    __tablename__ = 'Restaurant_Info'

    RestaurantID = db.Column(db.Integer, primary_key=True)
    RestaurantName = db.Column(db.String(255))
    PhoneNumber = db.Column(db.Integer)
    OpenTime = db.Column(db.DateTime)
    CloseTime = db.Column(db.DateTime)
    Description = db.Column(db.String(1000))
    Picture = db.Column(db.String(255))
    RatingCnt = db.Column(db.Integer)
    Rating = db.Column(db.Float)

    def __repr__(self):
        return f"<Restaurant_Information {self.RestaurantName}>"
    
class Order_Dish(db.Model):
    __tablename__ = 'Order_Dish'

    SerialID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer)
    DishID = db.Column(db.Integer)
    Number = db.Column(db.Integer)

    def __repr__(self):
        return f"<Order_Dish {self.OrderID}>"

class Orders(db.Model):
    __tablename__ = 'Orders'

    OrderID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer)
    RestaurantID = db.Column(db.Integer)
    TotalPrice = db.Column(db.Integer)
    OrderTime = db.Column(db.DateTime)
    Finish = db.Column(db.Boolean)
    Reviewed = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Orders {self.OrderID}>"

class Review(db.Model):
    __tablename__ = 'Review'

    ReviewID = db.Column(db.Integer, primary_key=True)
    AuthorGithubID = db.Column(db.String(255))
    PRUrl = db.Column(db.String(255))
    ReviewerGithubID = db.Column(db.String(255))
    Points = db.Column(db.Integer)
    ReviewAt = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Review {self.ReviewID}>"

class Staff_Info(db.Model):
    __tablename__ = 'Staff_Info'

    StaffID = db.Column(db.Integer, primary_key=True)
    StaffName = db.Column(db.String(255))
    Position = db.Column(db.String(255))
    Gmail = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    PhoneNumber = db.Column(db.Integer)
    Paid = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Staff_Information {self.StaffID}>"