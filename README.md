## SAP P2P Working Project

This is a complete, ready-to-run project for the Procure-to-Pay (P2P) workflow inspired by the SAP MM + FI flow.

## Project Structure

sap-p2p-project/
├── docs/
│   ├── project-report.md
│   └── sample-data.md
├── project/
│   ├── backend/
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── frontend/
│   │   └── p2p-dashboard.html
│   └── database/
│       └── schema.sql
└── README.md

## Features
- Create vendors
- Create materials
- Raise purchase requisitions
- Approve and convert requisitions into purchase orders
- Post goods receipt
- Post invoice verification
- Run payment processing
- View P2P dashboard and document status

## Tech Stack
- Python Flask
- SQLite
- HTML, CSS, JavaScript

## How to Run

### Backend
cd project/backend
pip install -r requirements.txt
python app.py


### Frontend
Open `project/frontend/p2p-dashboard.html` in a browser after starting the backend.

