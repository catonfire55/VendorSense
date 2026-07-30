from database import crud


class DashboardService:

    def search_product(self, product_name):

        product = crud.get_product_by_name(product_name)

        if not product:
            return []

        vendor_products = crud.get_vendor_products(product.id)

        dashboard = []

        for vp in vendor_products:

            vendor = crud.get_vendor_by_id(vp.vendor_id)
            purchase_history = crud.get_purchase_history(vp.id)
            products = crud.get_products_by_vendor(vendor.id)

            po_list = []

            for po in purchase_history:

                po_list.append({

                    "number": po.po_number,

                    "status": po.status,

                    "amount": po.amount,

                    "date": po.date

                })

            dashboard.append({

                "vendor_id": vendor.id,

                "vendor_name": vendor.name,

                "email": vendor.email,

                "phone": vendor.phone,

                "price": vp.price,

                "lead_time": vp.lead_time,

                "minimum_qty": vp.minimum_qty,

                "agent_score": vp.agent_score if vp.agent_score is not None else "--",
                "purchase_orders": po_list,
                "products": products,

            })

        return dashboard


dashboard_service = DashboardService()