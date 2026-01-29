from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

class BaseLayer(ABC):
    """Base class for all layer types"""
    
    def __init__(self, layer_config: dict):
        self.config = layer_config
    
    @abstractmethod
    def render(self, canvas: Image.Image, draw: ImageDraw.Draw, data: dict) -> None:
        """
        Render this layer onto the canvas
        
        Args:
            canvas: PIL Image object
            draw: PIL ImageDraw object
            data: Data context (product, campaign, etc.)
        """
        pass
    
    def resolve_key(self, key: str, data: dict):
        """
        Resolve data key like 'product.name' to actual value
        
        Args:
            key: Dot-notation key (e.g., 'product.price')
            data: Data dictionary
            
        Returns:
            Resolved value or None
        """
        parts = key.split('.')
        value = data
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                return None
        
        return value
