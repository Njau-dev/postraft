from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), default=1)

    # Usage tracking
    monthly_generations = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.DateTime, default=datetime.utcnow)
    password_changed_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plan = db.relationship('Plan', backref='users')
    products = db.relationship(
        'Product', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    templates = db.relationship(
        'Template', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    campaigns = db.relationship(
        'Campaign', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    posters = db.relationship(
        'Poster', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
        self.password_changed_at = datetime.utcnow()

    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def reset_password(self, new_password):
        self.set_password(new_password)
        self.last_password_reset = datetime.utcnow()

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_name': self.user_name,
            'email': self.email,
            'plan_id': self.plan_id,
            'monthly_generations': self.monthly_generations,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f'<User {self.email}>'
