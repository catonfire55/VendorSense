from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from database.database import Base


# ==========================
# Products
# ==========================

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    odoo_product_id = Column(Integer, unique=True, nullable=False)

    code = Column(String)

    name = Column(String)

    vendors = relationship(
        "VendorProduct",
        back_populates="product",
        cascade="all, delete-orphan"
    )


# ==========================
# Vendors
# ==========================

class Vendor(Base):

    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True)

    odoo_vendor_id = Column(Integer, unique=True, nullable=False)

    name = Column(String)

    email = Column(String)

    phone = Column(String)

    products = relationship(
        "VendorProduct",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )


# ==========================
# VendorProduct
# ==========================

class VendorProduct(Base):

    __tablename__ = "vendor_products"

    id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    vendor_id = Column(
        Integer,
        ForeignKey("vendors.id"),
        nullable=False
    )

    price = Column(Float)

    lead_time = Column(Integer)

    minimum_qty = Column(Float)

    agent_score = Column(Float)

    last_updated = Column(DateTime)

    product = relationship(
        "Product",
        back_populates="vendors"
    )

    vendor = relationship(
        "Vendor",
        back_populates="products"
    )

    purchase_history = relationship(
        "PurchaseHistory",
        back_populates="vendor_product",
        cascade="all, delete-orphan"
    )

    score_metrics = relationship(
        "ScoreMetric",
        back_populates="vendor_product",
        cascade="all, delete-orphan"
    )


# ==========================
# Purchase History
# ==========================

class PurchaseHistory(Base):

    __tablename__ = "purchase_history"

    id = Column(Integer, primary_key=True)

    vendor_product_id = Column(
        Integer,
        ForeignKey("vendor_products.id")
    )

    po_number = Column(String)

    date = Column(DateTime)

    amount = Column(Float)

    status = Column(String)

    vendor_product = relationship(
        "VendorProduct",
        back_populates="purchase_history"
    )


# ==========================
# Score Metrics
# ==========================

class ScoreMetric(Base):

    __tablename__ = "score_metrics"

    id = Column(Integer, primary_key=True)

    vendor_product_id = Column(
        Integer,
        ForeignKey("vendor_products.id")
    )

    metric = Column(String)

    raw_value = Column(Float)

    normalized_value = Column(Float)

    weight = Column(Float)

    weighted_score = Column(Float)

    vendor_product = relationship(
        "VendorProduct",
        back_populates="score_metrics"
    )