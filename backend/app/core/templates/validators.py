from typing import Dict, Any, List, Tuple

class TemplateValidator:
    """Validates template data"""
    
    VALID_FORMATS = ['square', 'story', 'a4']
    VALID_LAYER_TYPES = ['background', 'image', 'text', 'shape']
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate template creation data
        
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []
        
        # Name validation
        if not data.get('name'):
            errors.append('Template name is required')
        elif len(data['name'].strip()) < 2:
            errors.append('Template name must be at least 2 characters')
        
        # Format validation
        if not data.get('format'):
            errors.append('Template format is required')
        elif data['format'] not in TemplateValidator.VALID_FORMATS:
            errors.append(f'Format must be one of: {", ".join(TemplateValidator.VALID_FORMATS)}')
        
        # JSON definition validation
        if not data.get('json_definition'):
            errors.append('Template definition is required')
        else:
            json_errors = TemplateValidator._validate_json_definition(data['json_definition'])
            errors.extend(json_errors)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _validate_json_definition(json_def: Any) -> List[str]:
        """Validate template JSON structure"""
        errors = []
        
        if not isinstance(json_def, dict):
            errors.append('Template definition must be an object')
            return errors
        
        # Canvas validation
        if 'canvas' not in json_def:
            errors.append('Template must have a canvas definition')
        else:
            canvas = json_def['canvas']
            if not isinstance(canvas, dict):
                errors.append('Canvas must be an object')
            elif 'w' not in canvas or 'h' not in canvas:
                errors.append('Canvas must have width (w) and height (h)')
        
        # Layers validation
        if 'layers' not in json_def:
            errors.append('Template must have layers')
        else:
            layers = json_def['layers']
            if not isinstance(layers, list):
                errors.append('Layers must be an array')
            elif len(layers) == 0:
                errors.append('Template must have at least one layer')
            else:
                for idx, layer in enumerate(layers):
                    if not isinstance(layer, dict):
                        errors.append(f'Layer {idx} must be an object')
                        continue
                    
                    if 'type' not in layer:
                        errors.append(f'Layer {idx} must have a type')
                    elif layer['type'] not in TemplateValidator.VALID_LAYER_TYPES:
                        errors.append(f'Layer {idx} has invalid type: {layer["type"]}')
        
        return errors
