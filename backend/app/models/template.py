from app.extensions import db
from datetime import datetime

class Template(db.Model):
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    # NULL user_id = system template
    
    # Template details
    name = db.Column(db.String(200), nullable=False)
    format = db.Column(db.String(50), nullable=False)  # 'square', 'story', 'a4'
    
    # Template data
    background_url = db.Column(db.String(500))
    json_definition = db.Column(db.JSON, nullable=False)
    preview_url = db.Column(db.String(500))
    
    # Flags
    is_system = db.Column(db.Boolean, default=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaigns = db.relationship('Campaign', backref='template', lazy='dynamic')
    posters = db.relationship('Poster', backref='template', lazy='dynamic')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'format': self.format,
            'background_url': self.background_url,
            'json_definition': self.json_definition,
            'preview_url': self.preview_url,
            'is_system': self.is_system,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<Template {self.name}>'
