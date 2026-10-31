import json
import time
import random
from app import create_app

app = create_app()
client = app.test_client()

def test_full_portal_flow():
    print("==================================================")
    print(" TESTING CAMPUSFIND FULL-STACK WORKFLOW")
    print("==================================================")

    rand_suffix = random.randint(1000, 9999)
    test_email = f"student.{rand_suffix}@campusfind.test"

    # 1. Register a new user without mandatory roll number (open registration)
    print(f"\n1. Registering user: Neeraj Kumar ({test_email})...")
    reg_res = client.post('/api/auth/register', json={
        "name": f"Neeraj Kumar {rand_suffix}",
        "email": test_email,
        "user_type": "student",
        "department": "Computer Applications (BCA)",
        "phone": "+91 99887 76655",
        "password": "student123"
    })
    assert reg_res.status_code == 201, f"Registration failed: {reg_res.get_json()}"
    reg_data = reg_res.get_json()
    neeraj_token = reg_data['token']
    neeraj_id = reg_data['user']['id']
    neeraj_campus_id = reg_data['user']['student_id']
    print(f" Registered successfully: User ID #{neeraj_id}, Assigned Campus ID: {neeraj_campus_id}")

    # 2. Test logging in with the newly generated Campus ID
    print(f"\n2. Testing login using Campus ID '{neeraj_campus_id}'...")
    login_id_res = client.post('/api/auth/login', json={
        "identifier": neeraj_campus_id,
        "password": "student123"
    })
    assert login_id_res.status_code == 200, f"Login with Campus ID failed: {login_id_res.get_json()}"
    print(f" Login via Campus ID succeeded for: {login_id_res.get_json()['user']['name']}")

    # 3. Neeraj reports a lost item
    print("\n3. Neeraj posts a Lost Item report...")
    item_res = client.post(
        '/api/items',
        json={
            "title": f"Casio G-Shock Matte Black Watch #{rand_suffix}",
            "type": "lost",
            "category": "Other Belongings",
            "description": "Black rugged digital watch lost during evening basketball practice near the bleachers.",
            "location": "College Sports Complex & Gymnasium",
            "date_lost_or_found": "2026-10-28",
            "primary_color": "Matte Black",
            "brand": "Casio G-Shock",
            "contact_phone": "+91 99887 76655"
        },
        headers={"Authorization": f"Bearer {neeraj_token}"}
    )
    assert item_res.status_code == 201, f"Post item failed: {item_res.get_json()}"
    new_item_id = item_res.get_json()['item']['id']
    print(f" Item posted: ID #{new_item_id} - '{item_res.get_json()['item']['title']}'")

    # 4. Student Priya logs in using demo credentials
    print("\n4. Student Priya logs in...")
    priya_login = client.post('/api/auth/login', json={
        "email": "priya@student.edu",
        "password": "student123"
    })
    assert priya_login.status_code == 200
    priya_token = priya_login.get_json()['token']
    print(f" Priya logged in: {priya_login.get_json()['user']['name']}")

    # 5. Priya submits ownership claim
    print("\n5. Priya submits verification claim for the watch...")
    claim_res = client.post(
        '/api/claims',
        json={
            "item_id": new_item_id,
            "proof_description": "My brother's watch. The back plate has model DW-5600BB and a tiny scratch on the strap buckle.",
            "secret_identifier": "Alarm was set to 06:30 AM daily with 24-hr military time mode enabled."
        },
        headers={"Authorization": f"Bearer {priya_token}"}
    )
    assert claim_res.status_code == 201, f"Claim submission failed: {claim_res.get_json()}"
    claim_id = claim_res.get_json()['claim']['id']
    print(f" Claim submitted: Claim ID #{claim_id} (Status: {claim_res.get_json()['claim']['status']})")

    # 6. Priya sends a message in the verification chat
    print("\n6. Priya sends message in claim thread...")
    msg_res = client.post(
        f'/api/claims/{claim_id}/messages',
        json={"message": "Hey Neeraj, I can meet you at Central Security Gate 1 during lunch break to verify!"},
        headers={"Authorization": f"Bearer {priya_token}"}
    )
    assert msg_res.status_code == 201
    print(f" Message sent: '{msg_res.get_json()['data']['message']}'")

    # 7. Neeraj replies in the verification thread
    print("\n7. Neeraj replies in claim thread...")
    reply_res = client.post(
        f'/api/claims/{claim_id}/messages',
        json={"message": "Sounds perfect Priya! The alarm detail and buckle scratch match 100%."},
        headers={"Authorization": f"Bearer {neeraj_token}"}
    )
    assert reply_res.status_code == 201
    print(f" Reply sent: '{reply_res.get_json()['data']['message']}'")

    # 8. Neeraj approves the claim
    print("\n8. Neeraj approves the claim and marks item reunited...")
    status_res = client.post(
        f'/api/claims/{claim_id}/status',
        json={"status": "approved", "notes": "Ownership verified. Safe handover at Security Gate 1 scheduled."},
        headers={"Authorization": f"Bearer {neeraj_token}"}
    )
    assert status_res.status_code == 200
    print(f" Claim updated: Status is now '{status_res.get_json()['claim']['status']}'")

    # 9. Verify Item status in catalog
    item_check = client.get(f'/api/items/{new_item_id}')
    assert item_check.status_code == 200
    assert item_check.get_json()['item']['status'] == 'resolved', "Item should now be resolved!"
    print(f" Item status after claim approval verified: '{item_check.get_json()['item']['status']}'")

    # 10. Admin checks overview
    print("\n10. Admin logs in to verify system metrics...")
    admin_login = client.post('/api/auth/login', json={
        "email": "admin@campusfind.edu",
        "password": "admin123"
    })
    assert admin_login.status_code == 200
    admin_token = admin_login.get_json()['token']
    overview = client.get('/api/admin/overview', headers={"Authorization": f"Bearer {admin_token}"})
    assert overview.status_code == 200
    print(" Admin metrics verified:")
    print(f"   - Total Items: {overview.get_json()['items']['total']}")
    print(f"   - Resolved Reunited: {overview.get_json()['items']['resolved']}")
    print(f"   - Recovery Success Rate: {overview.get_json()['items']['recovery_rate']}%")
    print(f"   - Total Verified Users: {overview.get_json()['users']['total']}")

    print("\n==================================================")
    print(" ALL WORKFLOW TESTS PASSED WITHOUT ERRORS! ")
    print("==================================================")

if __name__ == '__main__':
    test_full_portal_flow()
