from database.database import Base, engine

# Import all table classes so SQLAlchemy knows about them
from database.models import (
    Product,
    Vendor,
    VendorProduct,
    PurchaseHistory,
    ScoreMetric,
)

Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")