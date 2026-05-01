"""
Python seed script — programmatic demo data seeder.
Uses async SQLAlchemy directly (no HTTP calls needed).

Usage:
    cd backend
    python -m scripts.seed_db

Idempotent: safe to run multiple times (uses merge / upsert pattern).
"""
import asyncio
import logging
from datetime import date, time, timedelta

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.database import AsyncSessionLocal, engine, Base
from app.core.security import hash_password
from app.models import (  # noqa — ensures all models registered
    Organization, User, Vehicle, Job, Route, RouteStop, OptimizationJob
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("seed")

# ── Fixed UUIDs (deterministic, idempotent) ───────────────────────────────────
ORG_ID      = "a1000000-0000-0000-0000-000000000001"
USER_ADMIN  = "b1000000-0000-0000-0000-000000000001"
USER_MGR    = "b2000000-0000-0000-0000-000000000002"
USER_DRIVER = "b3000000-0000-0000-0000-000000000003"
VAN_ID      = "c1000000-0000-0000-0000-000000000001"
TRUCK_ID    = "c2000000-0000-0000-0000-000000000002"
ROUTE_ID    = "e1000000-0000-0000-0000-000000000001"

TOMORROW = date.today() + timedelta(days=1)

JOBS_DATA = [
    dict(
        id="d1000000-0000-0000-0000-000000000001",
        title="Airport Cargo Pickup", reference="REF-001",
        address="Bole International Airport, Addis Ababa",
        latitude=8.9778, longitude=38.7992, city="Addis Ababa",
        contact_name="Cargo Office", contact_phone="+251911100001",
        scheduled_date=TOMORROW, time_window_start=time(8, 0), time_window_end=time(10, 0),
        service_time_min=30, weight_kg=120.0, volume_m3=0.8, quantity=3,
        priority="high",
    ),
    dict(
        id="d2000000-0000-0000-0000-000000000002",
        title="Mercato Wholesale Delivery", reference="REF-002",
        address="Addis Mercato, Addis Ababa",
        latitude=9.0100, longitude=38.7350, city="Addis Ababa",
        contact_name="Kebede Store", contact_phone="+251911100002",
        scheduled_date=TOMORROW, time_window_start=time(9, 0), time_window_end=time(12, 0),
        service_time_min=20, weight_kg=250.0, volume_m3=1.5, quantity=10,
        priority="normal",
    ),
    dict(
        id="d3000000-0000-0000-0000-000000000003",
        title="Piazza Retail Delivery", reference="REF-003",
        address="Piazza, Churchill Avenue, Addis Ababa",
        latitude=9.0320, longitude=38.7480, city="Addis Ababa",
        contact_name="Almaz Shop", contact_phone="+251911100003",
        scheduled_date=TOMORROW, time_window_start=time(10, 0), time_window_end=time(13, 0),
        service_time_min=15, weight_kg=75.0, volume_m3=0.4, quantity=5,
        priority="normal",
    ),
    dict(
        id="d4000000-0000-0000-0000-000000000004",
        title="Kazanchis Office Supplies", reference="REF-004",
        address="Kazanchis Business District, Addis Ababa",
        latitude=9.0200, longitude=38.7600, city="Addis Ababa",
        contact_name="Yonas Tesfaye", contact_phone="+251911100004",
        scheduled_date=TOMORROW, time_window_start=time(8, 30), time_window_end=time(11, 0),
        service_time_min=10, weight_kg=40.0, volume_m3=0.2, quantity=2,
        priority="low",
    ),
    dict(
        id="d5000000-0000-0000-0000-000000000005",
        title="CMC Residential Delivery", reference="REF-005",
        address="CMC Road, Addis Ababa",
        latitude=9.0560, longitude=38.7830, city="Addis Ababa",
        contact_name="Hiwot Alemu", contact_phone="+251911100005",
        scheduled_date=TOMORROW, time_window_start=time(11, 0), time_window_end=time(14, 0),
        service_time_min=10, weight_kg=15.0, volume_m3=0.1, quantity=1,
        priority="normal",
    ),
    dict(
        id="d6000000-0000-0000-0000-000000000006",
        title="Sarbet Supermarket Restock", reference="REF-006",
        address="Sarbet, Addis Ababa",
        latitude=8.9950, longitude=38.7560, city="Addis Ababa",
        contact_name="Meron Market", contact_phone="+251911100006",
        scheduled_date=TOMORROW, time_window_start=time(13, 0), time_window_end=time(16, 0),
        service_time_min=25, weight_kg=320.0, volume_m3=2.0, quantity=15,
        priority="high",
    ),
    dict(
        id="d7000000-0000-0000-0000-000000000007",
        title="Gerji Electronics Shop", reference="REF-007",
        address="Gerji, Addis Ababa",
        latitude=9.0070, longitude=38.8100, city="Addis Ababa",
        contact_name="Dawit Tadesse", contact_phone="+251911100007",
        scheduled_date=TOMORROW, time_window_start=time(10, 0), time_window_end=time(14, 0),
        service_time_min=15, weight_kg=60.0, volume_m3=0.5, quantity=4,
        priority="normal",
    ),
    dict(
        id="d8000000-0000-0000-0000-000000000008",
        title="Ayat Residential Complex", reference="REF-008",
        address="Ayat, Addis Ababa",
        latitude=9.0400, longitude=38.8400, city="Addis Ababa",
        contact_name="Selam Hailu", contact_phone="+251911100008",
        scheduled_date=TOMORROW, time_window_start=time(14, 0), time_window_end=time(17, 0),
        service_time_min=10, weight_kg=22.0, volume_m3=0.15, quantity=2,
        priority="low",
    ),
]

ROUTE_STOPS = [
    ("d1000000-0000-0000-0000-000000000001", 1),
    ("d2000000-0000-0000-0000-000000000002", 2),
    ("d3000000-0000-0000-0000-000000000003", 3),
    ("d4000000-0000-0000-0000-000000000004", 4),
    ("d5000000-0000-0000-0000-000000000005", 5),
    ("d6000000-0000-0000-0000-000000000006", 6),
]


async def seed() -> None:
    log.info("Starting database seed…")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log.info("Tables ensured.")

    async with AsyncSessionLocal() as db:
        # ── Organization ──────────────────────────────────────────────────────
        org = Organization(
            id=ORG_ID,
            name="Addis Express Logistics",
            slug="addis-express",
            plan="pro",
            address="Bole Road, Addis Ababa, Ethiopia",
            phone="+251911000001",
            email="ops@addisexpress.et",
        )
        await db.merge(org)
        log.info("Organization upserted.")

        # ── Users ─────────────────────────────────────────────────────────────
        users = [
            User(id="b0000000-0000-0000-0000-000000000000", org_id=ORG_ID, email="super@addisexpress.et",
                 hashed_password=hash_password("SuperPass123!"),
                 full_name="System Superadmin", role="admin", is_superuser=True),
            User(id=USER_ADMIN,  org_id=ORG_ID, email="admin@addisexpress.et",
                 hashed_password=hash_password("AdminPass123!"),
                 full_name="Abebe Girma",   role="admin",   phone="+251911000002"),
            User(id=USER_MGR,    org_id=ORG_ID, email="manager@addisexpress.et",
                 hashed_password=hash_password("ManagerPass123!"),
                 full_name="Tigist Bekele", role="manager", phone="+251911000003"),
            User(id=USER_DRIVER, org_id=ORG_ID, email="driver@addisexpress.et",
                 hashed_password=hash_password("DriverPass123!"),
                 full_name="Solomon Haile", role="driver",  phone="+251911000004"),
        ]
        for u in users:
            await db.merge(u)
        log.info("Users upserted (superadmin, admin, manager, driver).")

        # ── Vehicles ──────────────────────────────────────────────────────────
        vehicles = [
            Vehicle(
                id=VAN_ID, org_id=ORG_ID, driver_id=USER_DRIVER,
                name="Delivery Van #1", license_plate="AA-12345",
                vehicle_type="van", status="available",
                capacity_weight_kg=800, capacity_volume_m3=3.5, max_stops=15,
                fuel_type="diesel", speed_profile="driving",
            ),
            Vehicle(
                id=TRUCK_ID, org_id=ORG_ID, driver_id=None,
                name="Truck #1", license_plate="AA-67890",
                vehicle_type="truck", status="available",
                capacity_weight_kg=3500, capacity_volume_m3=14.0, max_stops=30,
                fuel_type="diesel", speed_profile="driving",
            ),
        ]
        for v in vehicles:
            await db.merge(v)
        log.info("Vehicles upserted (van, truck).")

        # ── Jobs ──────────────────────────────────────────────────────────────
        assigned_job_ids = {jid for jid, _ in ROUTE_STOPS}
        for jd in JOBS_DATA:
            status = "assigned" if jd["id"] in assigned_job_ids else "pending"
            job = Job(org_id=ORG_ID, status=status, **jd)
            await db.merge(job)
        log.info("Jobs upserted (8 delivery points).")

        # ── Route ─────────────────────────────────────────────────────────────
        route = Route(
            id=ROUTE_ID,
            org_id=ORG_ID,
            vehicle_id=VAN_ID,
            driver_id=USER_DRIVER,
            created_by_id=USER_MGR,
            name="Morning Addis Run — Day 1",
            status="draft",
            profile="driving",
            algorithm="osrm_trip",
            scheduled_date=TOMORROW,
            departure_time=time(7, 30),
        )
        await db.merge(route)
        log.info("Route upserted.")

        # ── Route Stops ───────────────────────────────────────────────────────
        for job_id, seq in ROUTE_STOPS:
            stop = RouteStop(
                route_id=ROUTE_ID,
                job_id=job_id,
                sequence=seq,
                status="pending",
            )
            # Use merge-safe approach: check existing
            existing = await db.execute(
                select(RouteStop).where(
                    RouteStop.route_id == ROUTE_ID,
                    RouteStop.job_id == job_id,
                )
            )
            if not existing.scalar_one_or_none():
                db.add(stop)
        log.info("Route stops seeded (6 stops).")

        await db.commit()
        log.info("✅ Seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
