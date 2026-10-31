import json
from app import create_app

app = create_app()
client = app.test_client()

def test_all():
    print("--- 1. Testing Health Endpoint ---")
    res = client.get('/api/health')
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print("Health check OK:", res.get_json())

    print("\n--- 2. Testing Items List & Stats ---")
    res = client.get('/api/items')
    assert res.status_code == 200
    data = res.get_json()
    print(f"Total items in DB: {data['total']}")
    assert len(data['items']) > 0

    res = client.get('/api/items/stats')
    assert res.status_code == 200
    print("Item stats:", res.get_json())

    print("\n--- 3. Testing Student Login ---")
    res = client.post('/api/auth/login', json={
        'email': 'aarav@student.edu',
        'password': 'student123'
    })
    assert res.status_code == 200, f"Student login failed: {res.get_json()}"
    student_data = res.get_json()
    student_token = student_data['token']
    print(f"Student login OK. Logged in as: {student_data['user']['name']} ({student_data['user']['student_id']})")

    print("\n--- 4. Testing Student Claims & Profile ---")
    res = client.get('/api/claims/my-claims', headers={'Authorization': f'Bearer {student_token}'})
    assert res.status_code == 200
    print(f"Student claims retrieved: {len(res.get_json()['claims'])}")

    res = client.get('/api/auth/me', headers={'Authorization': f'Bearer {student_token}'})
    assert res.status_code == 200
    print("Student dashboard profile stats:", res.get_json()['user']['stats'])

    print("\n--- 5. Testing Admin Login & Overview ---")
    res = client.post('/api/auth/login', json={
        'email': 'admin@campusfind.edu',
        'password': 'admin123'
    })
    assert res.status_code == 200, f"Admin login failed: {res.get_json()}"
    admin_token = res.get_json()['token']
    print("Admin login OK.")

    res = client.get('/api/admin/overview', headers={'Authorization': f'Bearer {admin_token}'})
    assert res.status_code == 200
    print("Admin overview stats:", res.get_json()['items'])

    print("\n--- 6. Testing Unauthorized Admin Access Prevention ---")
    res = client.get('/api/admin/overview', headers={'Authorization': f'Bearer {student_token}'})
    assert res.status_code == 403
    print("Security check passed: Student cannot access admin endpoints (HTTP 403).")

    print("\n--- 7. Testing Open Registration for Any External User (Visitor/General) ---")
    import random
    rand_id = random.randint(10000, 99999)
    res = client.post('/api/auth/register', json={
        'name': f'Kavita Singh {rand_id}',
        'email': f'kavita.{rand_id}@gmail.com',
        'user_type': 'visitor',
        'password': 'mypassword123'
    })
    assert res.status_code == 201, f"Open registration failed: {res.get_json()}"
    reg_user = res.get_json()['user']
    auto_id = reg_user['student_id']
    print(f"Open registration OK! New user: {reg_user['name']}, Email: {reg_user['email']}, Auto ID: {auto_id}")
    assert auto_id.startswith('VIS-') or auto_id.startswith('CF-'), "Expected auto-generated Campus/Visitor ID"

    print("\n--- 8. Testing Login via Campus ID instead of Email ---")
    res = client.post('/api/auth/login', json={
        'identifier': auto_id,
        'password': 'mypassword123'
    })
    assert res.status_code == 200, f"Login with Campus ID failed: {res.get_json()}"
    print(f"Campus ID login OK! Logged in as: {res.get_json()['user']['name']}")

    print("\n--- 9. Testing Demo Account Login via Roll Number ---")
    res = client.post('/api/auth/login', json={
        'identifier': 'BCA-2024-012',
        'password': 'student123'
    })
    assert res.status_code == 200, f"Roll number login failed: {res.get_json()}"
    print(f"Roll Number login OK! Logged in as: {res.get_json()['user']['name']}")

    print("\nALL BACKEND API TESTS PASSED PERFECTLY!")

if __name__ == '__main__':
    test_all()
