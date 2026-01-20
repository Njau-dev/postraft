from app.extensions import db
from datetime import datetime

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Campaign details
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Template association
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    
    # Campaign rules (JSON)
    rules = db.Column(db.JSON, default=dict)
    # Example: {"discount": 20, "banner_text": "EASTER SALE", "category": "groceries"}
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posters = db.relationship('Poster', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'template_id': self.template_id,
            'rules': self.rules or {},
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<Campaign {self.name}>'
