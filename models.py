from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with conversions
    conversions = db.relationship('Conversion', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Conversion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pdf_filename = db.Column(db.String(255), nullable=False)
    xml_filename = db.Column(db.String(255), nullable=False)
    conversion_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_size = db.Column(db.Integer, nullable=True)  # Size in bytes
    status = db.Column(db.String(50), default='completed')
    # Store the XML content as text to allow viewing/downloading
    xml_content = db.Column(db.Text, nullable=True)
    
    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Conversion {self.pdf_filename} to {self.xml_filename}>'
