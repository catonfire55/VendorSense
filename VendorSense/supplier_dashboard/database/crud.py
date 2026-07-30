from database.database import SessionLocal
from database.models import Product
from database.models import Vendor
from datetime import datetime
from database.models import VendorProduct
from database.models import PurchaseHistory

def get_session():
    return SessionLocal()


def get_product_by_odoo_id(odoo_id):

    session = get_session()

    try:

        return session.query(Product).filter(
            Product.odoo_product_id == odoo_id
        ).first()

    finally:

        session.close()


def save_product(
    odoo_product_id,
    code,
    name
):

    session = get_session()

    try:

        product = session.query(Product).filter(
            Product.odoo_product_id == odoo_product_id
        ).first()

        if product:

            product.code = code
            product.name = name

        else:

            product = Product(

                odoo_product_id=odoo_product_id,

                code=code,

                name=name

            )

            session.add(product)

        session.commit()

        return product

    finally:

        session.close()

def save_vendor(

    odoo_vendor_id,

    name,

    email,

    phone

):

    session = get_session()

    try:

        vendor = session.query(Vendor).filter(

            Vendor.odoo_vendor_id == odoo_vendor_id

        ).first()

        if vendor:

            vendor.name = name
            vendor.email = email
            vendor.phone = phone

        else:

            vendor = Vendor(

                odoo_vendor_id=odoo_vendor_id,

                name=name,

                email=email,

                phone=phone

            )

            session.add(vendor)

        session.commit()

        return vendor

    finally:

        session.close()

def save_vendor_product(

    product_id,

    vendor_id,

    price,

    lead_time,

    minimum_qty

):

    session = get_session()

    try:

        vp = session.query(VendorProduct).filter(

            VendorProduct.product_id == product_id,

            VendorProduct.vendor_id == vendor_id

        ).first()

        if vp:

            vp.price = price
            vp.lead_time = lead_time
            vp.minimum_qty = minimum_qty
            vp.last_updated = datetime.now()

        else:

            vp = VendorProduct(

                product_id=product_id,

                vendor_id=vendor_id,

                price=price,

                lead_time=lead_time,

                minimum_qty=minimum_qty,

                agent_score=None,

                last_updated=datetime.now()

            )

            session.add(vp)

        session.commit()

        return vp

    finally:

        session.close()

def get_vendor_by_odoo_id(

    odoo_vendor_id

):

    session = get_session()

    try:

        return session.query(Vendor).filter(

            Vendor.odoo_vendor_id == odoo_vendor_id

        ).first()

    finally:

        session.close()

def get_vendor_by_id(vendor_id):

    session = get_session()

    try:

        return session.query(Vendor).filter(
            Vendor.id == vendor_id
        ).first()

    finally:

        session.close()

def get_product_by_odoo_id(

    odoo_product_id

):

    session = get_session()

    try:

        return session.query(Product).filter(

            Product.odoo_product_id == odoo_product_id

        ).first()

    finally:

        session.close()

def get_vendor_product(

    product_id,

    vendor_id

):

    session = get_session()

    try:

        return session.query(VendorProduct).filter(

            VendorProduct.product_id == product_id,

            VendorProduct.vendor_id == vendor_id

        ).first()

    finally:

        session.close()


def get_product_by_name(name):

    session = get_session()

    try:

        return session.query(Product).filter(
            Product.name.ilike(f"%{name}%")
        ).first()

    finally:

        session.close()

def get_vendor_products(product_id):

    session = get_session()

    try:

        return session.query(VendorProduct).filter(
            VendorProduct.product_id == product_id
        ).all()

    finally:

        session.close()

def save_purchase_history(
    vendor_product_id,
    po_number,
    date,
    amount,
    status
):
    session = get_session()

    try:

        existing = session.query(PurchaseHistory).filter(
            PurchaseHistory.vendor_product_id == vendor_product_id,
            PurchaseHistory.po_number == po_number
        ).first()

        if existing:

            existing.date = date
            existing.amount = amount
            existing.status = status

        else:

            po = PurchaseHistory(
                vendor_product_id=vendor_product_id,
                po_number=po_number,
                date=date,
                amount=amount,
                status=status
            )

            session.add(po)

        session.commit()

    finally:
        session.close()

def get_purchase_history(vendor_product_id):

    session = get_session()

    try:

        return session.query(PurchaseHistory).filter(
            PurchaseHistory.vendor_product_id == vendor_product_id
        ).all()

    finally:

        session.close()

def get_products_by_vendor(vendor_id):

    session = get_session()

    try:

        vendor_products = session.query(VendorProduct).filter(
            VendorProduct.vendor_id == vendor_id
        ).all()

        products = []

        for vp in vendor_products:

            product = session.query(Product).filter(
                Product.id == vp.product_id
            ).first()

            if product:

                products.append({

                    "name": product.name,

                    "code": product.code

                })

        return products

    finally:

        session.close()

def update_agent_score(vendor_product_id, score):

    session = get_session()

    try:

        vp = session.query(VendorProduct).filter(
            VendorProduct.id == vendor_product_id
        ).first()

        if vp:
            vp.agent_score = round(score, 2)
            session.commit()

    finally:
        session.close()