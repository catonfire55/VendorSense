from flask import Flask, render_template, request

from services.odoo_service import odoo_service
from models.vendor import VendorProfile
from services.sync_service import sync_service
from services.dashboard_service import dashboard_service
from agent.SPO_AGENT import supplier_agent

from config import SECRET_KEY

app = Flask(__name__)

app.secret_key = SECRET_KEY


@app.route("/")
def home():

    return render_template(
        "index.html",
        vendors=[],
        searched=False
    )


@app.route("/search")
def search():

    product_name = request.args.get("product")

    sync_service.sync_product(product_name)
    
    #supplier_agent.run(product_name)

    vendors = dashboard_service.search_product(product_name)

    return render_template(

        "index.html",

        vendors=vendors,

        searched=True,

        product_name=product_name

    )


if __name__ == "__main__":
    app.run(debug=True)