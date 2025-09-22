#!/usr/bin/env python3
"""
Smart Dataset Generator Backend Startup Script
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import fastapi
        import uvicorn
        import requests
        import pandas
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file found")
        return True
    else:
        print("✗ .env file not found")
        print("Please copy env.example to .env and add your API keys")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["data", "data/temp"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✓ Directories created")

def main():
    """Main startup function"""
    print("=" * 60)
    print("SMART DATASET GENERATOR BACKEND")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment file
    if not check_env_file():
        print("\nTo get started:")
        print("1. Copy env.example to .env")
        print("2. Add your API keys to .env")
        print("3. Run this script again")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n🚀 Starting Smart Dataset Generator Backend...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    # Start the server
    try:
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
