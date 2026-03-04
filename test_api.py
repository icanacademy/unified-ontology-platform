#!/usr/bin/env python3
"""
Quick API test to verify all endpoints are working
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:9000"
    
    print("🧪 Testing Unified Ontology Platform API")
    print("=" * 50)
    
    endpoints = [
        ("/", "Main endpoint"),
        ("/health", "Health check"), 
        ("/api/books/", "Books platform"),
        ("/api/faculty/", "Faculty platform"),
        ("/api/students/", "Student platform"), 
        ("/api/classes/", "Classes platform"),
        ("/api/ontology/", "Ontology platform")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {description} ({endpoint})")
                if 'message' in data:
                    print(f"   📝 {data['message']}")
                if 'platforms' in data and isinstance(data['platforms'], dict):
                    print(f"   🔗 Available platforms: {len(data['platforms'])}")
                print()
            else:
                print(f"⚠️ {description} ({endpoint}) - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {description} ({endpoint}) - Error: {e}")
    
    print("🎯 Test completed!")
    print("🌐 Visit http://localhost:9000/api/docs for full API documentation")

if __name__ == "__main__":
    test_api()