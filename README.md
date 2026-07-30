VendorSense

AI-Assisted Supplier Performance Optimizer for Odoo ERP using MCP

VendorSense is an AI-assisted procurement support system that integrates with Odoo ERP to evaluate suppliers based on procurement metrics such as price, lead time, and purchase history.



Instead of allowing an LLM to make procurement decisions, VendorSense follows a deterministic scoring approach where a dedicated Supplier Agent calculates supplier scores and the LLM only explains the recommendation in natural language.



Features

Odoo ERP Integration using OdooRPC

PostgreSQL Analytics Database

Supplier Performance Scoring Engine

MCP (Model Context Protocol) Server

Flask Dashboard

AI-assisted Recommendation Explanation

Modular & Extensible Architecture

Architecture

                 User

                   │

                   ▼

                LLM Client

                   │

                   ▼

              MCP Server

         ┌─────────┴─────────┐

         ▼                   ▼

   Sync Service        Supplier Agent

         │                   │

         └─────────┬─────────┘

                   ▼

             PostgreSQL

                   ▲

                   │

              Dashboard

                   ▲

                   │

               Odoo ERP

Project Workflow

User Request



        │



        ▼



MCP receives Product Name



        │



        ▼



Sync Service fetches latest data from Odoo



        │



        ▼



Store data in PostgreSQL



        │



        ▼



Supplier Agent calculates scores



        │



        ▼



Update PostgreSQL



        │



        ▼



Dashboard reads updated data



        │



        ▼



MCP returns Vendor Packets



        │



        ▼



LLM explains recommendation

Supplier Scoring

Current scoring metrics:



Metric	Weight

Price	40%

Lead Time	30%

Purchase History	20%

Quality (Placeholder)	10%

Current implementation uses:



Supplier Price

Lead Time

Purchase Order History

Quality is currently implemented as a placeholder value and can later be replaced with inspection or vendor quality metrics.



Technologies Used

Backend

Python

Flask

SQLAlchemy

PostgreSQL

OdooRPC

FastMCP

Database

PostgreSQL

ERP

Odoo 19

Required Python Libraries

Install all dependencies:



pip install flask

pip install sqlalchemy

pip install psycopg2-binary

pip install odoorpc

pip install fastmcp

pip install python-dotenv

Installation Guide

Step 1

Clone the repository



git clone https://github.com/<your_username>/VendorSense.git



cd VendorSense

Step 2

Create a virtual environment



python -m venv .venv

Activate it



Windows

.venv\Scripts\activate

Linux / macOS

source .venv/bin/activate

Step 3

Install dependencies



PostgreSQL Setup

Create a PostgreSQL database.



Example



Database Name:

vendorsense

Update your database connection string inside



database/database.py

Example



DATABASE_URL = "postgresql://postgres:password@localhost/vendorsense"

Create Database Tables

Run



python create_tables.py

This creates



Products

Vendors

VendorProducts

PurchaseHistory

Configure Odoo

Open



config.py

Update the following credentials



ODOO_URL = "http://localhost:8069"



ODOO_DATABASE = "your_database"



ODOO_USERNAME = "admin"



ODOO_PASSWORD = "password"

Run Dashboard

Navigate to



supplier_dashboard/

Run



python app.py

Dashboard will be available at



http://127.0.0.1:5000

Run MCP Server

From the project root



python final_mcp_server.py

The MCP server will expose the supplier recommendation tool for compatible LLM clients.



How the System Works

Dashboard Search

Search Product



↓



Sync latest data from Odoo



↓



Store in PostgreSQL



↓



Run Supplier Agent



↓



Update Scores



↓



Display Dashboard

MCP Request

LLM



↓



MCP Tool



↓



Sync Service



↓



Supplier Agent



↓



Dashboard Service



↓



Vendor Packets



↓



LLM Explanation

Project Structure

VendorSense/



│



├── supplier_dashboard/



│   ├── app.py



│   ├── templates/



│   ├── services/



│   ├── database/



│   └── agent/



│



├── final_mcp_server.py



├── requirements.txt



├── README.md



└── config.py

Future Improvements

Vendor Quality Integration

Delivery Reliability Score

Supplier Rating Prediction

Machine Learning-based Supplier Ranking

Interactive Analytics Dashboard

Multi-ERP Support

Docker Deployment

Authentication & Role-Based Access

Disclaimer

This project was developed as an internship project to demonstrate the integration of ERP systems, AI-assisted procurement, deterministic supplier scoring, and Model Context Protocol (MCP). Any credentials, URLs, or sample data should be replaced with your own environment-specific configurations before deployment.
