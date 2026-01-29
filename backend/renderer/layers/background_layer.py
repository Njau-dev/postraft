from PIL import Image, ImageDraw
from renderer.layers.base_layer import BaseLayer

class BackgroundLayer(BaseLayer):
    """Renders background (solid color or gradient)"""
    
    def render(self, canvas: Image.Image, draw: ImageDraw.Draw, data: dict) -> None:
        """Render background"""
        
        # Solid color background
        if 'color' in self.config:
            color = self.config['color']
            draw.rectangle([(0, 0), canvas.size], fill=color)
        
        # Gradient background (simplified - linear only)
        elif 'gradient' in self.config:
            gradient = self.config['gradient']
            self._render_gradient(canvas, draw, gradient)
    
    def _render_gradient(self, canvas: Image.Image, draw: ImageDraw.Draw, gradient: dict) -> None:
        """Render gradient background"""
        width, height = canvas.size
        colors = gradient.get('colors', ['#ffffff', '#000000'])
        
        # Parse colors
        start_color = self._parse_color(colors[0])
        end_color = self._parse_color(colors[1])
        
        # Create vertical gradient (simplified)
        for y in range(height):
            # Calculate interpolation factor
            factor = y / height
            
            # Interpolate RGB
            r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
            
            # Draw horizontal line
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    def _parse_color(self, color_hex: str) -> tuple:
        """Parse hex color to RGB tuple"""
        color_hex = color_hex.lstrip('#')
        return tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
