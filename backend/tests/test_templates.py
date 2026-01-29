import requests
import json

BASE_URL = 'http://localhost:5000/api'

def get_auth_token():
    """Login and get token"""
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'demo@postcraft.com',
        'password': 'SecurePass123'
    })
    return response.json()['data']['token']

def test_templates():
    print("\n🧪 Testing Template API\n")
    
    # Get token
    token = get_auth_token()
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test 1: Get all templates
    print("1️⃣ Fetching all templates...")
    response = requests.get(f'{BASE_URL}/templates', headers=headers)
    print(f"   Status: {response.status_code}")
    data = response.json()['data']
    print(f"   ✅ Found {len(data['templates'])} templates")
    
    # Display templates
    for template in data['templates']:
        system_tag = " [SYSTEM]" if template['is_system'] else ""
        print(f"      - {template['name']} ({template['format']}){system_tag}")
    
    # Test 2: Get templates by format
    print("\n2️⃣ Fetching square templates...")
    response = requests.get(f'{BASE_URL}/templates?format=square', headers=headers)
    data = response.json()['data']
    print(f"   ✅ Found {len(data['templates'])} square templates")
    
    # Test 3: Get single template
    if data['templates']:
        template_id = data['templates'][0]['id']
        print(f"\n3️⃣ Fetching template {template_id}...")
        response = requests.get(f'{BASE_URL}/templates/{template_id}', headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   ✅ Template fetched")
        
        # Test 4: Duplicate template
        print(f"\n4️⃣ Duplicating template {template_id}...")
        response = requests.post(f'{BASE_URL}/templates/{template_id}/duplicate', headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            dup_template = response.json()['data']
            print(f"   ✅ Created duplicate: {dup_template['name']}")
            
            # Test 5: Delete duplicate
            print(f"\n5️⃣ Deleting duplicate...")
            response = requests.delete(f'{BASE_URL}/templates/{dup_template["id"]}', headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   ✅ Template deleted")
    
    # Test 6: Create custom template
    print("\n6️⃣ Creating custom template...")
    custom_template = {
        'name': 'My Custom Template',
        'format': 'square',
        'json_definition': {
            'canvas': {'w': 1080, 'h': 1080},
            'layers': [
                {'type': 'background', 'color': '#ffffff'},
                {'type': 'text', 'key': 'product.name', 'x': 100, 'y': 100, 'size': 64}
            ]
        }
    }
    response = requests.post(f'{BASE_URL}/templates', json=custom_template, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✅ Custom template created")
    
    print("\n✅ Template API tests complete!\n")

if __name__ == '__main__':
    test_templates()
