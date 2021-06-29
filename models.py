from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    department = db.Column(db.String(20), nullable=False)
    manager = db.Column(db.String(20), nullable=False)
    job_title = db.Column(db.String(20), nullable=False)
    supervisor = db.Column(db.String(20), nullable=False)
    high_risk = db.Column(db.String(20), nullable=False)
    health = db.Column(db.String(20), nullable=False)
    h_comment = db.Column(db.String(60),nullable=False)
    employment = db.Column(db.String(20), nullable=False)
    e_comment = db.Column(db.String(60),nullable=False)  
    date_updated = db.Column(db.String(60),nullable=False, default=datetime.utcnow)  
    
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}','{self.password}','{self.department}','{self.manager}','{self.job_title}','{self.supervisor}','{self.high_risk}','{self.health}','{self.h_comment}','{self.employment}','{self.e_comment}')"

