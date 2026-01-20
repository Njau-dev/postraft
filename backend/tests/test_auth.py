import requests
import json

BASE_URL = 'http://localhost:5000/api/auth'

def test_auth():
    print("\n🧪 Testing Authentication API\n")
    
    # Test 1: Register
    print("1️⃣ Testing Registration...")
    register_data = {
        'email': 'demo@postcraft.com',
        'password': 'SecurePass123'
    }
    
    response = requests.post(f'{BASE_URL}/register', json=register_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        token = response.json()['data']['token']
        print(f"   ✅ Token: {token[:50]}...")
    
    # Test 2: Login
    print("\n2️⃣ Testing Login...")
    login_data = {
        'email': 'demo@postcraft.com',
        'password': 'SecurePass123'
    }
    
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json()['data']['token']
        print(f"   ✅ Login successful, token received")
        
        # Test 3: Get current user
        print("\n3️⃣ Testing Get Current User...")
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{BASE_URL}/me', headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Invalid credentials
    print("\n4️⃣ Testing Invalid Login...")
    bad_login = {
        'email': 'demo@postcraft.com',
        'password': 'WrongPassword'
    }
    response = requests.post(f'{BASE_URL}/login', json=bad_login)
    print(f"   Status: {response.status_code}")
    print(f"   Error: {response.json().get('error')}")
    
    print("\n✅ Auth tests complete!\n")

if __name__ == '__main__':
    test_auth()
