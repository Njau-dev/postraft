from PIL import Image, ImageDraw
import requests
from io import BytesIO
from renderer.layers.base_layer import BaseLayer

class ImageLayer(BaseLayer):
    """Renders product images"""
    
    def render(self, canvas: Image.Image, draw: ImageDraw.Draw, data: dict) -> None:
        """Render image layer"""
        
        # Get image URL from data
        key = self.config.get('key', 'product.image')
        image_url = self.resolve_key(key, data)
        
        if not image_url:
            # Draw placeholder if no image
            self._draw_placeholder(draw)
            return
        
        try:
            # Download image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            product_image = Image.open(BytesIO(response.content))
            
            # Convert to RGB if needed
            if product_image.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', product_image.size, (255, 255, 255))
                if product_image.mode == 'P':
                    product_image = product_image.convert('RGBA')
                background.paste(product_image, mask=product_image.split()[-1] if product_image.mode == 'RGBA' else None)
                product_image = background
            
            # Get position and size
            x = self.config.get('x', 0)
            y = self.config.get('y', 0)
            w = self.config.get('w', 400)
            h = self.config.get('h', 400)
            
            # Resize image
            fit_mode = self.config.get('fit', 'cover')
            resized_image = self._resize_image(product_image, w, h, fit_mode)
            
            # Apply border radius if specified
            border_radius = self.config.get('border_radius', 0)
            if border_radius > 0:
                resized_image = self._apply_border_radius(resized_image, border_radius)
            
            # Paste image onto canvas
            canvas.paste(resized_image, (x, y))
            
            # Draw border if specified
            border = self.config.get('border')
            if border:
                border_width = border.get('width', 2)
                border_color = border.get('color', '#000000')
                draw.rectangle(
                    [(x, y), (x + w, y + h)],
                    outline=border_color,
                    width=border_width
                )
        
        except Exception as e:
            print(f"Error loading image: {e}")
            self._draw_placeholder(draw)
    
    def _resize_image(self, image: Image.Image, target_w: int, target_h: int, fit: str) -> Image.Image:
        """Resize image to fit target dimensions"""
        
        if fit == 'cover':
            # Calculate aspect ratios
            img_aspect = image.width / image.height
            target_aspect = target_w / target_h
            
            if img_aspect > target_aspect:
                # Image is wider - scale by height
                new_height = target_h
                new_width = int(target_h * img_aspect)
            else:
                # Image is taller - scale by width
                new_width = target_w
                new_height = int(target_w / img_aspect)
            
            # Resize
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop to exact size
            left = (new_width - target_w) // 2
            top = (new_height - target_h) // 2
            right = left + target_w
            bottom = top + target_h
            
            return resized.crop((left, top, right, bottom))
        
        else:  # contain
            image.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Create centered image on white background
            result = Image.new('RGB', (target_w, target_h), (255, 255, 255))
            offset_x = (target_w - image.width) // 2
            offset_y = (target_h - image.height) // 2
            result.paste(image, (offset_x, offset_y))
            
            return result
    
    def _apply_border_radius(self, image: Image.Image, radius: int) -> Image.Image:
        """Apply rounded corners to image"""
        # Create mask
        mask = Image.new('L', image.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            [(0, 0), image.size],
            radius=radius,
            fill=255
        )
        
        # Apply mask
        result = Image.new('RGB', image.size, (255, 255, 255))
        result.paste(image, mask=mask)
        
        return result
    
    def _draw_placeholder(self, draw: ImageDraw.Draw) -> None:
        """Draw placeholder when image is not available"""
        x = self.config.get('x', 0)
        y = self.config.get('y', 0)
        w = self.config.get('w', 400)
        h = self.config.get('h', 400)
        
        # Draw gray rectangle
        draw.rectangle(
            [(x, y), (x + w, y + h)],
            fill='#e5e7eb',
            outline='#9ca3af',
            width=2
        )
        
        # Draw X
        draw.line([(x, y), (x + w, y + h)], fill='#9ca3af', width=2)
        draw.line([(x + w, y), (x, y + h)], fill='#9ca3af', width=2)
