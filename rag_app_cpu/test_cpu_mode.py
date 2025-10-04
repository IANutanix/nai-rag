#!/usr/bin/env python3
"""
Test script for CPU mode functionality
"""

import requests
import json

def test_cpu_mode():
    """Test the CPU mode with gemma-9b-cpu model"""
    
    # Configuration
    endpoint_url = "https://ai.nutanix.com/api/v1/chat/completions"
    model_name = "gemma-9b-cpu"
    api_key = "bf0ba95c-99a2-4f2b-8c6b-54ba6ef3310f"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Test data
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "Explain Deep Neural Networks in simple terms"
            }
        ],
        "max_tokens": 256,
        "stream": False
    }
    
    try:
        print(f"Testing CPU mode with model: {model_name}")
        print(f"Endpoint: {endpoint_url}")
        print("Sending request...")
        
        response = requests.post(endpoint_url, headers=headers, json=data, timeout=30, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            print("Success!")
            print(f"Response: {result['choices'][0]['message']['content']}")
            
            if 'usage' in result:
                usage = result['usage']
                print(f"Token usage - Input: {usage.get('prompt_tokens', 0)}, Output: {usage.get('completion_tokens', 0)}")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    test_cpu_mode()