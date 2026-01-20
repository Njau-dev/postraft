from app import create_app
from app.extensions import db
from app.models import Plan

def seed_plans():
    """Seed default subscription plans"""
    app = create_app()
    
    with app.app_context():
        # Check if plans already exist
        if Plan.query.count() > 0:
            print("Plans already exist. Skipping seed.")
            return
        
        plans = [
            Plan(
                name='Free',
                price=0,
                max_products=10,
                max_templates=3,
                monthly_generations=50,
                description='Perfect for trying out PostCraft',
                features={
                    'branding_removal': False,
                    'batch_export': False,
                    'auto_post': False,
                    'priority_support': False,
                }
            ),
            Plan(
                name='Starter',
                price=1500,  # KES per month
                max_products=100,
                max_templates=10,
                monthly_generations=500,
                description='Great for small businesses',
                features={
                    'branding_removal': True,
                    'batch_export': True,
                    'auto_post': False,
                    'priority_support': False,
                }
            ),
            Plan(
                name='Pro',
                price=4500,  # KES per month
                max_products=1000,
                max_templates=50,
                monthly_generations=5000,
                description='For growing businesses',
                features={
                    'branding_removal': True,
                    'batch_export': True,
                    'auto_post': True,
                    'priority_support': True,
                }
            ),
            Plan(
                name='Agency',
                price=9500,  # KES per month
                max_products=-1,  # Unlimited
                max_templates=-1,  # Unlimited
                monthly_generations=-1,  # Unlimited
                description='For agencies and enterprises',
                features={
                    'branding_removal': True,
                    'batch_export': True,
                    'auto_post': True,
                    'priority_support': True,
                    'white_label': True,
                    'api_access': True,
                }
            ),
        ]
        
        for plan in plans:
            db.session.add(plan)
        
        db.session.commit()
        print(f"✅ Created {len(plans)} subscription plans")
        
        # Display plans
        for plan in Plan.query.all():
            print(f"  - {plan.name}: KES {plan.price}/month")

if __name__ == '__main__':
    seed_plans()
