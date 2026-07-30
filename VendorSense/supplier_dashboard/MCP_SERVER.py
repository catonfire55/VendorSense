from mcp.server.fastmcp import FastMCP

from services.sync_service import sync_service
from services.dashboard_service import dashboard_service
from agent.SPO_AGENT import supplier_agent

mcp = FastMCP("Supplier Performance Optimizer")


@mcp.tool()
def recommend_supplier(product_name: str):

    # Refresh PostgreSQL from Odoo
    sync_service.sync_product(product_name)

    # Calculate scores and update DB
    supplier_agent.run(product_name)

    # Read updated vendor packets
    vendors = dashboard_service.search_product(product_name)

    return {
        "product": product_name,
        "vendor_count": len(vendors),
        "vendors": vendors
    }


if __name__ == "__main__":
    mcp.run()