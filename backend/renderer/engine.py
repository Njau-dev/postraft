from PIL import Image, ImageDraw
from io import BytesIO
from renderer.layers.background_layer import BackgroundLayer
from renderer.layers.image_layer import ImageLayer
from renderer.layers.text_layer import TextLayer

class PosterRenderer:
    """Main poster rendering engine"""
    
    LAYER_CLASSES = {
        'background': BackgroundLayer,
        'image': ImageLayer,
        'text': TextLayer,
    }
    
    def __init__(self):
        pass
    
    def render(self, template_json: dict, data: dict) -> bytes:
        """
        Render a poster from template and data
        
        Args:
            template_json: Template JSON definition
            data: Data context (product, campaign, etc.)
            
        Returns:
            bytes: PNG image data
        """
        # Create canvas
        canvas_config = template_json.get('canvas', {})
        width = canvas_config.get('w', 1080)
        height = canvas_config.get('h', 1080)
        
        # Create image
        canvas = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(canvas)
        
        # Render each layer
        layers = template_json.get('layers', [])
        for layer_config in layers:
            layer_type = layer_config.get('type')
            
            if layer_type in self.LAYER_CLASSES:
                layer_class = self.LAYER_CLASSES[layer_type]
                layer = layer_class(layer_config)
                
                try:
                    layer.render(canvas, draw, data)
                except Exception as e:
                    print(f"Error rendering layer {layer_type}: {e}")
                    # Continue with other layers
        
        # Convert to bytes
        output = BytesIO()
        canvas.save(output, format='PNG', quality=95)
        output.seek(0)
        
        return output.getvalue()
    
    def render_to_file(self, template_json: dict, data: dict, output_path: str) -> None:
        """
        Render poster and save to file
        
        Args:
            template_json: Template JSON definition
            data: Data context
            output_path: Output file path
        """
        image_bytes = self.render(template_json, data)
        
        with open(output_path, 'wb') as f:
            f.write(image_bytes)
