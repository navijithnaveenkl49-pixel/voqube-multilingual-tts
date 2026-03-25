import requests
import json

def test_backend_long_text():
    url = "http://localhost:8000/api/auth/login"
    data = {"username": "admin", "password": "admin123"}
    
    # Login to get token
    # Since OAuth2PasswordRequestForm expects form data
    response = requests.post(url, data=data)
    token = response.json()["access_token"]
    
    # Test generation
    gen_url = "http://localhost:8000/api/tts/generate"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Create ~6000 character text
    long_text = "The quick brown fox jumps over the lazy dog. " * 150 
    print(f"Testing with {len(long_text)} characters...")
    
    payload = {
        "text": long_text,
        "language": "Malayalam",
        "voice_type": "Female",
        "auto_translate": True
    }
    
    response = requests.post(gen_url, headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_backend_long_text()
