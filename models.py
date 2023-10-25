from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Instagram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.Text, nullable=False)
    anti_pro = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False)

