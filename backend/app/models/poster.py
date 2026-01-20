from app.extensions import db
from datetime import datetime

class Poster(db.Model):
    __tablename__ = 'posters'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=True)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    
    # Generated poster
    image_url = db.Column(db.String(500), nullable=False)
    
    # Metadata
    format = db.Column(db.String(50))  # 'square', 'story', 'a4'
    status = db.Column(db.String(20), default='generated')  # 'generating', 'generated', 'failed'
    
    # Job tracking
    job_id = db.Column(db.String(100), unique=True)
    error_message = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'campaign_id': self.campaign_id,
            'template_id': self.template_id,
            'image_url': self.image_url,
            'format': self.format,
            'status': self.status,
            'job_id': self.job_id,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<Poster {self.id}>'
