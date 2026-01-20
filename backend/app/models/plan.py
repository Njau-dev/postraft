from app.extensions import db

class Plan(db.Model):
    __tablename__ = 'plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, default=0.0)
    
    # Limits
    max_products = db.Column(db.Integer, default=10)
    max_templates = db.Column(db.Integer, default=3)
    monthly_generations = db.Column(db.Integer, default=50)
    
    # Features (JSON)
    features = db.Column(db.JSON, default=dict)
    # Example: {"branding_removal": False, "batch_export": False, "auto_post": False}
    
    # Metadata
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'max_products': self.max_products,
            'max_templates': self.max_templates,
            'monthly_generations': self.monthly_generations,
            'features': self.features or {},
            'description': self.description,
        }
    
    def __repr__(self):
        return f'<Plan {self.name}>'
