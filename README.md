## SAP P2P Working Project

This is a ready-to-run project that highlights the Procure-to-Pay (P2P) workflow inspired by the SAP MM + FI flow.

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
<img width="639" height="820" alt="Screenshot 2026-04-19 223615" src="https://github.com/user-attachments/assets/904e16e9-d4ae-43c7-a1ba-668e48a907ef" />

<img width="1889" height="886" alt="Screenshot 2026-04-19 234325" src="https://github.com/user-attachments/assets/5b89ef76-3a64-45d3-8c45-fec137810a77" />




