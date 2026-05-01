-- =============================================================================
-- RouteOpt — Demo / Seed Data
-- Organization: Addis Express Logistics
-- Location context: Addis Ababa, Ethiopia
-- =============================================================================
-- NOTE: Passwords are bcrypt hashes of the plaintext shown in comments.
--       Replace with real hashes in production.
--       Plaintext for testing:
--         admin@addisexpress.et   → AdminPass123!
--         manager@addisexpress.et → ManagerPass123!
--         driver@addisexpress.et  → DriverPass123!
-- =============================================================================

BEGIN;

-- ── 1. Organization ───────────────────────────────────────────────────────────
INSERT INTO organizations (id, name, slug, plan, address, phone, email)
VALUES (
    'a1000000-0000-0000-0000-000000000001',
    'Addis Express Logistics',
    'addis-express',
    'pro',
    'Bole Road, Addis Ababa, Ethiopia',
    '+251911000001',
    'ops@addisexpress.et'
)
ON CONFLICT (id) DO NOTHING;

-- ── 2. Users (3 roles) ────────────────────────────────────────────────────────
-- Passwords below are bcrypt hashes — generated with passlib bcrypt rounds=12
-- admin: AdminPass123!
INSERT INTO users (id, org_id, email, hashed_password, full_name, role, phone)
VALUES (
    'b1000000-0000-0000-0000-000000000001',
    'a1000000-0000-0000-0000-000000000001',
    'admin@addisexpress.et',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiQKjLkOC3gHpFZY/wZPQ/nxVHe2',  -- AdminPass123!
    'Abebe Girma',
    'admin',
    '+251911000002'
)
ON CONFLICT (id) DO NOTHING;

-- manager: ManagerPass123!
INSERT INTO users (id, org_id, email, hashed_password, full_name, role, phone)
VALUES (
    'b2000000-0000-0000-0000-000000000002',
    'a1000000-0000-0000-0000-000000000001',
    'manager@addisexpress.et',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  -- ManagerPass123!
    'Tigist Bekele',
    'manager',
    '+251911000003'
)
ON CONFLICT (id) DO NOTHING;

-- driver: DriverPass123!
INSERT INTO users (id, org_id, email, hashed_password, full_name, role, phone)
VALUES (
    'b3000000-0000-0000-0000-000000000003',
    'a1000000-0000-0000-0000-000000000001',
    'driver@addisexpress.et',
    '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC8a.GB6pL8GtgjkhuPa',  -- DriverPass123!
    'Solomon Haile',
    'driver',
    '+251911000004'
)
ON CONFLICT (id) DO NOTHING;

-- ── 3. Vehicles (2) ───────────────────────────────────────────────────────────
INSERT INTO vehicles (
    id, org_id, driver_id, name, license_plate,
    vehicle_type, status,
    capacity_weight_kg, capacity_volume_m3, max_stops,
    fuel_type, speed_profile
) VALUES
(
    'c1000000-0000-0000-0000-000000000001',
    'a1000000-0000-0000-0000-000000000001',
    'b3000000-0000-0000-0000-000000000003',   -- assigned to driver Solomon
    'Delivery Van #1',
    'AA-12345',
    'van', 'available',
    800,    -- 800 kg
    3.5,    -- 3.5 m³
    15,
    'diesel', 'driving'
),
(
    'c2000000-0000-0000-0000-000000000002',
    'a1000000-0000-0000-0000-000000000001',
    NULL,
    'Truck #1',
    'AA-67890',
    'truck', 'available',
    3500,   -- 3.5 tonnes
    14.0,
    30,
    'diesel', 'driving'
)
ON CONFLICT (id) DO NOTHING;

-- ── 4. Jobs — 8 delivery points in Addis Ababa ───────────────────────────────
INSERT INTO jobs (
    id, org_id,
    title, reference,
    address, latitude, longitude, city,
    contact_name, contact_phone,
    scheduled_date,
    time_window_start, time_window_end, service_time_min,
    weight_kg, volume_m3, quantity,
    status, priority
) VALUES

-- Stop 1: Bole International Airport area
(
    'd1000000-0000-0000-0000-000000000001',
    'a1000000-0000-0000-0000-000000000001',
    'Airport Cargo Pickup',      'REF-001',
    'Bole International Airport, Addis Ababa', 8.9778, 38.7992, 'Addis Ababa',
    'Cargo Office',              '+251911100001',
    CURRENT_DATE + 1,
    '08:00', '10:00', 30,
    120.0, 0.8, 3,
    'pending', 'high'
),

-- Stop 2: Mercato Market
(
    'd2000000-0000-0000-0000-000000000002',
    'a1000000-0000-0000-0000-000000000001',
    'Mercato Wholesale Delivery', 'REF-002',
    'Addis Mercato, Addis Ababa', 9.0100, 38.7350, 'Addis Ababa',
    'Kebede Store',              '+251911100002',
    CURRENT_DATE + 1,
    '09:00', '12:00', 20,
    250.0, 1.5, 10,
    'pending', 'normal'
),

