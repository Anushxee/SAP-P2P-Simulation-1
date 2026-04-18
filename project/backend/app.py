from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'
CORS(app)

DB_PATH = Path(__file__).resolve().parent.parent / 'database' / 'p2p.db'
SCHEMA_PATH = Path(__file__).resolve().parent.parent / 'database' / 'schema.sql'


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()

    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) AS c FROM vendors')
    if cur.fetchone()['c'] == 0:
        cur.execute(
            "INSERT INTO vendors (vendor_code, vendor_name, city, payment_terms) VALUES (?, ?, ?, ?)",
            ('V1001', 'ABC Supplies', 'Bengaluru', '30 Days')
        )
        cur.execute(
            "INSERT INTO materials (material_code, material_name, uom, price) VALUES (?, ?, ?, ?)",
            ('M1001', 'Laptop Battery', 'EA', 2500.00)
        )
        conn.commit()
    conn.close()


def doc_no(prefix):
    return f"{prefix}{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}"

@app.route('/')
def home():
    return send_from_directory(FRONTEND_DIR, 'p2p-dashboard.html')

@app.route('/api/init', methods=['POST'])
def api_init():
    init_db()
    return jsonify({'message': 'Database initialized successfully'})


@app.route('/api/vendors', methods=['GET', 'POST'])
def vendors():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.json
        cur.execute(
            'INSERT INTO vendors (vendor_code, vendor_name, city, payment_terms) VALUES (?, ?, ?, ?)',
            (
                data['vendor_code'],
                data['vendor_name'],
                data.get('city', ''),
                data.get('payment_terms', '30 Days')
            )
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Vendor created'})

    rows = [dict(r) for r in cur.execute('SELECT * FROM vendors ORDER BY id DESC').fetchall()]
    conn.close()
    return jsonify(rows)


@app.route('/api/materials', methods=['GET', 'POST'])
def materials():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.json
        cur.execute(
            'INSERT INTO materials (material_code, material_name, uom, price) VALUES (?, ?, ?, ?)',
            (
                data['material_code'],
                data['material_name'],
                data['uom'],
                data['price']
            )
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Material created'})

    rows = [dict(r) for r in cur.execute('SELECT * FROM materials ORDER BY id DESC').fetchall()]
    conn.close()
    return jsonify(rows)


@app.route('/api/pr', methods=['GET', 'POST'])
def prs():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.json
        number = doc_no('PR')
        cur.execute(
            'INSERT INTO purchase_requisitions (pr_number, material_id, quantity, requested_by, status) VALUES (?, ?, ?, ?, ?)',
            (
                number,
                data['material_id'],
                data['quantity'],
                data['requested_by'],
                'CREATED'
            )
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Purchase Requisition created', 'pr_number': number})

    rows = [
        dict(r) for r in cur.execute(
            '''
            SELECT pr.id, pr.pr_number, m.material_name, pr.quantity, pr.requested_by, pr.status, pr.created_at
            FROM purchase_requisitions pr
            JOIN materials m ON pr.material_id = m.id
            ORDER BY pr.id DESC
            '''
        ).fetchall()
    ]
    conn.close()
    return jsonify(rows)


@app.route('/api/po', methods=['GET', 'POST'])
def pos():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.json
        pr = cur.execute(
            'SELECT * FROM purchase_requisitions WHERE id = ?',
            (data['pr_id'],)
        ).fetchone()

        if not pr:
            conn.close()
            return jsonify({'error': 'PR not found'}), 404

        number = doc_no('PO')
        cur.execute(
            'INSERT INTO purchase_orders (po_number, pr_id, vendor_id, status) VALUES (?, ?, ?, ?)',
            (
                number,
                data['pr_id'],
                data['vendor_id'],
                'APPROVED'
            )
        )
        cur.execute(
            'UPDATE purchase_requisitions SET status = ? WHERE id = ?',
            ('CONVERTED_TO_PO', data['pr_id'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Purchase Order created', 'po_number': number})

    rows = [
        dict(r) for r in cur.execute(
            '''
            SELECT po.id, po.po_number, pr.pr_number, v.vendor_name, po.status, po.created_at
            FROM purchase_orders po
            JOIN purchase_requisitions pr ON po.pr_id = pr.id
            JOIN vendors v ON po.vendor_id = v.id
            ORDER BY po.id DESC
            '''
        ).fetchall()
    ]
    conn.close()
    return jsonify(rows)


@app.route('/api/gr', methods=['GET', 'POST'])
def grs():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.json
        po = cur.execute(
            'SELECT * FROM purchase_orders WHERE id = ?',
            (data['po_id'],)
        ).fetchone()

        if not po:
            conn.close()
            return jsonify({'error': 'PO not found'}), 404

        number = doc_no('GR')
        cur.execute(
            'INSERT INTO goods_receipts (gr_number, po_id, quantity_received, status) VALUES (?, ?, ?, ?)',
            (
                number,
                data['po_id'],
                data['quantity_received'],
                'POSTED'
            )
        )
        cur.execute(
            'UPDATE purchase_orders SET status = ? WHERE id = ?',
            ('GOODS_RECEIVED', data['po_id'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Goods Receipt posted', 'gr_number': number})

    rows = [
        dict(r) for r in cur.execute(
            '''
            SELECT gr.id, gr.gr_number, po.po_number, gr.quantity_received, gr.status, gr.created_at
            FROM goods_receipts gr
            JOIN purchase_orders po ON gr.po_id = po.id
            ORDER BY gr.id DESC
            '''
        ).fetchall()
    ]
    conn.close()
    return jsonify(rows)


@app.route('/api/invoice', methods=['GET', 'POST'])
def invoices():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.json
        po = cur.execute(
            '''
            SELECT po.id, pr.material_id, pr.quantity, m.price
            FROM purchase_orders po
            JOIN purchase_requisitions pr ON po.pr_id = pr.id
            JOIN materials m ON pr.material_id = m.id
            WHERE po.id = ?
            ''',
            (data['po_id'],)
        ).fetchone()

        if not po:
            conn.close()
            return jsonify({'error': 'PO not found'}), 404

        amount = float(po['quantity']) * float(po['price'])
        number = doc_no('IV')

        cur.execute(
            'INSERT INTO invoices (invoice_number, po_id, amount, status) VALUES (?, ?, ?, ?)',
            (
                number,
                data['po_id'],
                amount,
                'VERIFIED'
            )
        )
        cur.execute(
            'UPDATE purchase_orders SET status = ? WHERE id = ?',
            ('INVOICED', data['po_id'])
        )
        conn.commit()
        conn.close()
        return jsonify({
            'message': 'Invoice verified',
            'invoice_number': number,
            'amount': amount
        })

    rows = [
        dict(r) for r in cur.execute(
            '''
            SELECT i.id, i.invoice_number, po.po_number, i.amount, i.status, i.created_at
            FROM invoices i
            JOIN purchase_orders po ON i.po_id = po.id
            ORDER BY i.id DESC
            '''
        ).fetchall()
    ]
    conn.close()
    return jsonify(rows)


@app.route('/api/payment', methods=['GET', 'POST'])
def payments():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.json
        inv = cur.execute(
            'SELECT * FROM invoices WHERE id = ?',
            (data['invoice_id'],)
        ).fetchone()

        if not inv:
            conn.close()
            return jsonify({'error': 'Invoice not found'}), 404

        number = doc_no('PY')
        cur.execute(
            'INSERT INTO payments (payment_number, invoice_id, amount, status) VALUES (?, ?, ?, ?)',
            (
                number,
                data['invoice_id'],
                inv['amount'],
                'PAID'
            )
        )
        cur.execute(
            'UPDATE invoices SET status = ? WHERE id = ?',
            ('PAID', data['invoice_id'])
        )
        conn.commit()
        conn.close()
        return jsonify({
            'message': 'Payment completed',
            'payment_number': number,
            'amount': inv['amount']
        })

    rows = [
        dict(r) for r in cur.execute(
            '''
            SELECT p.id, p.payment_number, i.invoice_number, p.amount, p.status, p.created_at
            FROM payments p
            JOIN invoices i ON p.invoice_id = i.id
            ORDER BY p.id DESC
            '''
        ).fetchall()
    ]
    conn.close()
    return jsonify(rows)


@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    conn = get_conn()
    cur = conn.cursor()

    data = {
        'vendors': cur.execute('SELECT COUNT(*) c FROM vendors').fetchone()['c'],
        'materials': cur.execute('SELECT COUNT(*) c FROM materials').fetchone()['c'],
        'prs': cur.execute('SELECT COUNT(*) c FROM purchase_requisitions').fetchone()['c'],
        'pos': cur.execute('SELECT COUNT(*) c FROM purchase_orders').fetchone()['c'],
        'grs': cur.execute('SELECT COUNT(*) c FROM goods_receipts').fetchone()['c'],
        'invoices': cur.execute('SELECT COUNT(*) c FROM invoices').fetchone()['c'],
        'payments': cur.execute('SELECT COUNT(*) c FROM payments').fetchone()['c'],
    }

    conn.close()
    return jsonify(data)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)