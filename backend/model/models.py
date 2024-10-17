from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

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

    SerialID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer)
    CustomerID = db.Column(db.Integer)
    DishID = db.Column(db.Integer)
    Rating = db.Column(db.Integer)
    Time = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Review {self.ReviewID}>"