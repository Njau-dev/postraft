from app import create_app
from app.extensions import db
from app.models import Template

def seed_system_templates():
    """Seed system templates"""
    app = create_app()
    
    with app.app_context():
        # Check if templates already exist
        if Template.query.filter_by(is_system=True).count() > 0:
            print("System templates already exist. Skipping seed.")
            return
        
        templates = [
            # Template 1: Modern Square Instagram Post
            Template(
                user_id=None,
                name='Modern Square',
                format='square',
                is_system=True,
                json_definition={
                    'canvas': {'w': 1080, 'h': 1080},
                    'layers': [
                        {
                            'type': 'background',
                            'color': '#ffffff'
                        },
                        {
                            'type': 'image',
                            'key': 'product.image',
                            'x': 100,
                            'y': 200,
                            'w': 400,
                            'h': 400,
                            'fit': 'cover'
                        },
                        {
                            'type': 'text',
                            'key': 'product.name',
                            'x': 550,
                            'y': 300,
                            'max_width': 450,
                            'font': 'bold',
                            'size': 64,
                            'color': '#000000',
                            'align': 'left'
                        },
                        {
                            'type': 'text',
                            'key': 'product.price',
                            'x': 550,
                            'y': 420,
                            'font': 'bold',
                            'size': 72,
                            'color': '#ef4444',
                            'prefix': 'KSh '
                        },
                        {
                            'type': 'text',
                            'value': 'LIMITED OFFER',
                            'x': 100,
                            'y': 100,
                            'font': 'bold',
                            'size': 36,
                            'color': '#ef4444'
                        }
                    ]
                },
                preview_url='https://placehold.co/1080x1080/e0e7ff/4f46e5?text=Modern+Square'
            ),
            
            # Template 2: Story Format (Vertical)
            Template(
                user_id=None,
                name='Story Promo',
                format='story',
                is_system=True,
                json_definition={
                    'canvas': {'w': 1080, 'h': 1920},
                    'layers': [
                        {
                            'type': 'background',
                            'color': '#1e293b'
                        },
                        {
                            'type': 'image',
                            'key': 'product.image',
                            'x': 190,
                            'y': 400,
                            'w': 700,
                            'h': 700,
                            'fit': 'cover'
                        },
                        {
                            'type': 'text',
                            'key': 'product.name',
                            'x': 540,
                            'y': 1200,
                            'max_width': 800,
                            'font': 'bold',
                            'size': 80,
                            'color': '#ffffff',
                            'align': 'center'
                        },
                        {
                            'type': 'text',
                            'key': 'product.price',
                            'x': 540,
                            'y': 1400,
                            'font': 'bold',
                            'size': 96,
                            'color': '#22c55e',
                            'prefix': 'KSh ',
                            'align': 'center'
                        },
                        {
                            'type': 'text',
                            'value': 'SPECIAL PRICE',
                            'x': 540,
                            'y': 250,
                            'font': 'bold',
                            'size': 48,
                            'color': '#fbbf24',
                            'align': 'center'
                        }
                    ]
                },
                preview_url='https://placehold.co/1080x1920/1e293b/22c55e?text=Story+Promo'
            ),
            
            # Template 3: Minimalist A4 Print
            Template(
                user_id=None,
                name='Print Poster',
                format='a4',
                is_system=True,
                json_definition={
                    'canvas': {'w': 2480, 'h': 3508},  # A4 at 300 DPI
                    'layers': [
                        {
                            'type': 'background',
                            'color': '#fafafa'
                        },
                        {
                            'type': 'image',
                            'key': 'product.image',
                            'x': 490,
                            'y': 600,
                            'w': 1500,
                            'h': 1500,
                            'fit': 'cover'
                        },
                        {
                            'type': 'text',
                            'key': 'product.name',
                            'x': 1240,
                            'y': 2300,
                            'max_width': 2000,
                            'font': 'bold',
                            'size': 120,
                            'color': '#0f172a',
                            'align': 'center'
                        },
                        {
                            'type': 'text',
                            'key': 'product.price',
                            'x': 1240,
                            'y': 2550,
                            'font': 'bold',
                            'size': 180,
                            'color': '#dc2626',
                            'prefix': 'KSh ',
                            'align': 'center'
                        },
                        {
                            'type': 'text',
                            'value': 'AVAILABLE NOW',
                            'x': 1240,
                            'y': 350,
                            'font': 'bold',
                            'size': 72,
                            'color': '#475569',
                            'align': 'center'
                        }
                    ]
                },
                preview_url='https://placehold.co/2480x3508/fafafa/dc2626?text=Print+Poster'
            ),
            
            # Template 4: Vibrant Grid
            Template(
                user_id=None,
                name='Vibrant Grid',
                format='square',
                is_system=True,
                json_definition={
                    'canvas': {'w': 1080, 'h': 1080},
                    'layers': [
                        {
                            'type': 'background',
                            'gradient': {
                                'type': 'linear',
                                'colors': ['#ec4899', '#8b5cf6'],
                                'angle': 135
                            }
                        },
                        {
                            'type': 'image',
                            'key': 'product.image',
                            'x': 540,
                            'y': 540,
                            'w': 600,
                            'h': 600,
                            'fit': 'cover',
                            'border_radius': 30
                        },
                        {
                            'type': 'text',
                            'key': 'product.name',
                            'x': 540,
                            'y': 150,
                            'max_width': 900,
                            'font': 'bold',
                            'size': 72,
                            'color': '#ffffff',
                            'align': 'center',
                            'shadow': True
                        },
                        {
                            'type': 'text',
                            'key': 'product.price',
                            'x': 540,
                            'y': 920,
                            'font': 'bold',
                            'size': 96,
                            'color': '#ffffff',
                            'prefix': 'KSh ',
                            'align': 'center',
                            'shadow': True
                        }
                    ]
                },
                preview_url='https://placehold.co/1080x1080/ec4899/ffffff?text=Vibrant+Grid'
            ),
            
            # Template 5: Classic Sale
            Template(
                user_id=None,
                name='Classic Sale',
                format='square',
                is_system=True,
                json_definition={
                    'canvas': {'w': 1080, 'h': 1080},
                    'layers': [
                        {
                            'type': 'background',
                            'color': '#fef3c7'
                        },
                        {
                            'type': 'image',
                            'key': 'product.image',
                            'x': 90,
                            'y': 90,
                            'w': 900,
                            'h': 600,
                            'fit': 'cover',
                            'border': {'width': 8, 'color': '#78350f'}
                        },
                        {
                            'type': 'text',
                            'key': 'product.name',
                            'x': 540,
                            'y': 780,
                            'max_width': 900,
                            'font': 'bold',
                            'size': 64,
                            'color': '#78350f',
                            'align': 'center'
                        },
                        {
                            'type': 'text',
                            'key': 'product.price',
                            'x': 540,
                            'y': 900,
                            'font': 'bold',
                            'size': 96,
                            'color': '#dc2626',
                            'prefix': 'KSh ',
                            'align': 'center'
                        },
                        {
                            'type': 'text',
                            'value': 'SALE',
                            'x': 900,
                            'y': 180,
                            'font': 'bold',
                            'size': 120,
                            'color': '#dc2626',
                            'rotation': -15
                        }
                    ]
                },
                preview_url='https://placehold.co/1080x1080/fef3c7/dc2626?text=Classic+Sale'
            ),
        ]
        
        for template in templates:
            db.session.add(template)
        
        db.session.commit()
        print(f"✅ Created {len(templates)} system templates")
        
        # Display templates
        for template in Template.query.filter_by(is_system=True).all():
            print(f"  - {template.name} ({template.format})")

if __name__ == '__main__':
    seed_system_templates()
