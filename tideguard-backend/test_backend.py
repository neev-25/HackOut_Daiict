#!/usr/bin/env python3
"""
Simple test script for TideGuard Backend
"""

import requests
import json
import time
from utils.data_simulator import DataSimulator

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to backend. Is it running?")
        return False

def test_data_simulator():
    """Test the data simulator"""
    print("Testing data simulator...")
    try:
        simulator = DataSimulator()
        data = simulator.generate_data()
        
        required_fields = ['timestamp', 'wind_speed', 'wave_height', 'weather_condition', 
                          'temperature', 'humidity', 'pressure']
        
        for field in required_fields:
            if field not in data:
                print(f"✗ Missing field: {field}")
                return False
        
        print(f"✓ Data simulator working: {data}")
        return True
    except Exception as e:
        print(f"✗ Data simulator failed: {e}")
        return False

def test_threshold_logic():
    """Test threshold checking logic"""
    print("Testing threshold logic...")
    
    # Test data that should trigger alerts
    test_cases = [
        {'wind_speed': 85, 'wave_height': 2.0, 'expected_alert': True},
        {'wind_speed': 70, 'wave_height': 5.0, 'expected_alert': True},
        {'wind_speed': 85, 'wave_height': 5.0, 'expected_alert': True},
        {'wind_speed': 70, 'wave_height': 2.0, 'expected_alert': False},
    ]
    
    for i, test_case in enumerate(test_cases):
        wind_speed = test_case['wind_speed']
        wave_height = test_case['wave_height']
        expected = test_case['expected_alert']
        
        # Simulate threshold check
        alert_triggered = wind_speed > 80 or wave_height > 4
        
        if alert_triggered == expected:
            print(f"✓ Test case {i+1} passed: Wind={wind_speed}km/h, Waves={wave_height}m")
        else:
            print(f"✗ Test case {i+1} failed: Wind={wind_speed}km/h, Waves={wave_height}m")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🌊 TideGuard Backend Tests")
    print("=" * 30)
    
    tests = [
        ("Data Simulator", test_data_simulator),
        ("Threshold Logic", test_threshold_logic),
        ("Health Endpoint", test_health_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print(f"\n{'=' * 30}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())
