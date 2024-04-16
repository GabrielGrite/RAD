from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = "User"
    Id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Name = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def get_id(self):
        return self.Id

class Initiative(db.Model):
    __tablename__ = "Initiative"
    Id = db.Column(db.Integer, primary_key=True)    
    Name = db.Column(db.String(255), nullable=True)
    ProjectManagerName = db.Column(db.String(255), nullable=True)
    PlannedStartDate = db.Column(db.DateTime, nullable=False)   
    PlannedEndDate = db.Column(db.DateTime, nullable=False)
    RealStartDate = db.Column(db.DateTime, nullable=True)   
    RealEndDate = db.Column(db.DateTime, nullable=True)   
    Modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Comment(db.Model):
    __tablename__ = "Comment"
    Id = db.Column(db.Integer, primary_key=True)
    Text = db.Column(db.String(255), nullable=False)
    FK_Initiative_Id = db.Column(db.Integer, db.ForeignKey('Initiative.Id'), nullable=False)
    initiative = db.relationship('Initiative', backref=db.backref('comments', lazy=True))