from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class Webuser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        return '<WebUser %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    webuser_id = db.Column(db.Integer, db.ForeignKey('webuser.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
        

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    webuser_id = db.Column(db.Integer, db.ForeignKey('webuser.id'))
    
    def __repr__(self):
        return '<Project %r>' % (self.body)