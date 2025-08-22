#!/usr/bin/env python3
"""
Test script for Payment Wallet Service API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_user():
    """Test user creation"""
    print("=== Testing User Creation ===")
    user_data = {"name": "Test User"}
    response = requests.post(f"{BASE_URL}/wallet/user", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json()["id"]
    return None

def test_add_funds(user_id, amount=100.50):
    """Test adding funds"""
    print(f"=== Testing Add Funds (${amount}) ===")
    funds_data = {
        "user_id": user_id,
        "amount": amount,
        "description": f"Test deposit of ${amount}"
    }
    response = requests.post(f"{BASE_URL}/wallet/addFunds", json=funds_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.status_code == 200

def test_get_balance(user_id):
    """Test getting balance"""
    print("=== Testing Get Balance ===")
    response = requests.get(f"{BASE_URL}/wallet/balance/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.json() if response.status_code == 200 else None

def test_withdraw_funds(user_id, amount=25.00):
    """Test withdrawing funds"""
    print(f"=== Testing Withdraw Funds (${amount}) ===")
    funds_data = {
        "user_id": user_id,
        "amount": amount,
        "description": f"Test withdrawal of ${amount}"
    }
    response = requests.post(f"{BASE_URL}/wallet/withdrawFunds", json=funds_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.status_code == 200

def test_get_transactions(user_id):
    """Test getting transaction history"""
    print("=== Testing Get Transaction History ===")
    response = requests.get(f"{BASE_URL}/wallet/transactions/{user_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_insufficient_funds(user_id):
    """Test insufficient funds scenario"""
    print("=== Testing Insufficient Funds ===")
    funds_data = {
        "user_id": user_id,
        "amount": 1000.00,  # Large amount to trigger insufficient funds
        "description": "Test insufficient funds"
    }
    response = requests.post(f"{BASE_URL}/wallet/withdrawFunds", json=funds_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting Payment Wallet Service API Tests")
    print("=" * 50)
    
    # Test health check
    test_health_check()
    
    # Create a test user
    user_id = test_create_user()
    if not user_id:
        print("❌ Failed to create user. Stopping tests.")
        return
    
    print(f"✅ Created user with ID: {user_id}")
    print()
    
    # Add funds
    if test_add_funds(user_id, 100.50):
        print("✅ Successfully added funds")
    
    # Check balance
    balance_info = test_get_balance(user_id)
    if balance_info:
        print(f"✅ Current balance: ${balance_info['balance']}")
    
    # Withdraw funds
    if test_withdraw_funds(user_id, 25.00):
        print("✅ Successfully withdrew funds")
    
    # Check balance again
    balance_info = test_get_balance(user_id)
    if balance_info:
        print(f"✅ New balance: ${balance_info['balance']}")
    
    # Get transaction history
    test_get_transactions(user_id)
    
    # Test insufficient funds
    test_insufficient_funds(user_id)
    
    print("=" * 50)
    print("🎉 All tests completed!")
    print("📖 Check Swagger UI at: http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server.")
        print("   Make sure the server is running at http://localhost:8000")
        print("   Run: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
