#!/usr/bin/env python3
"""
Simple backend test script
"""
import subprocess
import time
import sys

def test_backend():
    # Kill any existing processes on port 8000
    subprocess.run("lsof -i :8000 -sTCP:LISTEN -t | xargs -r kill -9 2>/dev/null || true", 
                   shell=True, capture_output=True)
    time.sleep(2)
    
    # Start the server
    proc = subprocess.Popen(
        ["python3", "-m", "uvicorn", "main:app", "--reload"],
        cwd="/Users/lucky/Documents/FitnessCoachMVP/backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("Starting backend server...")
    time.sleep(5)
    
    # Test the API
    try:
        print("\n🧪 Testing backend...")
        result = subprocess.run(
            ["python3", "-c", """
import requests
try:
    resp = requests.get('http://localhost:8000/', timeout=2)
    print(f'✅ Status: {resp.status_code}')
    print(f'✅ Response: {resp.json()}')
except Exception as e:
    print(f'❌ Error: {e}')
"""],
            cwd="/Users/lucky/Documents/FitnessCoachMVP",
            capture_output=True,
            timeout=10
        )
        print(result.stdout.decode())
        if result.stderr:
            print("Errors:", result.stderr.decode())
            
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
        # Show server output
        stdout, stderr = proc.communicate(timeout=1)
        print("\n🔍 Server output:")
        print(stdout.decode()[:500] if stdout else "No stdout")
        print("\n🔍 Server errors:")
        print(stderr.decode()[:1000] if stderr else "No stderr")
    
    # Cleanup
    try:
        proc.kill()
    except:
        pass

if __name__ == "__main__":
    test_backend()
