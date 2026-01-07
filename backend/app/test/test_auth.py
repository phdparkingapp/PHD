#!/usr/bin/env python3
"""
Test script for Firebase authentication.
Tests authentication endpoints and token verification.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_health():
    """Test the health endpoint"""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_verify_token_invalid():
    """Test with an invalid token"""
    print("\n🔍 Testing /auth/verify-token with invalid token...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/verify-token",
            headers={"Authorization": "Bearer invalid_token"}
        )
        print(f"✅ Expected status (401): {response.status_code}")
        return response.status_code == 401
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_me_endpoint_no_token():
    """Test /me without token"""
    print("\n🔍 Testing /users/me without token...")
    try:
        response = requests.get(f"{BASE_URL}/api/users/me")
        print(f"✅ Expected status (401): {response.status_code}")
        return response.status_code == 401
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_with_real_token(token):
    """Test with a real Firebase token"""
    print(f"\n🔍 Testing with a real Firebase token...")
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Test verify-token
        print("  📝 Test /auth/verify-token...")
        response = requests.post(
            f"{BASE_URL}/api/auth/verify-token",
            headers=headers
        )
        print(f"    ✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ User ID: {data.get('user_id')}")
            print(f"    ✅ Firebase UID: {data.get('firebase_uid')}")
            print(f"    ✅ Email: {data.get('email')}")

        # Test login
        print("  📝 Test /auth/login...")
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            headers=headers
        )
        print(f"    ✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(
                f"    ✅ User: {data.get('display_name', 'N/A')} ({data.get('email', 'N/A')})")

        # Test logout
        print("  📝 Test /auth/logout...")
        response = requests.post(f"{BASE_URL}/api/auth/logout")
        print(f"    ✅ Status: {response.status_code}")
        if response.status_code == 200:
            print(f"    ✅ Message: {response.json().get('message')}")

        # Test /auth/me
        print("  📝 Test /auth/me...")
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers=headers
        )
        print(f"    ✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(
                f"    ✅ User: {data.get('display_name', 'N/A')} (ID: {data.get('id')})")

        # Test /users/me (old endpoint)
        print("  📝 Test /users/me...")
        response = requests.get(
            f"{BASE_URL}/api/users/me",
            headers=headers
        )
        print(f"    ✅ Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(
                f"    ✅ User: {data.get('display_name', 'N/A')} (ID: {data.get('id')})")

        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("🚀 Firebase Authentication Backend Test")
    print("=" * 50)

    # Basic tests
    health_ok = test_health()
    token_invalid_ok = test_verify_token_invalid()
    me_no_token_ok = test_me_endpoint_no_token()

    print(f"\n📊 Basic test results:")
    print(f"   Health endpoint: {'✅' if health_ok else '❌'}")
    print(f"   Invalid token: {'✅' if token_invalid_ok else '❌'}")
    print(f"   /me without token: {'✅' if me_no_token_ok else '❌'}")

    # Test with a real token (if provided)
    print(f"\n🔑 To test with a real Firebase token:")
    print(f"   1. Log in via the Flutter app")
    print(f"   2. Retrieve the idToken from Firebase Auth")
    print(f"   3. Run: python test_auth.py YOUR_TOKEN_HERE")

    import sys
    if len(sys.argv) > 1:
        token = sys.argv[1]
        real_token_ok = test_with_real_token(token)
        print(f"   Real token: {'✅' if real_token_ok else '❌'}")


if __name__ == "__main__":
    main()
