#!/usr/bin/env python3
"""
End-to-end test for the Todo API CRUD functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_crud_flow():
    print("Starting end-to-end CRUD functionality test...")

    # Test 1: Get initial todos (should be empty or have existing ones)
    print("\n1. Testing GET /todos")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"GET /todos status: {response.status_code}")
    print(f"Response: {response.json()}")
    initial_count = len(response.json()["data"])
    print(f"Initial todo count: {initial_count}")

    # Test 2: Create a new todo
    print("\n2. Testing POST /todos")
    new_todo = {
        "title": "Test todo for CRUD flow",
        "completed": False
    }
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    print(f"POST /todos status: {response.status_code}")
    created_todo = response.json()["data"]
    print(f"Created todo: {created_todo}")
    assert response.status_code == 201

    todo_id = created_todo["id"]

    # Test 3: Get the specific todo we just created
    print(f"\n3. Testing GET /todos/{todo_id}")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print(f"GET /todos/{todo_id} status: {response.status_code}")
    retrieved_todo = response.json()["data"]
    print(f"Retrieved todo: {retrieved_todo}")
    assert response.status_code == 200
    assert retrieved_todo["title"] == "Test todo for CRUD flow"

    # Test 4: Update the todo
    print(f"\n4. Testing PUT /todos/{todo_id}")
    update_data = {
        "title": "Updated test todo for CRUD flow",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
    print(f"PUT /todos/{todo_id} status: {response.status_code}")
    updated_todo = response.json()["data"]
    print(f"Updated todo: {updated_todo}")
    assert response.status_code == 200
    assert updated_todo["title"] == "Updated test todo for CRUD flow"
    assert updated_todo["completed"] == True

    # Test 5: Verify the update by getting all todos again
    print("\n5. Verifying update with GET /todos")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"GET /todos status: {response.status_code}")
    all_todos = response.json()["data"]
    print(f"Total todos after update: {len(all_todos)}")

    # Find our updated todo in the list
    our_todo = next((t for t in all_todos if t["id"] == todo_id), None)
    assert our_todo is not None
    assert our_todo["title"] == "Updated test todo for CRUD flow"
    assert our_todo["completed"] == True

    # Test 6: Delete the todo
    print(f"\n6. Testing DELETE /todos/{todo_id}")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    print(f"DELETE /todos/{todo_id} status: {response.status_code}")
    deleted_todo = response.json()["data"]
    print(f"Deleted todo: {deleted_todo}")
    assert response.status_code == 200
    assert deleted_todo["id"] == todo_id

    # Test 7: Verify the todo was deleted by trying to get it
    print(f"\n7. Verifying deletion by getting /todos/{todo_id}")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print(f"GET /todos/{todo_id} status: {response.status_code}")
    assert response.status_code == 404

    # Test 8: Verify the todo is no longer in the list
    print("\n8. Verifying deletion by getting all todos")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"GET /todos status: {response.status_code}")
    final_todos = response.json()["data"]
    print(f"Total todos after deletion: {len(final_todos)}")
    assert len(final_todos) == initial_count  # Should be back to initial count

    print("\nSUCCESS: All CRUD operations completed successfully!")
    print("SUCCESS: End-to-end test passed!")

if __name__ == "__main__":
    test_crud_flow()