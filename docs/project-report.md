# Project Report: Procure-to-Pay (P2P) Working Project

## Title
SAP Procure-to-Pay (P2P) Process Simulation using Python Flask and SQLite

## Problem Statement
Organizations need a structured procurement cycle to manage material requests, vendor selection, purchase ordering, goods receipt, invoice verification, and payment settlement. This project simulates the full P2P business flow in a working software application.

## Solution and Features
The project provides a web-based academic prototype that models the standard procurement cycle:
- Vendor master creation
- Material master creation
- Purchase requisition creation
- Purchase order generation from PR
- Goods receipt posting
- Invoice verification
- Payment processing
- Dashboard-based status tracking

## Tech Stack
- Python
- Flask
- Flask-CORS
- SQLite
- HTML
- CSS
- JavaScript

## Unique Points
- Covers end-to-end P2P lifecycle in one working system
- Simple academic implementation that is easy to demonstrate viva-wise
- Includes backend APIs, database schema, and frontend dashboard
- Maps well to SAP MM + FI integration concepts

## Future Improvements
- Add approval workflow and user login
- Add GR/IR accounting simulation
- Add PDF invoice printout
- Add vendor quotation comparison
- Deploy on Render or Railway and host frontend on GitHub Pages

## Suggested Screenshots
1. Dashboard home page
2. Vendor and material creation
3. Purchase requisition screen
4. Purchase order generation
5. Goods receipt and invoice verification
6. Payment completion and final document flow