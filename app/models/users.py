import datetime
from app import db, ma

class Users(db.Model):# type: ignore    
    """
        Definição de classe/Tabela dos usuários e seus campos
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

class UsersSchema(ma.Schema):
    """
        Definindo o Schema do Mashmallow para facilitar a utilização de JSON
    """
    class Meta:
        fields = ('id', 'username', 'name', 'email', 'password', 'created_on')
        
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
    