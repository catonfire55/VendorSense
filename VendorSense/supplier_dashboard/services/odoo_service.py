import odoorpc

from config import (
    ODOO_HOST,
    ODOO_PORT,
    ODOO_DATABASE,
    ODOO_USERNAME,
    ODOO_PASSWORD,
)


class OdooService:

    def __init__(self):
        self.odoo = None

    def connect(self):

        if self.odoo is not None:
            return

        self.odoo = odoorpc.ODOO(
            ODOO_HOST,
            port=ODOO_PORT
        )

        self.odoo.login(
            ODOO_DATABASE,
            ODOO_USERNAME,
            ODOO_PASSWORD
        )

    def search_product(self, product_name):

        self.connect()

        Product = self.odoo.env["product.product"]

        ids = Product.search([
            ("name", "ilike", product_name)
        ])

        return Product.browse(ids)

    def get_supplier_infos(self, product_template_id):

        self.connect()

        SupplierInfo = self.odoo.env["product.supplierinfo"]

        ids = SupplierInfo.search([
            ("product_tmpl_id", "=", product_template_id)
        ])

        return SupplierInfo.browse(ids)

    def get_vendor(self, vendor_id):

        self.connect()

        Partner = self.odoo.env["res.partner"]

        return Partner.browse(vendor_id)

    def get_purchase_orders_for_product(

        self,

        vendor_id,

        product_id

    ):

        self.connect()

        PurchaseOrder = self.odoo.env["purchase.order"]

        PurchaseOrderLine = self.odoo.env["purchase.order.line"]

        po_ids = PurchaseOrder.search([

            ("partner_id", "=", vendor_id)

        ])

        purchase_orders = []

        for po in PurchaseOrder.browse(po_ids):

            line_ids = PurchaseOrderLine.search([

                ("order_id", "=", po.id),

                ("product_id", "=", product_id)

            ])

            if not line_ids:
                continue

            purchase_orders.append({

                "number": po.name,

                "date": po.date_order,

                "amount": po.amount_total,

                "status": po.state

            })

        return purchase_orders
    
    def get_vendor_products(self, vendor_id):

        self.connect()

        SupplierInfo = self.odoo.env["product.supplierinfo"]

        supplier_ids = SupplierInfo.search([
            ("partner_id", "=", vendor_id)
        ])

        supplier_infos = SupplierInfo.browse(supplier_ids)

        products = []

        for supplier in supplier_infos:

            product = supplier.product_tmpl_id

            products.append({
                "id": product.id,
                "name": product.name,
                "code": product.default_code or "-"
            })

        return products

    def get_purchase_orders(self, vendor_id):

        self.connect()

        PurchaseOrder = self.odoo.env["purchase.order"]

        ids = PurchaseOrder.search([
            ("partner_id", "=", vendor_id)
        ])

        orders = PurchaseOrder.browse(ids)

        purchase_orders = []

        for po in orders:

            purchase_orders.append({

                "number": po.name,

                "date": str(po.date_order),

                "state": po.state,

                "amount": po.amount_total

            })

        return purchase_orders

odoo_service = OdooService()