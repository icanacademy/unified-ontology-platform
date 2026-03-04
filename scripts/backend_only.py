#!/usr/bin/env python3
"""
Backend-Only Startup Script for Unified Ontology Platform

Starts just the backend API server (which is working perfectly)
The frontend can be added later once dependencies are resolved.
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                 Unified Ontology Platform - Backend             ║
    ║                                                                  ║
    ║  🎓 Integrated Educational Analytics Platform                    ║
    ║                                                                  ║
    ║  All 5 platforms accessible through one API:                    ║
    ║  📚 Books & Library Management                                   ║
    ║  👨‍🏫 Faculty Analytics                                           ║
    ║  🎓 Student Analytics                                            ║
    ║  📋 Class Management                                             ║
    ║  🧠 Ontology Platform                                            ║
    ║                                                                  ║
    ║  🚀 Backend API: http://localhost:9000                          ║
    ║  📖 API Docs: http://localhost:9000/api/docs                    ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    
    backend_dir = Path(__file__).parent.parent / "backend"
    
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return 1
    
    print("🚀 Starting unified backend server...")
    print("📊 All 5 platforms will be available at:")
    print("   📚 Books: http://localhost:9000/api/books")  
    print("   👨‍🏫 Faculty: http://localhost:9000/api/faculty")
    print("   🎓 Students: http://localhost:9000/api/students")
    print("   📋 Classes: http://localhost:9000/api/classes")
    print("   🧠 Ontology: http://localhost:9000/api/ontology")
    print("")
    print("📖 Full API Documentation: http://localhost:9000/api/docs")
    print("⌨️  Press Ctrl+C to stop the server")
    print("=" * 70)
    
    try:
        os.chdir(backend_dir)
        
        # Start the server with clean output
        result = subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "9000", 
            "--reload"
        ])
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n✅ Unified Ontology Platform stopped successfully")
        return 0
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())