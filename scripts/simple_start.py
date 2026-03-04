#!/usr/bin/env python3
"""
Simple Unified Ontology Platform Startup Script

This is a simplified version that just starts the backend server.
Use this if the main start.py script has issues.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Simple Start - Unified Ontology Platform")
    print("=" * 50)
    
    backend_dir = Path(__file__).parent.parent / "backend"
    
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return 1
    
    print("📡 Starting backend server on http://localhost:9001...")
    print("📖 API Docs will be at: http://localhost:9001/api/docs")
    print("⌨️  Press Ctrl+C to stop")
    print("")
    
    try:
        os.chdir(backend_dir)
        
        # Start the server directly
        result = subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "9001", 
            "--reload"
        ])
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
        return 0
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())