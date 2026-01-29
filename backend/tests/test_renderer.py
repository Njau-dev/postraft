from renderer.engine import PosterRenderer
from app import create_app
from app.models import Template, Product, User

def test_renderer():
    """Test the rendering engine"""
    print("\n🎨 Testing Poster Renderer\n")
    
    app = create_app()
    
    with app.app_context():
        # Get a system template
        template = Template.query.filter_by(is_system=True).first()
        
        if not template:
            print("❌ No templates found. Run seed_templates.py first")
            return
        
        print(f"✅ Using template: {template.name}")
        
        # Create mock product data
        mock_product = {
            'name': 'Premium Rice 2kg',
            'price': 450.00,
            'image': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=800',
            'category': 'Groceries'
        }
        
        # Prepare data context
        data = {
            'product': mock_product
        }
        
        # Render
        print("🎨 Rendering poster...")
        renderer = PosterRenderer()
        
        try:
            image_bytes = renderer.render(template.json_definition, data)
            
            # Save to file
            output_path = 'test_poster.png'
            with open(output_path, 'wb') as f:
                f.write(image_bytes)
            
            print(f"✅ Poster rendered successfully!")
            print(f"📁 Saved to: {output_path}")
            print(f"📏 Size: {len(image_bytes)} bytes")
            
        except Exception as e:
            print(f"❌ Rendering failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_renderer()
