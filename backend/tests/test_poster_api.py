import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'

def get_auth_token():
    """Login and get token"""
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'demo@postcraft.com',
        'password': 'SecurePass123'
    })
    return response.json()['data']['token']

def test_poster_api():
    print("\n🧪 Testing Poster Generation API\n")
    
    # Get token
    token = get_auth_token()
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test 1: Get stats
    print("1️⃣ Fetching generation stats...")
    response = requests.get(f'{BASE_URL}/posters/stats', headers=headers)
    print(f"   Status: {response.status_code}")
    stats = response.json()['data']
    print(f"   Usage: {stats['used']}/{stats['limit']}")
    print(f"   Total posters: {stats['total_posters']}")
    
    # Test 2: Get template and product
    print("\n2️⃣ Getting template and product...")
    templates_response = requests.get(f'{BASE_URL}/templates', headers=headers)
    templates = templates_response.json()['data']['templates']
    
    products_response = requests.get(f'{BASE_URL}/products', headers=headers)
    products = products_response.json()['data']['products']
    
    if not templates or not products:
        print("   ❌ Need at least 1 template and 1 product")
        return
    
    template_id = templates[0]['id']
    product_id = products[0]['id']
    
    print(f"   Template: {templates[0]['name']}")
    print(f"   Product: {products[0]['name']}")
    
    # Test 3: Generate poster
    print("\n3️⃣ Generating poster...")
    gen_data = {
        'template_id': template_id,
        'product_ids': [product_id]
    }
    response = requests.post(f'{BASE_URL}/posters/generate', json=gen_data, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()['data']
        job_id = result['job_id']
        print(f"   ✅ Job queued: {job_id}")
        
        # Test 4: Poll job status
        print("\n4️⃣ Polling job status...")
        for i in range(60):  # Wait up to 60 seconds
            time.sleep(1)
            status_response = requests.get(f'{BASE_URL}/posters/job/{job_id}', headers=headers)
            status = status_response.json()['data']['status']
            print(f"   Status: {status}       ", end='\r')
            
            if status in ['completed', 'failed']:
                break
        
        print()  # New line
        
        final_status_response = requests.get(f'{BASE_URL}/posters/job/{job_id}', headers=headers)
        final_status = final_status_response.json()['data']
        
        if final_status['status'] == 'completed':
            print(f"   ✅ Generation completed!")
            if 'result' in final_status:
                print(f"   Image URL: {final_status['result'].get('image_url', 'N/A')}")
        else:
            print(f"   ❌ Generation failed or timed out")
    
    # Test 5: Get all posters
    print("\n5️⃣ Fetching all posters...")
    response = requests.get(f'{BASE_URL}/posters', headers=headers)
    posters_data = response.json()['data']
    print(f"   Status: {response.status_code}")
    print(f"   ✅ Found {posters_data['total']} posters")
    
    if posters_data['posters']:
        poster = posters_data['posters'][0]
        print(f"   Latest: {poster.get('image_url', 'No URL')}")
        
        # Test 6: Get single poster
        print("\n6️⃣ Fetching single poster...")
        poster_id = poster['id']
        response = requests.get(f'{BASE_URL}/posters/{poster_id}', headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   ✅ Poster {poster_id} retrieved")
        
        # Test 7: Download posters
        print("\n7️⃣ Downloading posters as ZIP...")
        download_data = {'poster_ids': [poster_id]}
        response = requests.post(f'{BASE_URL}/posters/download', json=download_data, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            with open('posters_download.zip', 'wb') as f:
                f.write(response.content)
            print(f"   ✅ ZIP downloaded: posters_download.zip ({len(response.content)} bytes)")
    
    # Test 8: Batch generation
    if len(products) >= 2:
        print("\n8️⃣ Testing batch generation...")
        batch_data = {
            'template_id': template_id,
            'product_ids': [p['id'] for p in products[:2]]
        }
        response = requests.post(f'{BASE_URL}/posters/generate', json=batch_data, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()['data']
            print(f"   ✅ Batch job queued: {result['total']} posters")
    
    print("\n✅ Poster API tests complete!\n")

if __name__ == '__main__':
    test_poster_api()
