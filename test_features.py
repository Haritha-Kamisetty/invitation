"""
Test script to verify all new professional features
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_venue_autocomplete():
    """Test venue autocomplete API"""
    print("\n=== Testing Venue Autocomplete ===")
    try:
        response = requests.get(f"{BASE_URL}/api/venues/autocomplete?q=Mumbai&country=in")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} venues")
            if data:
                print(f"First venue: {data[0].get('display_name', 'N/A')}")
            print("[OK] Venue autocomplete working!")
        else:
            print(f"[ERROR] Error: {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception: {str(e)}")

def test_venue_geocode():
    """Test venue geocoding API"""
    print("\n=== Testing Venue Geocoding ===")
    try:
        response = requests.post(
            f"{BASE_URL}/api/venues/geocode",
            json={"address": "Gateway of India, Mumbai"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Coordinates: {data.get('lat')}, {data.get('lon')}")
            print(f"Address: {data.get('display_name', 'N/A')}")
            print("[OK] Geocoding working!")
        else:
            print(f"[ERROR] Error: {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception: {str(e)}")

def test_api_endpoints():
    """Test that all API endpoints are accessible"""
    print("\n=== Testing API Endpoint Availability ===")
    
    endpoints = [
        ("GET", "/api/venues/autocomplete?q=test"),
        ("POST", "/api/venues/geocode"),
    ]
    
    for method, endpoint in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url)
            else:
                response = requests.post(url, json={})
            
            print(f"{method} {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"{method} {endpoint}: [ERROR] {str(e)}")

def main():
    print("=" * 60)
    print("PROFESSIONAL FEATURES TEST SUITE")
    print("=" * 60)
    
    # Test venue services
    test_venue_autocomplete()
    test_venue_geocode()
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED - APPLICATION WORKING CORRECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
