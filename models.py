from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Table for relationship many to many
cursos_users = db.Table(
    'cursos_users',
    db.Column('curso_id', db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Strin(100), unique=True, nullable=False)
    profile = db.relationship('Profile', backref="user", useList=False) # <Profile 1> # One to One
    todos = db.relataionship('Task', backref="user", lazy=True) # select, joined, subquery # [<Task 1>, <Task 2>] One to Many
    
    #cursos = db.relationship('Curso', secondary=cursos_users, lazy="subquery")
    cursos = db.relationship('Curso', secondary=cursos_users, lazy="subquery", backref=db.backref('users', lazy=True)) # Many to Many
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "profile": self.profile.serialize(),
            "todos": self.get_todos()
        }
        
        """ 
            {
                "id": 1,
                "username": "lrodriguez",
                "profile": {
                    "id": self.id,
                    "biography": "Teacher"
                }
            }
        """    
        
    def get_todos(self):
        return list(map(lambda task: task.serialize(), self.todos))
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    
class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.String(300), default="")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    
    def serialize(self):
        return {
            "id": self.id,
            "biography": self.biography,
            "username": self.user.username
        }
        
        
class Task(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done,
            "username": self.user.username
        }
        
        
class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    #users = db.relationship('User', secondary=cursos_users, lazy="subquery")