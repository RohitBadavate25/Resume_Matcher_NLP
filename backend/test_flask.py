#!/usr/bin/env python3

import requests
import time
import sys

def test_flask_server():
    """Test Flask server endpoints"""
    base_url = "http://127.0.0.1:5000"
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test root endpoint
        print("Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print("❌ Root endpoint failed")
            
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health")
        print(f"Health endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"Response: {response.json()}")
        else:
            print("❌ Health endpoint failed")
            
        # Test resumes endpoint
        print("Testing resumes endpoint...")
        response = requests.get(f"{base_url}/api/resumes")
        print(f"Resumes endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Resumes endpoint working")
            data = response.json()
            print(f"Found {len(data.get('resumes', []))} resumes")
        else:
            print("❌ Resumes endpoint failed")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server")
        print("Make sure the server is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Error testing server: {str(e)}")

if __name__ == "__main__":
    test_flask_server()