#!/usr/bin/env python3
"""
Test error handling scenarios for the Todo API
"""
import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def test_error_handling():
    print("Testing error handling scenarios...")

    # Test 1: Try to get a non-existent todo
    print("\n1. Testing GET /todos/{non_existent_id}")
    response = requests.get(f"{BASE_URL}/todos/non-existent-id")
    print(f"GET /todos/non-existent-id status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()
    assert response.json()["data"] is None

    # Test 2: Try to update a non-existent todo
    print("\n2. Testing PUT /todos/{non_existent_id}")
    update_data = {
        "title": "Should not update",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/todos/non-existent-id", json=update_data)
    print(f"PUT /todos/non-existent-id status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()
    assert response.json()["data"] is None

    # Test 3: Try to delete a non-existent todo
    print("\n3. Testing DELETE /todos/{non_existent_id}")
    response = requests.delete(f"{BASE_URL}/todos/non-existent-id")
    print(f"DELETE /todos/non-existent-id status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()
    assert response.json()["data"] is None

    # Test 4: Create a valid todo first for update testing
    print("\n4. Creating a todo to test valid update operations")
    new_todo = {
        "title": "Test todo for error handling",
        "completed": False
    }
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    print(f"POST /todos status: {response.status_code}")
    created_todo = response.json()["data"]
    print(f"Created todo: {created_todo}")
    assert response.status_code == 201
    todo_id = created_todo["id"]

    # Test 5: Try to update with invalid data (though our API is flexible)
    print(f"\n5. Testing PUT /todos/{todo_id} with partial update")
    update_data = {
        "title": "Updated title only"
        # Not sending 'completed' to test partial update
    }
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
    print(f"PUT /todos/{todo_id} with partial data status: {response.status_code}")
    updated_todo = response.json()["data"]
    print(f"Updated todo: {updated_todo}")
    assert response.status_code == 200
    assert updated_todo["title"] == "Updated title only"
    # completed should remain as it was (should still be False from creation)

    # Test 6: Test GET all todos
    print("\n6. Testing GET /todos (should work)")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"GET /todos status: {response.status_code}")
    all_todos = response.json()["data"]
    print(f"Total todos: {len(all_todos)}")
    assert response.status_code == 200

    # Test 7: Delete the todo we created
    print(f"\n7. Testing DELETE /todos/{todo_id}")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    print(f"DELETE /todos/{todo_id} status: {response.status_code}")
    deleted_todo = response.json()["data"]
    print(f"Deleted todo: {deleted_todo}")
    assert response.status_code == 200

    # Test 8: Try to delete the same todo again (should fail)
    print(f"\n8. Testing DELETE /todos/{todo_id} again (should fail)")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    print(f"DELETE /todos/{todo_id} (second time) status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()
    assert response.json()["data"] is None

    print("\nSUCCESS: All error handling scenarios tested successfully!")
    print("SUCCESS: Error handling test passed!")

if __name__ == "__main__":
    test_error_handling()