"""
Models package — import all models here so Alembic and
Base.metadata.create_all() can discover them.
"""
from app.models.organization import Organization      # noqa: F401
from app.models.user import User                      # noqa: F401
from app.models.vehicle import Vehicle                # noqa: F401
from app.models.job import Job                        # noqa: F401
from app.models.route import Route, RouteStop         # noqa: F401
from app.models.optimization_job import OptimizationJob  # noqa: F401
