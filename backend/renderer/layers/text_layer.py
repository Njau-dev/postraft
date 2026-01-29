from PIL import Image, ImageDraw, ImageFont
import os
from renderer.layers.base_layer import BaseLayer

class TextLayer(BaseLayer):
    """Renders text"""
    
    # Default font paths (you'll need to add font files)
    FONT_PATHS = {
        'bold': 'renderer/fonts/bold.ttf',
        'regular': 'renderer/fonts/regular.ttf',
    }
    
    def render(self, canvas: Image.Image, draw: ImageDraw.Draw, data: dict) -> None:
        """Render text layer"""
        
        # Get text value
        if 'value' in self.config:
            # Static text
            text = self.config['value']
        elif 'key' in self.config:
            # Dynamic text from data
            text = self.resolve_key(self.config['key'], data)
            if text is None:
                return
            
            # Add prefix if specified
            prefix = self.config.get('prefix', '')
            text = f"{prefix}{text}"
        else:
            return
        
        # Convert to string
        text = str(text)
        
        # Get position
        x = self.config.get('x', 0)
        y = self.config.get('y', 0)
        
        # Get font
        font_name = self.config.get('font', 'regular')
        font_size = self.config.get('size', 48)
        font = self._get_font(font_name, font_size)
        
        # Get color
        color = self.config.get('color', '#000000')
        
        # Get alignment
        align = self.config.get('align', 'left')
        
        # Handle text wrapping if max_width specified
        max_width = self.config.get('max_width')
        if max_width:
            text = self._wrap_text(text, font, max_width, draw)
        
        # Adjust position based on alignment
        if align == 'center':
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = x - (text_width // 2)
        elif align == 'right':
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = x - text_width
        
        # Draw shadow if specified
        if self.config.get('shadow'):
            shadow_offset = 3
            draw.text(
                (x + shadow_offset, y + shadow_offset),
                text,
                font=font,
                fill='#00000080'  # Semi-transparent black
            )
        
        # Draw text
        draw.text((x, y), text, font=font, fill=color)
    
    def _get_font(self, font_name: str, size: int) -> ImageFont.FreeTypeFont:
        """Load font or return default"""
        font_path = self.FONT_PATHS.get(font_name)
        
        if font_path and os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception as e:
                print(f"Error loading font {font_path}: {e}")
        
        # Return default font
        try:
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> str:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
