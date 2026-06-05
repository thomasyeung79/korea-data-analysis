"""
Data migration script: import existing JSON data into SQLite database.

Usage:
    cd d:\project\practice\south_korea_perception_analysis
    python -m backend.scripts.migrate_data

This script reads user_results.json and korea_travel_orders.json,
creates User records for unique usernames, and links existing data.
"""
import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.database import engine, SessionLocal, Base
from backend.app.models.user import User
from backend.app.models.perception_result import PerceptionResult
from backend.app.models.travel_order import TravelOrder
from backend.app.services.auth_service import hash_password


def migrate():
    print("=" * 60)
    print("KoreaIntel Pro - Data Migration Script")
    print("=" * 60)

    # Create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # ── Load JSON files ──
        user_results_path = PROJECT_ROOT / "user_results.json"
        travel_orders_path = PROJECT_ROOT / "korea_travel_orders.json"

        user_results = []
        travel_orders = []

        if user_results_path.exists():
            with open(user_results_path, "r", encoding="utf-8") as f:
                user_results = json.load(f)
            print(f"Loaded {len(user_results)} perception results from user_results.json")
        else:
            print("user_results.json not found, skipping perception data.")

        if travel_orders_path.exists():
            with open(travel_orders_path, "r", encoding="utf-8") as f:
                travel_orders = json.load(f)
            print(f"Loaded {len(travel_orders)} travel orders from korea_travel_orders.json")
        else:
            print("korea_travel_orders.json not found, skipping travel data.")

        # ── Collect unique usernames ──
        usernames = set()

        for r in user_results:
            name = r.get("username", "").strip()
            if name:
                usernames.add(name)

        for o in travel_orders:
            name = o.get("customer_name", "").strip()
            if name:
                usernames.add(name)

        print(f"\nFound {len(usernames)} unique usernames: {', '.join(sorted(usernames))}")

        # ── Create User records ──
        user_map = {}  # username -> User object

        for username in sorted(usernames):
            existing = db.query(User).filter(User.username == username).first()
            if existing:
                user_map[username] = existing
                print(f"  User '{username}' already exists (id={existing.id})")
            else:
                user = User(
                    username=username,
                    hashed_password=hash_password("migrated_placeholder"),
                    language_preference="English",
                )
                db.add(user)
                db.flush()
                user_map[username] = user
                print(f"  Created user '{username}' (id={user.id}) with placeholder password")

        db.commit()

        # ── Migrate Perception Results ──
        perception_count = 0
        for r in user_results:
            username = r.get("username", "").strip()
            user = user_map.get(username)
            if not user:
                continue

            result = PerceptionResult(
                user_id=user.id,
                technology=float(r.get("technology", 0)),
                culture=float(r.get("culture", 0)),
                pressure=float(r.get("pressure", 0)),
                global_influence=float(r.get("global_influence", 0)),
                overall_score=float(r.get("score", 0)),
                ai_report=str(r.get("ai_result", "")),
            )
            db.add(result)
            perception_count += 1

        db.commit()
        print(f"\nMigrated {perception_count} perception results.")

        # ── Migrate Travel Orders ──
        order_count = 0
        for o in travel_orders:
            username = o.get("customer_name", "").strip()
            user = user_map.get(username)
            if not user:
                continue

            order_id = o.get("order_id", "")
            if not order_id:
                import uuid
                order_id = str(uuid.uuid4())[:8].upper()

            route = o.get("route") or o.get("main_route") or str(o.get("travel_route", ""))
            days = int(o.get("days", 1))
            budget = o.get("budget", "Medium")
            interests = str(o.get("interests", ""))
            travel_style = o.get("travel_style", "Relaxed")
            estimated_price = float(o.get("estimated_price_aud", o.get("estimated_price", 0)))
            ai_plan = o.get("ai_plan")
            itinerary_json = json.dumps(o.get("itinerary", []), ensure_ascii=False) if o.get("itinerary") else None

            order = TravelOrder(
                user_id=user.id,
                order_id=order_id,
                route=str(route),
                days=days,
                budget=budget,
                interests=str(interests),
                travel_style=travel_style,
                estimated_price=estimated_price,
                status=o.get("order_status", "Draft"),
                ai_plan=ai_plan,
                itinerary_json=itinerary_json,
            )
            db.add(order)
            order_count += 1

        db.commit()
        print(f"Migrated {order_count} travel orders.")

        # ── Summary ──
        print("\n" + "=" * 60)
        print("Migration Summary:")
        print(f"  Users:              {len(user_map)}")
        print(f"  Perception Results: {perception_count}")
        print(f"  Travel Orders:      {order_count}")
        print("=" * 60)
        print("\nNOTE: Migrated users have placeholder passwords.")
        print("Users should reset their password on first login via Register.")
        print("Migration complete!")

    except Exception as e:
        db.rollback()
        print(f"\nERROR: Migration failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()
