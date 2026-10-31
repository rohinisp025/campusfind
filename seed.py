import sys
from datetime import datetime, timedelta, timezone
from app import create_app
from models import db, User, Item, Claim, ClaimMessage, Notification

app = create_app()

def seed_database():
    with app.app_context():
        print("Cleaning existing database tables...")
        db.drop_all()
        db.create_all()

        print("Creating Users...")
        # 1. Admin
        admin = User(
            name="Prof. Rajesh Verma",
            email="admin@campusfind.edu",
            student_id="FAC-CS-001",
            department="Dept of Computer Applications & IT",
            phone="+91 98765 43210",
            role="admin",
            avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
        )
        admin.set_password("admin123")
        db.session.add(admin)

        # 2. Students
        s1 = User(
            name="Aarav Sharma",
            email="aarav@student.edu",
            student_id="BCA-2024-012",
            department="Computer Applications (BCA)",
            phone="+91 91234 56781",
            role="student",
            avatar="https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150"
        )
        s1.set_password("student123")
        db.session.add(s1)

        s2 = User(
            name="Priya Patel",
            email="priya@student.edu",
            student_id="BCA-2024-045",
            department="Computer Applications (BCA)",
            phone="+91 91234 56782",
            role="student",
            avatar="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150"
        )
        s2.set_password("student123")
        db.session.add(s2)

        s3 = User(
            name="Rohan Gupta",
            email="rohan@student.edu",
            student_id="BCA-2023-089",
            department="Computer Science & Data",
            phone="+91 91234 56783",
            role="student",
            avatar="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"
        )
        s3.set_password("student123")
        db.session.add(s3)

        s4 = User(
            name="Sneha Reddy",
            email="sneha@student.edu",
            student_id="BCA-2024-033",
            department="Information Technology",
            phone="+91 91234 56784",
            role="student",
            avatar="https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150"
        )
        s4.set_password("student123")
        db.session.add(s4)

        db.session.commit()

        print("Creating Sample Lost & Found Items...")
        items_data = [
            {
                "title": "HP 65W Laptop Charger (Blue Pin)",
                "type": "lost",
                "category": "Electronics & Gadgets",
                "description": "Black HP 65W original laptop power adapter with blue tip. Forgot it plugged into the third power strip on table 4 during our Java Lab session.",
                "location": "Computer Science & IT Block - MCA/BCA Lab 1",
                "date_lost_or_found": (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d"),
                "primary_color": "Black",
                "brand": "HP",
                "photo_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600",
                "status": "open",
                "user_id": s1.id,
                "contact_email": s1.email,
                "contact_phone": s1.phone
            },
            {
                "title": "Navy Blue Wildcraft College Backpack",
                "type": "found",
                "category": "Bags & Backpacks",
                "description": "Found a navy blue Wildcraft backpack left unattended on the library 2nd floor silent reading zone. Contains class notes for BCA Semester 4 and a pencil pouch.",
                "location": "Central Library (2nd Floor Reading Hall)",
                "date_lost_or_found": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "primary_color": "Navy Blue",
                "brand": "Wildcraft",
                "photo_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
                "status": "open",
                "user_id": s2.id,
                "contact_email": s2.email,
                "contact_phone": s2.phone
            },
            {
                "title": "Apple AirPods 2nd Gen with Charging Case",
                "type": "found",
                "category": "Electronics & Gadgets",
                "description": "Found white AirPods in their original charging case under seat E-14 during the morning tech seminar. Case has a small cartoon astronaut sticker on the back.",
                "location": "Auditorium / Seminar Hall 1",
                "date_lost_or_found": (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d"),
                "primary_color": "White",
                "brand": "Apple",
                "photo_url": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=600",
                "status": "open",
                "user_id": s3.id,
                "contact_email": s3.email,
                "contact_phone": s3.phone
            },
            {
                "title": "Casio Scientific Calculator fx-991ES PLUS",
                "type": "lost",
                "category": "Calculators & Stationery",
                "description": "Lost my grey scientific calculator right after the Mathematics internal exam. It has my initial 'R.G.' engraved on the backside slide cover.",
                "location": "Computer Science & IT Block - Lab 2",
                "date_lost_or_found": (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d"),
                "primary_color": "Grey / Silver",
                "brand": "Casio",
                "photo_url": "https://images.unsplash.com/photo-1611125832047-1d7ad1e8e48f?w=600",
                "status": "open",
                "user_id": s3.id,
                "contact_email": s3.email,
                "contact_phone": s3.phone
            },
            {
                "title": "Official College ID Card with Blue Lanyard",
                "type": "found",
                "category": "College IDs & Cards",
                "description": "Found a student identity card along with college RFID access card on table 7 in the cafeteria. Handed over details safely to avoid misuse.",
                "location": "Main College Cafeteria / Food Court",
                "date_lost_or_found": (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d"),
                "primary_color": "Blue",
                "brand": "College ID",
                "photo_url": "https://images.unsplash.com/photo-1589330694653-dad6bc01cf0e?w=600",
                "status": "resolved",
                "user_id": s4.id,
                "contact_email": s4.email,
                "contact_phone": s4.phone
            },
            {
                "title": "Silver Milton Thermosteel Water Bottle (1000ml)",
                "type": "found",
                "category": "Water Bottles & Flasks",
                "description": "Stainless steel 1-liter vacuum insulated bottle found near the spectator bench next to the basketball court. Clean and intact.",
                "location": "College Sports Complex & Gymnasium",
                "date_lost_or_found": (datetime.now(timezone.utc) - timedelta(days=4)).strftime("%Y-%m-%d"),
                "primary_color": "Silver",
                "brand": "Milton",
                "photo_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600",
                "status": "open",
                "user_id": s1.id,
                "contact_email": s1.email,
                "contact_phone": s1.phone
            },
            {
                "title": "Bike Keys with Red Honda Keychain",
                "type": "lost",
                "category": "Keys & Keychains",
                "description": "Pair of two bike keys on a red braided Honda keychain with a small brass ring. Probably slipped out of pocket while parking.",
                "location": "Parking Area - 2 Wheeler Stand",
                "date_lost_or_found": (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d"),
                "primary_color": "Silver & Red",
                "brand": "Honda",
                "photo_url": "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=600",
                "status": "open",
                "user_id": s2.id,
                "contact_email": s2.email,
                "contact_phone": s2.phone
            },
            {
                "title": "Fastrack Brown Leather Wallet",
                "type": "lost",
                "category": "Wallets & Purses",
                "description": "Dark brown leather tri-fold wallet. Contains student metro pass, driver's license, and some cash. Deeply need the documents back!",
                "location": "Bus Stop / Main Campus Gate 1",
                "date_lost_or_found": (datetime.now(timezone.utc) - timedelta(days=5)).strftime("%Y-%m-%d"),
                "primary_color": "Brown",
                "brand": "Fastrack",
                "photo_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=600",
                "status": "open",
                "user_id": s4.id,
                "contact_email": s4.email,
                "contact_phone": s4.phone
            }
        ]

        created_items = []
        for item_info in items_data:
            item = Item(**item_info)
            db.session.add(item)
            created_items.append(item)

        db.session.commit()

        print("Creating Sample Claims & Verification Messages...")
        # 1. Claim on the AirPods (s1 claims the airpods found by s3)
        airpods_item = created_items[2]
        claim1 = Claim(
            item_id=airpods_item.id,
            claimant_id=s1.id,
            proof_description="The left earbud has a tiny hairline scuff near the microphone tip. The Bluetooth name set is 'Aarav's Pods' and serial ending in '849X'.",
            secret_identifier="Bluetooth device name: Aarav's Pods (shows when connecting to my iPhone 13)",
            proof_image_url="https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?w=500",
            status="pending"
        )
        db.session.add(claim1)
        db.session.commit()

        # Messages on Claim 1
        m1 = ClaimMessage(
            claim_id=claim1.id,
            sender_id=s1.id,
            message="Hi Rohan! Thanks so much for turning this in. I lost it right at the end of the seminar."
        )
        m2 = ClaimMessage(
            claim_id=claim1.id,
            sender_id=s3.id,
            message="Hey Aarav! Can you confirm what color the astronaut sticker on the case is?"
        )
        m3 = ClaimMessage(
            claim_id=claim1.id,
            sender_id=s1.id,
            message="Yes! It's a glow-in-the-dark blue and orange space suit sticker!"
        )
        db.session.add_all([m1, m2, m3])

        # 2. Approved Claim on the College ID card
        id_item = created_items[4]
        claim2 = Claim(
            item_id=id_item.id,
            claimant_id=s1.id,
            proof_description="My student ID card: Name Aarav Sharma, Roll No BCA-2024-012, blood group O+ve.",
            secret_identifier="Roll number BCA-2024-012 matches database",
            status="approved",
            admin_notes="Verified via College Identity database record. Returned safely."
        )
        db.session.add(claim2)

        print("Creating Sample Notifications...")
        n1 = Notification(
            user_id=s3.id,
            title="New Ownership Claim Received",
            message=f"Student Aarav Sharma submitted an ownership claim for your found item: '{airpods_item.title}'.",
            type="claim_received",
            link="/dashboard"
        )
        n2 = Notification(
            user_id=s1.id,
            title="Claim Approved: College ID Card",
            message=f"Your claim for '{id_item.title}' has been verified and approved! You can pick it up safely.",
            type="claim_approved",
            link="/dashboard"
        )
        db.session.add_all([n1, n2])
        db.session.commit()

        print("=" * 60)
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("Demo Accounts Created:")
        print(" 1. ADMIN USER:")
        print("    Email: admin@campusfind.edu")
        print("    Password: admin123")
        print(" 2. STUDENT USER:")
        print("    Email: aarav@student.edu")
        print("    Password: student123")
        print(" 3. STUDENT USER 2:")
        print("    Email: priya@student.edu")
        print("    Password: student123")
        print("=" * 60)

if __name__ == '__main__':
    seed_database()
