#!/usr/bin/env python3
"""
Quick test script for the Unified Ontology Platform

This script quickly starts the backend and tests the API endpoints
"""

import subprocess
import time
import requests
import sys
import threading
from pathlib import Path

def test_endpoints():
    """Test all platform endpoints"""
    print("🧪 Testing API endpoints...")
    
    # Wait a moment for server to fully start
    time.sleep(2)
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/",
        "/health", 
        "/api/books/",
        "/api/faculty/",
        "/api/students/", 
        "/api/classes/",
        "/api/ontology/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
            else:
                print(f"⚠️ {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")

def main():
    """Quick test function"""
    print("🚀 Quick Test - Unified Ontology Platform")
    print("=" * 50)
    
    backend_dir = Path(__file__).parent.parent / "backend"
    
    # Start the server
    print("📡 Starting test server...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000"
    ], 
    cwd=backend_dir,
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
    )
    
    # Test endpoints in a separate thread  
    test_thread = threading.Thread(target=test_endpoints)
    test_thread.daemon = True
    test_thread.start()
    
    # Wait for tests to complete
    test_thread.join()
    
    # Stop the server
    print("\n🛑 Stopping test server...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    
    print("✅ Quick test completed!")
    print("\n🎯 To start the full platform: python3 scripts/start.py")

if __name__ == "__main__":
    main()