-- Stop 3: Piazza / City Centre
(
    'd3000000-0000-0000-0000-000000000003',
    'a1000000-0000-0000-0000-000000000001',
    'Piazza Retail Delivery',    'REF-003',
    'Piazza, Churchill Avenue, Addis Ababa', 9.0320, 38.7480, 'Addis Ababa',
    'Almaz Shop',                '+251911100003',
    CURRENT_DATE + 1,
    '10:00', '13:00', 15,
    75.0, 0.4, 5,
    'pending', 'normal'
),

-- Stop 4: Kazanchis
(
    'd4000000-0000-0000-0000-000000000004',
    'a1000000-0000-0000-0000-000000000001',
    'Kazanchis Office Supplies',  'REF-004',
    'Kazanchis Business District, Addis Ababa', 9.0200, 38.7600, 'Addis Ababa',
    'Yonas Tesfaye',             '+251911100004',
    CURRENT_DATE + 1,
    '08:30', '11:00', 10,
    40.0, 0.2, 2,
    'pending', 'low'
),

-- Stop 5: CMC Road
(
    'd5000000-0000-0000-0000-000000000005',
    'a1000000-0000-0000-0000-000000000001',
    'CMC Residential Delivery',  'REF-005',
    'CMC Road, Addis Ababa',     9.0560, 38.7830, 'Addis Ababa',
    'Hiwot Alemu',               '+251911100005',
    CURRENT_DATE + 1,
    '11:00', '14:00', 10,
    15.0, 0.1, 1,
    'pending', 'normal'
),

-- Stop 6: Sarbet
(
    'd6000000-0000-0000-0000-000000000006',
    'a1000000-0000-0000-0000-000000000001',
    'Sarbet Supermarket Restock', 'REF-006',
    'Sarbet, Addis Ababa',        8.9950, 38.7560, 'Addis Ababa',
    'Meron Market',              '+251911100006',
    CURRENT_DATE + 1,
    '13:00', '16:00', 25,
    320.0, 2.0, 15,
    'pending', 'high'
),

-- Stop 7: Gerji
(
    'd7000000-0000-0000-0000-000000000007',
    'a1000000-0000-0000-0000-000000000001',
    'Gerji Electronics Shop',    'REF-007',
    'Gerji, Addis Ababa',         9.0070, 38.8100, 'Addis Ababa',
    'Dawit Tadesse',             '+251911100007',
    CURRENT_DATE + 1,
    '10:00', '14:00', 15,
    60.0, 0.5, 4,
    'pending', 'normal'
),

-- Stop 8: Ayat
(
    'd8000000-0000-0000-0000-000000000008',
    'a1000000-0000-0000-0000-000000000001',
    'Ayat Residential Complex',  'REF-008',
    'Ayat, Addis Ababa',          9.0400, 38.8400, 'Addis Ababa',
    'Selam Hailu',               '+251911100008',
    CURRENT_DATE + 1,
    '14:00', '17:00', 10,
    22.0, 0.15, 2,
    'pending', 'low'
)

ON CONFLICT (id) DO NOTHING;

-- ── 5. Demo Route (draft — not yet optimized) ─────────────────────────────────
INSERT INTO routes (
    id, org_id, vehicle_id, driver_id, created_by_id,
    name, status, profile, algorithm,
    scheduled_date, departure_time
) VALUES (
    'e1000000-0000-0000-0000-000000000001',
    'a1000000-0000-0000-0000-000000000001',
    'c1000000-0000-0000-0000-000000000001',   -- Van #1
    'b3000000-0000-0000-0000-000000000003',   -- Driver Solomon
    'b2000000-0000-0000-0000-000000000002',   -- Created by manager Tigist
    'Morning Addis Run — Day 1',
    'draft', 'driving', 'osrm_trip',
    CURRENT_DATE + 1, '07:30'
)
ON CONFLICT (id) DO NOTHING;

-- Attach stops 1-6 to the demo route (sequential, not yet optimized)
INSERT INTO route_stops (id, route_id, job_id, sequence, status)
VALUES
    (gen_random_uuid(), 'e1000000-0000-0000-0000-000000000001', 'd1000000-0000-0000-0000-000000000001', 1, 'pending'),
    (gen_random_uuid(), 'e1000000-0000-0000-0000-000000000001', 'd2000000-0000-0000-0000-000000000002', 2, 'pending'),
    (gen_random_uuid(), 'e1000000-0000-0000-0000-000000000001', 'd3000000-0000-0000-0000-000000000003', 3, 'pending'),
    (gen_random_uuid(), 'e1000000-0000-0000-0000-000000000001', 'd4000000-0000-0000-0000-000000000004', 4, 'pending'),
    (gen_random_uuid(), 'e1000000-0000-0000-0000-000000000001', 'd5000000-0000-0000-0000-000000000005', 5, 'pending'),
    (gen_random_uuid(), 'e1000000-0000-0000-0000-000000000001', 'd6000000-0000-0000-0000-000000000006', 6, 'pending')
ON CONFLICT (route_id, job_id) DO NOTHING;

-- Update job statuses for assigned stops
UPDATE jobs SET status = 'assigned'
WHERE id IN (
    'd1000000-0000-0000-0000-000000000001',
    'd2000000-0000-0000-0000-000000000002',
    'd3000000-0000-0000-0000-000000000003',
    'd4000000-0000-0000-0000-000000000004',
    'd5000000-0000-0000-0000-000000000005',
    'd6000000-0000-0000-0000-000000000006'
);

COMMIT;
