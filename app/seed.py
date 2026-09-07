from app.database import SessionLocal
from app.models import Customer


def seed():
    db = SessionLocal()
    try:
        existing_count = db.query(Customer).count()
        if existing_count > 0:
            print(f"Customers already exist ({existing_count}) — skipping seed.")
            return

        customers = [
            Customer(name="Test Customer", api_key="test-customer-key-001"),
            Customer(name="Acme Corp", api_key="acme-corp-key-002"),
        ]
        db.add_all(customers)
        db.commit()
        print(f"Seeded {len(customers)} customers.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()