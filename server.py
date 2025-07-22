from flask import Flask, request
from trade import execute_trade

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    result = execute_trade(data)
    return result

if __name__ == "__main__":
    app.run(port=5000)
