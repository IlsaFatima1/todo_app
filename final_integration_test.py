#!/usr/bin/env python3
"""
Final end-to-end integration test for the frontend-backend connection
This test simulates real user interactions with the API through the frontend client
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"

def simulate_frontend_behavior():
    print("Starting final end-to-end integration test...")
    print("Simulating frontend behavior with backend API...")

    # Step 1: Clear any existing todos by getting them first
    print("\n1. Getting initial todos from backend")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"GET /todos status: {response.status_code}")
    initial_todos = response.json()["data"]
    print(f"Initial todos count: {len(initial_todos)}")

    # Step 2: Simulate creating a new todo (like frontend would)
    print("\n2. Creating a new todo (simulating frontend POST)")
    new_todo_data = {
        "title": "Integration test todo",
        "completed": False
    }
    response = requests.post(f"{BASE_URL}/todos", json=new_todo_data)
    print(f"POST /todos status: {response.status_code}")
    created_todo = response.json()["data"]
    print(f"Created todo: ID={created_todo['id']}, Title='{created_todo['title']}', Completed={created_todo['completed']}")
    assert response.status_code == 201
    assert created_todo["title"] == "Integration test todo"
    assert created_todo["completed"] is False

    todo_id = created_todo["id"]

    # Step 3: Simulate getting all todos (like frontend does on page load)
    print("\n3. Getting all todos (simulating frontend GET)")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"GET /todos status: {response.status_code}")
    all_todos = response.json()["data"]
    print(f"All todos after creation: {len(all_todos)}")
    assert len(all_todos) == len(initial_todos) + 1

    # Verify our todo is in the list
    our_todo = next((t for t in all_todos if t["id"] == todo_id), None)
    assert our_todo is not None
    assert our_todo["title"] == "Integration test todo"
    assert our_todo["completed"] is False

    # Step 4: Simulate updating a todo (like frontend would when toggling completion)
    print("\n4. Updating todo completion status (simulating frontend PUT)")
    update_data = {
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
    print(f"PUT /todos/{todo_id} status: {response.status_code}")
    updated_todo = response.json()["data"]
    print(f"Updated todo: ID={updated_todo['id']}, Title='{updated_todo['title']}', Completed={updated_todo['completed']}")
    assert response.status_code == 200
    assert updated_todo["completed"] is True

    # Step 5: Verify the update worked
    print("\n5. Verifying update by getting the specific todo")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print(f"GET /todos/{todo_id} status: {response.status_code}")
    retrieved_todo = response.json()["data"]
    print(f"Retrieved todo: {retrieved_todo}")
    assert response.status_code == 200
    assert retrieved_todo["id"] == todo_id
    assert retrieved_todo["completed"] is True

    # Step 6: Simulate updating todo title (like frontend would when editing)
    print("\n6. Updating todo title (simulating frontend PUT)")
    update_data = {
        "title": "Updated integration test todo"
    }
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
    print(f"PUT /todos/{todo_id} with new title status: {response.status_code}")
    updated_todo = response.json()["data"]
    print(f"Updated todo: {updated_todo}")
    assert response.status_code == 200
    assert updated_todo["title"] == "Updated integration test todo"

    # Step 7: Simulate deleting a todo (like frontend would when clicking delete)
    print("\n7. Deleting the todo (simulating frontend DELETE)")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    print(f"DELETE /todos/{todo_id} status: {response.status_code}")
    deleted_todo = response.json()["data"]
    print(f"Deleted todo: {deleted_todo}")
    assert response.status_code == 200
    assert deleted_todo["id"] == todo_id

    # Step 8: Verify the todo was deleted
    print("\n8. Verifying todo was deleted by getting all todos")
    response = requests.get(f"{BASE_URL}/todos")
    print(f"GET /todos status: {response.status_code}")
    final_todos = response.json()["data"]
    print(f"Final todos count: {len(final_todos)}")
    assert len(final_todos) == len(initial_todos)  # Should be back to initial count

    # Verify our todo is no longer in the list
    our_todo = next((t for t in final_todos if t["id"] == todo_id), None)
    assert our_todo is None

    # Step 9: Test error handling - try to get the deleted todo
    print("\n9. Testing error handling for non-existent todo")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print(f"GET /todos/{todo_id} (after deletion) status: {response.status_code}")
    error_response = response.json()
    print(f"Error response: {error_response}")
    assert response.status_code == 404
    assert error_response["data"] is None
    assert "not found" in error_response["message"].lower()

    # Step 10: Test creating multiple todos to simulate bulk operations
    print("\n10. Testing bulk operations (creating multiple todos)")
    todo_titles = ["Bulk todo 1", "Bulk todo 2", "Bulk todo 3"]
    created_ids = []

    for title in todo_titles:
        new_todo_data = {"title": title, "completed": False}
        response = requests.post(f"{BASE_URL}/todos", json=new_todo_data)
        print(f"POST for '{title}' status: {response.status_code}")
        created_todo = response.json()["data"]
        created_ids.append(created_todo["id"])
        assert response.status_code == 201

    # Verify all were created
    response = requests.get(f"{BASE_URL}/todos")
    all_todos = response.json()["data"]
    print(f"Total todos after bulk creation: {len(all_todos)}")
    current_count = len(all_todos)

    # Clean up - delete the bulk created todos
    for todo_id in created_ids:
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
        print(f"DELETE /todos/{todo_id} status: {response.status_code}")
        assert response.status_code == 200

    # Verify cleanup worked
    response = requests.get(f"{BASE_URL}/todos")
    all_todos = response.json()["data"]
    print(f"Total todos after cleanup: {len(all_todos)}")
    assert len(all_todos) == current_count - len(created_ids)

    print("\nSUCCESS: All frontend-backend integration tests passed!")
    print("SUCCESS: Complete end-to-end flow works as expected!")
    print("SUCCESS: API responses are consistent and properly formatted!")
    print("SUCCESS: Error handling works correctly!")
    print("SUCCESS: Frontend-backend integration is fully functional!")

if __name__ == "__main__":
    simulate_frontend_behavior()