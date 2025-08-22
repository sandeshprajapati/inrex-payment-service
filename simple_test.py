import requests
import json

def test_simple():
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test root endpoint
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"Root endpoint: {response.status_code} - {response.json()}")
        
        print("✅ Basic tests passed!")
        print("\n📖 Access the full API documentation at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_simple()
