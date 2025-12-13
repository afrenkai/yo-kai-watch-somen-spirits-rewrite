#!/usr/bin/env python3

import requests
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("  PASS")

def test_get_yokai():
    print("Testing GET /api/yokai...")
    response = requests.get(f"{BASE_URL}/api/yokai")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"  PASS - Found {len(data)} yokai")

def test_get_yokai_by_id():
    print("Testing GET /api/yokai/1...")
    response = requests.get(f"{BASE_URL}/api/yokai/1")
    assert response.status_code == 200
    yokai = response.json()
    assert yokai["id"] == 1
    assert "name" in yokai
    print(f"  PASS - Found {yokai['name']}")

def test_get_teams():
    print("Testing GET /api/teams...")
    response = requests.get(f"{BASE_URL}/api/teams")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"  PASS - Found {len(data)} teams")

def test_create_team():
    print("Testing POST /api/teams...")
    payload = {
        "name": "Test Team",
        "yokai_ids": [1, 2, 3],
        "tier": "OU"
    }
    response = requests.post(f"{BASE_URL}/api/teams?user_id=1", json=payload)
    assert response.status_code == 200
    team = response.json()
    assert team["name"] == "Test Team"
    assert len(team["yokai_ids"]) == 3
    print(f"  PASS - Created team {team['id']}")
    return team["id"]

def test_get_battles():
    print("Testing GET /api/battles...")
    response = requests.get(f"{BASE_URL}/api/battles")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"  PASS - Found {len(data)} battles")

def test_matchmaking_stats():
    print("Testing GET /api/matchmaking/stats...")
    response = requests.get(f"{BASE_URL}/api/matchmaking/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "queues" in stats
    assert "active_battles" in stats
    print(f"  PASS - Active battles: {stats['active_battles']}")

def run_all_tests():
    print("\n=== Running API Tests ===\n")
    
    try:
        test_health()
        test_get_yokai()
        test_get_yokai_by_id()
        test_get_teams()
        test_create_team()
        test_get_battles()
        test_matchmaking_stats()
        
        print("\n=== All Tests Passed ===\n")
        return 0
    except AssertionError as e:
        print(f"\n  FAIL: {e}")
        return 1
    except requests.exceptions.ConnectionError:
        print("\n  ERROR: Cannot connect to API server")
        print("  Make sure the server is running: uvicorn main:socket_app --reload")
        return 1
    except Exception as e:
        print(f"\n  ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
