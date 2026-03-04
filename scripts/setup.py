#!/usr/bin/env python3
"""
Unified Ontology Platform Setup Script

This script sets up the unified platform by:
1. Installing backend dependencies
2. Installing frontend dependencies  
3. Setting up databases
4. Verifying the installation
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                Unified Ontology Platform Setup                  ║
    ║                                                                  ║
    ║  Setting up integrated educational analytics platform...        ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def setup_backend():
    """Setup backend dependencies"""
    print("🔧 Setting up backend...")
    
    backend_dir = Path(__file__).parent.parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Requirements file not found")
        return False
        
    try:
        print("📦 Installing backend dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        return False

def setup_frontend():
    """Setup frontend dependencies"""
    print("🎨 Setting up frontend...")
    
    frontend_dir = Path(__file__).parent.parent / "frontend"
    package_json = frontend_dir / "package.json"
    
    if not package_json.exists():
        print("⚠️  Frontend package.json not found, skipping frontend setup")
        return True
        
    try:
        os.chdir(frontend_dir)
        
        # Check if npm is available
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        
        print("📦 Installing frontend dependencies...")
        subprocess.run(["npm", "install"], check=True)
        
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  npm not available, skipping frontend setup")
        return True
    except Exception as e:
        print(f"❌ Failed to setup frontend: {e}")
        return False

def setup_databases():
    """Initialize databases"""
    print("🗄️  Setting up databases...")
    
    backend_dir = Path(__file__).parent.parent / "backend"
    databases_dir = backend_dir / "databases"
    
    # Ensure databases directory exists
    databases_dir.mkdir(exist_ok=True)
    
    print("✅ Database directory ready")
    return True

def verify_installation():
    """Verify the installation"""
    print("✅ Verifying installation...")
    
    # Check if main files exist
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        "backend/main.py",
        "backend/database.py", 
        "backend/requirements.txt",
        "frontend/src/App.tsx",
        "frontend/src/components/Navigation.tsx",
        "scripts/start.py"
    ]
    
    all_good = True
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_good = False
    
    return all_good

def print_success_message():
    """Print success message with instructions"""
    message = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                      🎉 Setup Complete! 🎉                      ║
    ║                                                                  ║
    ║  Your Unified Ontology Platform is ready!                       ║
    ║                                                                  ║
    ║  To start the platform:                                          ║
    ║    python3 scripts/start.py                                     ║
    ║                                                                  ║
    ║  The platform will be available at:                             ║
    ║  🔗 Backend API: http://localhost:8000                          ║
    ║  📖 API Docs: http://localhost:8000/api/docs                    ║
    ║  🎨 Frontend: http://localhost:3000                             ║
    ║                                                                  ║
    ║  Platform endpoints:                                             ║
    ║  📚 Books: http://localhost:8000/api/books                      ║
    ║  👨‍🏫 Faculty: http://localhost:8000/api/faculty                 ║
    ║  🎓 Students: http://localhost:8000/api/students                ║
    ║  📋 Classes: http://localhost:8000/api/classes                  ║
    ║  🧠 Ontology: http://localhost:8000/api/ontology                ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(message)

def main():
    """Main setup function"""
    print_banner()
    
    success = True
    
    # Setup backend
    if not setup_backend():
        success = False
    
    # Setup frontend  
    if not setup_frontend():
        success = False
        
    # Setup databases
    if not setup_databases():
        success = False
    
    # Verify installation
    if not verify_installation():
        success = False
    
    if success:
        print_success_message()
        return 0
    else:
        print("❌ Setup completed with errors")
        return 1

if __name__ == "__main__":
    sys.exit(main())