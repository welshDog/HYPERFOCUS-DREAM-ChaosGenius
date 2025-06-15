
from flask import Flask, request, jsonify
import json
import sqlite3
import time

app = Flask(__name__)

@app.route('/paypal-webhook', methods=['POST'])
def paypal_webhook():
    """🔔 Handle PayPal webhook notifications"""
    try:
        event_data = request.json
        event_type = event_data.get('event_type')

        if event_type == 'CHECKOUT.ORDER.APPROVED':
            # Payment approved!
            resource = event_data['resource']
            order_id = resource['id']
            amount = resource['purchase_units'][0]['amount']['value']

            print(f"💰 PAYMENT APPROVED: {order_id} - ${amount}")

            # Update database
            with sqlite3.connect('/root/chaosgenius/boss_payment_processing.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE service_invoices
                    SET status = 'PAID'
                    WHERE paypal_invoice_id = ?
                """, (order_id,))
                conn.commit()

            # Trigger celebration in agent army!
            print("🎉 AGENT ARMY: BOSS GOT PAID! CELEBRATION TIME!")

        return jsonify({"status": "success"})

    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
        