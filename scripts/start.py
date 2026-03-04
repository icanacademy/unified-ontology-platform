#!/usr/bin/env python3
"""
Unified Ontology Platform Startup Script

This script starts the unified platform that combines all educational analytics platforms:
- Books & Library Management
- Faculty Analytics
- Student Analytics  
- Class Management
- Ontology Platform

All platforms are accessible through a single unified API at http://localhost:8000
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    Unified Ontology Platform                     ║
    ║                                                                  ║
    ║  🎓 Integrated Educational Analytics Platform                    ║
    ║                                                                  ║
    ║  Platforms included:                                             ║
    ║  📚 Books & Library Management                                   ║
    ║  👨‍🏫 Faculty Analytics                                           ║
    ║  🎓 Student Analytics                                            ║
    ║  📋 Class Management                                             ║
    ║  🧠 Ontology Platform                                            ║
    ║                                                                  ║
    ║  🚀 Starting on: http://localhost:9000                          ║
    ║  📖 API Docs: http://localhost:9000/api/docs                    ║
    ║  🎯 Frontend: http://localhost:3000                             ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if required dependencies are installed"""
    print("🔍 Checking requirements...")
    
    backend_dir = Path(__file__).parent.parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Requirements file not found")
        return False
        
    try:
        # Check if uvicorn is available
        result = subprocess.run([sys.executable, "-c", "import uvicorn"], 
                               capture_output=True, text=True)
        if result.returncode != 0:
            print("📦 Installing backend dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                          check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install backend dependencies")
        return False
        
    print("✅ Backend dependencies ready")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting unified backend server...")
    
    backend_dir = Path(__file__).parent.parent / "backend"
    os.chdir(backend_dir)
    
    try:
        # Start the unified FastAPI server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "9000", 
            "--reload"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend development server"""
    print("🎨 Starting unified frontend...")
    
    frontend_dir = Path(__file__).parent.parent / "frontend"
    
    if not (frontend_dir / "package.json").exists():
        print("⚠️  Frontend package.json not found, skipping frontend start")
        return None
    
    try:
        os.chdir(frontend_dir)
        
        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start React development server
        process = subprocess.Popen([
            "npm", "start"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        return process
    except subprocess.CalledProcessError:
        print("❌ Failed to start frontend (npm not available)")
        return None
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def monitor_processes(backend_process, frontend_process):
    """Monitor backend and frontend processes"""
    print("📊 Monitoring unified platform...")
    print("🔗 Backend API: http://localhost:9000")
    print("📖 API Documentation: http://localhost:9000/api/docs")
    if frontend_process:
        print("🎨 Frontend: http://localhost:3000")
    
    print("\n🌟 Platform Overview:")
    print("   📚 Books & Library: http://localhost:9000/api/books")  
    print("   👨‍🏫 Faculty Analytics: http://localhost:9000/api/faculty")
    print("   🎓 Student Analytics: http://localhost:9000/api/students")
    print("   📋 Class Management: http://localhost:9000/api/classes")
    print("   🧠 Ontology Platform: http://localhost:9000/api/ontology")
    
    print("\n⌨️  Press Ctrl+C to stop all services")
    print("🔍 Testing backend connection...")
    
    # Test backend connection
    for i in range(5):
        try:
            import requests
            response = requests.get("http://localhost:9000/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is responding correctly!")
                break
        except Exception:
            print(f"⏳ Waiting for backend... ({i+1}/5)")
            time.sleep(2)
    else:
        print("⚠️  Backend may not be responding, but processes are running")
    
    try:
        # Monitor processes with better error handling
        consecutive_failures = 0
        while True:
            backend_running = backend_process.poll() is None
            frontend_running = frontend_process.poll() is None if frontend_process else True
            
            if not backend_running:
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print("❌ Backend process stopped unexpectedly")
                    break
                else:
                    print(f"⚠️  Backend check failed ({consecutive_failures}/3)")
            else:
                consecutive_failures = 0
                
            if frontend_process and not frontend_running:
                print("⚠️  Frontend process stopped")
                
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down unified platform...")
        
        if backend_process:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                backend_process.kill()
                
        if frontend_process:
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
                
        print("✅ Unified platform stopped successfully")

def main():
    """Main startup function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        sys.exit(1)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend")
        sys.exit(1)
    
    # Wait a moment for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Monitor both processes
    monitor_processes(backend_process, frontend_process)

if __name__ == "__main__":
    main()