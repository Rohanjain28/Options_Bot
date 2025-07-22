from flask import Flask, request, jsonify
import websocket
import json
import threading
import os

# Your Deriv API Token
DERIV_TOKEN = "PUT_YOUR_DERIV_API_TOKEN_HERE"

# Flask app setup
app = Flask(__name__)

# Function to place a trade via WebSocket
def place_deriv_trade(data):
    def on_open(ws):
        print("WebSocket connection opened.")
        auth_req = json.dumps({"authorize": DERIV_TOKEN})
        ws.send(auth_req)

    def on_message(ws, message):
        response = json.loads(message)
        if response.get("msg_type") == "authorize":
            trade_request = {
                "buy": 1,
                "price": float(data["amount"]),
                "parameters": {
                    "amount": float(data["amount"]),
                    "basis": "stake",
                    "contract_type": data["contract_type"].upper(),
                    "currency": "USD",
                    "duration": int(data["duration"]),
                    "duration_unit": data["duration_unit"],
                    "symbol": data["symbol"].upper()
                }
            }
            print("Sending trade request:", trade_request)
            ws.send(json.dumps(trade_request))

        elif response.get("msg_type") == "buy":
            print("Trade executed successfully:", response)
            ws.close()

    def on_error(ws, error):
        print("WebSocket error:", error)

    def on_close(ws, close_status_code, close_msg):
        print("WebSocket connection closed.")

    ws = websocket.WebSocketApp(
        "wss://ws.derivws.com/websockets/v3?app_id=1089",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # Run the WebSocket in a new thread
    wst = threading.Thread(target=ws.run_forever)
    wst.start()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received TradingView alert:", data)

    required_keys = ["symbol", "amount", "duration", "duration_unit", "contract_type"]
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing required keys in alert"}), 400

    place_deriv_trade(data)
    return jsonify({"status": "Trade request sent to Deriv"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
