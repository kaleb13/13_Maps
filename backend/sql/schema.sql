-- =============================================================================
-- RouteOpt — PostgreSQL Schema DDL
-- Route Optimization SaaS — Multi-tenant schema
-- =============================================================================
-- Run order matters: enums → tables (parent first, then children)
-- =============================================================================

-- ── Extensions ────────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- trigram search on addresses/names

-- ── Enums ─────────────────────────────────────────────────────────────────────
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('admin', 'manager', 'driver');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE vehicle_type AS ENUM ('car', 'van', 'truck', 'motorcycle', 'bicycle');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE vehicle_status AS ENUM ('available', 'on_route', 'maintenance', 'retired');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE job_status AS ENUM ('pending', 'assigned', 'in_transit', 'completed', 'failed', 'cancelled');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE job_priority AS ENUM ('low', 'normal', 'high', 'urgent');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE route_status AS ENUM ('draft', 'optimized', 'dispatched', 'in_progress', 'completed', 'cancelled');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE stop_status AS ENUM ('pending', 'arrived', 'completed', 'skipped');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- =============================================================================
-- TABLE: organizations
-- Root entity for multi-tenancy. All data is scoped to an organization.
-- =============================================================================
CREATE TABLE IF NOT EXISTS organizations (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(200) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    plan        VARCHAR(50)  NOT NULL DEFAULT 'free',     -- free | pro | enterprise
    address     TEXT,
    phone       VARCHAR(30),
    email       VARCHAR(255),
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_organizations_slug ON organizations (slug);

COMMENT ON TABLE  organizations IS 'Multi-tenant root. Every resource belongs to one organization.';
COMMENT ON COLUMN organizations.slug IS 'URL-safe unique identifier, e.g. "acme-logistics"';
COMMENT ON COLUMN organizations.plan IS 'Subscription tier: free | pro | enterprise';

-- =============================================================================
-- TABLE: users
-- Platform users scoped to an organization with role-based access.
-- =============================================================================
CREATE TABLE IF NOT EXISTS users (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id           UUID        NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    email            VARCHAR(255) NOT NULL UNIQUE,
    hashed_password  VARCHAR     NOT NULL,
    full_name        VARCHAR(150),
    role             user_role   NOT NULL DEFAULT 'driver',
    phone            VARCHAR(30),
    avatar_url       VARCHAR(500),
    is_active        BOOLEAN     NOT NULL DEFAULT TRUE,
    is_superuser     BOOLEAN     NOT NULL DEFAULT FALSE,  -- platform-level admin
    last_login_at    TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_org_id ON users (org_id);
CREATE INDEX IF NOT EXISTS idx_users_email  ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_role   ON users (org_id, role);

COMMENT ON TABLE  users IS 'Platform users. Role governs access within their organization.';
COMMENT ON COLUMN users.role IS 'admin: full org access | manager: routes/jobs/vehicles | driver: own routes only';
COMMENT ON COLUMN users.is_superuser IS 'Platform-wide admin, not scoped to any organization.';

-- =============================================================================
-- TABLE: vehicles
-- Fleet resources assigned to an organization and optionally to a driver.
-- =============================================================================
CREATE TABLE IF NOT EXISTS vehicles (
    id                  UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id              UUID          NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    driver_id           UUID          REFERENCES users (id) ON DELETE SET NULL,
    name                VARCHAR(150)  NOT NULL,
    license_plate       VARCHAR(30),
    vehicle_type        vehicle_type  NOT NULL DEFAULT 'van',
    status              vehicle_status NOT NULL DEFAULT 'available',
    capacity_weight_kg  FLOAT,
    capacity_volume_m3  FLOAT,
    max_stops           INTEGER,
    fuel_type           VARCHAR(50),
    speed_profile       VARCHAR(50)   NOT NULL DEFAULT 'driving',
    notes               TEXT,
    is_active           BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_vehicles_org_id    ON vehicles (org_id);
CREATE INDEX IF NOT EXISTS idx_vehicles_driver_id ON vehicles (driver_id);
CREATE INDEX IF NOT EXISTS idx_vehicles_status    ON vehicles (org_id, status);

COMMENT ON TABLE  vehicles IS 'Fleet vehicles with capacity and assignment constraints.';
COMMENT ON COLUMN vehicles.capacity_weight_kg IS 'Maximum payload in kilograms.';
COMMENT ON COLUMN vehicles.capacity_volume_m3 IS 'Maximum payload volume in cubic metres.';

-- =============================================================================
-- TABLE: jobs
-- Delivery points / tasks. Each job is one stop in an optimized route.
-- =============================================================================
CREATE TABLE IF NOT EXISTS jobs (
    id                UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id            UUID          NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    title             VARCHAR(255)  NOT NULL,
    reference         VARCHAR(100),                 -- external order / waybill number
    address           TEXT          NOT NULL,
    latitude          FLOAT         NOT NULL,
    longitude         FLOAT         NOT NULL,
    city              VARCHAR(100),
    postal_code       VARCHAR(20),
    contact_name      VARCHAR(150),
    contact_phone     VARCHAR(30),
    contact_email     VARCHAR(255),
    scheduled_date    DATE,
    time_window_start TIME,                         -- earliest acceptable arrival
    time_window_end   TIME,                         -- latest acceptable arrival
    service_time_min  INTEGER       NOT NULL DEFAULT 10,
    weight_kg         FLOAT         NOT NULL DEFAULT 0,
    volume_m3         FLOAT         NOT NULL DEFAULT 0,
    quantity          INTEGER       NOT NULL DEFAULT 1,
    status            job_status    NOT NULL DEFAULT 'pending',
    priority          job_priority  NOT NULL DEFAULT 'normal',
    notes             TEXT,
    created_at        TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_jobs_org_id    ON jobs (org_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status    ON jobs (org_id, status);
CREATE INDEX IF NOT EXISTS idx_jobs_priority  ON jobs (org_id, priority);
CREATE INDEX IF NOT EXISTS idx_jobs_date      ON jobs (org_id, scheduled_date);
CREATE INDEX IF NOT EXISTS idx_jobs_reference ON jobs (org_id, reference);
-- GiST index for geo proximity queries (requires PostGIS; optional)
-- CREATE INDEX idx_jobs_geo ON jobs USING GIST (ST_MakePoint(longitude, latitude));

COMMENT ON TABLE  jobs IS 'Delivery tasks / stops to be included in optimized routes.';
COMMENT ON COLUMN jobs.time_window_start IS 'Earliest the driver may arrive (hard constraint for OSRM-VRP).';
COMMENT ON COLUMN jobs.service_time_min  IS 'Minutes to spend at the stop (unloading, signature, etc.)';

-- =============================================================================
-- TABLE: routes
-- Optimized route plan for one vehicle on one day.
-- =============================================================================
CREATE TABLE IF NOT EXISTS routes (
    id                UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id            UUID          NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    vehicle_id        UUID          REFERENCES vehicles (id) ON DELETE SET NULL,
    driver_id         UUID          REFERENCES users    (id) ON DELETE SET NULL,
    created_by_id     UUID          REFERENCES users    (id) ON DELETE SET NULL,
    name              VARCHAR(255)  NOT NULL,
    status            route_status  NOT NULL DEFAULT 'draft',
    profile           VARCHAR(50)   NOT NULL DEFAULT 'driving',
    algorithm         VARCHAR(100)  NOT NULL DEFAULT 'osrm_trip',
    scheduled_date    DATE,
    departure_time    TIME,
    total_distance_m  FLOAT,
    total_duration_s  FLOAT,
    total_weight_kg   FLOAT,
    total_volume_m3   FLOAT,
    stop_count        INTEGER,
    osrm_response     JSONB,                        -- full raw OSRM payload
    notes             TEXT,
    completed_at      TIMESTAMPTZ,
    created_at        TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_routes_org_id    ON routes (org_id);
CREATE INDEX IF NOT EXISTS idx_routes_vehicle   ON routes (vehicle_id);
CREATE INDEX IF NOT EXISTS idx_routes_driver    ON routes (driver_id);
CREATE INDEX IF NOT EXISTS idx_routes_status    ON routes (org_id, status);
CREATE INDEX IF NOT EXISTS idx_routes_date      ON routes (org_id, scheduled_date);

COMMENT ON TABLE  routes IS 'Optimized route plan: header record for one vehicle run.';
COMMENT ON COLUMN routes.osrm_response IS 'Full raw JSON from OSRM /trip or /route endpoint.';

-- =============================================================================
-- TABLE: route_stops
-- Ordered stops within a route, each pointing to a Job.
-- =============================================================================
CREATE TABLE IF NOT EXISTS route_stops (
    id                UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    route_id          UUID         NOT NULL REFERENCES routes (id) ON DELETE CASCADE,
    job_id            UUID         NOT NULL REFERENCES jobs   (id) ON DELETE RESTRICT,
    sequence          INTEGER      NOT NULL,
    estimated_arrival TIME,
    actual_arrival    TIMESTAMPTZ,
    actual_departure  TIMESTAMPTZ,
    status            stop_status  NOT NULL DEFAULT 'pending',
    driver_notes      TEXT,
    UNIQUE (route_id, job_id),                      -- a job appears once per route
    UNIQUE (route_id, sequence)                     -- each sequence position is unique
);

CREATE INDEX IF NOT EXISTS idx_route_stops_route ON route_stops (route_id);
CREATE INDEX IF NOT EXISTS idx_route_stops_job   ON route_stops (job_id);

COMMENT ON TABLE  route_stops IS 'Ordered stops within a route. Junction between routes and jobs.';

-- =============================================================================
-- TABLE: optimization_jobs
-- Async task queue for OSRM optimization requests.
-- =============================================================================
CREATE TABLE IF NOT EXISTS optimization_jobs (
    id                UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id            UUID         NOT NULL REFERENCES organizations (id) ON DELETE CASCADE,
    owner_id          UUID         NOT NULL REFERENCES users         (id) ON DELETE CASCADE,
    route_id          UUID         REFERENCES routes (id) ON DELETE SET NULL,
    status            VARCHAR(50)  NOT NULL DEFAULT 'queued',
    algorithm         VARCHAR(100) NOT NULL DEFAULT 'osrm_trip',
    profile           VARCHAR(50)  NOT NULL DEFAULT 'driving',
    total_distance_m  FLOAT,
    total_duration_s  FLOAT,
    result            JSONB,
    error_message     TEXT,
    created_at        TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    completed_at      TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_opt_jobs_org    ON optimization_jobs (org_id);
CREATE INDEX IF NOT EXISTS idx_opt_jobs_owner  ON optimization_jobs (owner_id);
CREATE INDEX IF NOT EXISTS idx_opt_jobs_status ON optimization_jobs (status);

-- =============================================================================
-- FUNCTION: auto-update updated_at on row change
-- =============================================================================
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to every table that has updated_at
DO $$ DECLARE
    t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY[
        'organizations', 'users', 'vehicles', 'jobs', 'routes'
    ] LOOP
        EXECUTE format(
            'DROP TRIGGER IF EXISTS trg_updated_at ON %I;
             CREATE TRIGGER trg_updated_at
             BEFORE UPDATE ON %I
             FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();',
            t, t
        );
    END LOOP;
END $$;
