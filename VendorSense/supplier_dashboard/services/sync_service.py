from services.odoo_service import odoo_service
from database import crud


class SyncService:

    def sync_product(self, product_name):

        products = odoo_service.search_product(product_name)

        if len(products) == 0:
            return False

        product = products[0]

        # -----------------------------
        # Save Product
        # -----------------------------

        db_product = crud.save_product(

            odoo_product_id=product.id,

            code=product.default_code or "",

            name=product.name

        )

        supplier_infos = odoo_service.get_supplier_infos(
            product.product_tmpl_id.id
        )

        for supplier in supplier_infos:

            partner = odoo_service.get_vendor(
                supplier.partner_id.id
            )

            crud.save_vendor(

                odoo_vendor_id=partner.id,

                name=partner.name,

                email=partner.email or "",

                phone=partner.phone or ""

            )
            
            db_vendor = crud.get_vendor_by_odoo_id(

                partner.id

            )

            db_product = crud.get_product_by_odoo_id(

                product.id

            )

            crud.save_vendor_product(

                product_id=db_product.id,

                vendor_id=db_vendor.id,

                price=supplier.price,

                lead_time=supplier.delay,

                minimum_qty=supplier.min_qty

            )
            vendor_product = crud.get_vendor_product(

                db_product.id,

                db_vendor.id

            )

            purchase_orders = odoo_service.get_purchase_orders_for_product(

                partner.id,

                product.id

            )

            for po in purchase_orders:

                crud.save_purchase_history(

                    vendor_product_id=vendor_product.id,

                    po_number=po["number"],

                    date=po["date"],

                    amount=po["amount"],

                    status=po["status"]

                )

        return True


sync_service = SyncService()