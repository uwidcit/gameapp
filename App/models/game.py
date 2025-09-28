from App.database import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
 
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f'<Game {self.id} - {self.title}>'