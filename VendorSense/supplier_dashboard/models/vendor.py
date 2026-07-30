from dataclasses import dataclass, field


@dataclass
class VendorProfile:

    vendor_id: int
    vendor_name: str

    email: str
    phone: str

    price: float
    lead_time: int
    minimum_qty: float

    products: list = field(default_factory=list)

    purchase_orders: list = field(default_factory=list)

    agent_score: float | None = None