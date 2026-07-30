from database import crud


class SupplierAgent:

    PRICE_WEIGHT = 0.40
    LEADTIME_WEIGHT = 0.30
    HISTORY_WEIGHT = 0.20
    QUALITY_WEIGHT = 0.10

    QUALITY_SCORE = 50


    def normalize_inverse(self, values):

        if len(values) == 1:
            return [100]

        mn = min(values)
        mx = max(values)

        if mx == mn:
            return [100 for _ in values]

        scores = []

        for v in values:

            score = ((mx - v) / (mx - mn)) * 100

            scores.append(score)

        return scores


    def normalize_direct(self, values):

        if len(values) == 1:
            return [100]

        mn = min(values)
        mx = max(values)

        if mx == mn:
            return [100 for _ in values]

        scores = []

        for v in values:

            score = ((v - mn) / (mx - mn)) * 100

            scores.append(score)

        return scores


    def run(self, product_name):

        product = crud.get_product_by_name(product_name)

        if product is None:
            return

        vendor_products = crud.get_vendor_products(product.id)

        if len(vendor_products) == 0:
            return

        prices = []
        lead_times = []
        histories = []

        for vp in vendor_products:

            prices.append(vp.price)

            lead_times.append(vp.lead_time)

            history = crud.get_purchase_history(vp.id)

            histories.append(len(history))

        price_scores = self.normalize_inverse(prices)

        lead_scores = self.normalize_inverse(lead_times)

        history_scores = self.normalize_direct(histories)

        for i, vp in enumerate(vendor_products):

            final_score = (

                price_scores[i] * self.PRICE_WEIGHT +

                lead_scores[i] * self.LEADTIME_WEIGHT +

                history_scores[i] * self.HISTORY_WEIGHT +

                self.QUALITY_SCORE * self.QUALITY_WEIGHT

            )

            crud.update_agent_score(

                vp.id,

                final_score

            )


supplier_agent = SupplierAgent()