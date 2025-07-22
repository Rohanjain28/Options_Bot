from iqoptionapi.stable_api import IQ_Option
import time

EMAIL = "your_email_here"
PASSWORD = "your_password_here"

def execute_trade(data):
    act = data.get('symbol', 'EURUSD')
    amt = float(data.get('amount', 1))
    action = data.get('direction', 'call')
    duration = int(data.get('duration', 1))

    iq = IQ_Option(EMAIL, PASSWORD)
    iq.connect()

    while not iq.check_connect():
        time.sleep(1)

    success, trade_id = iq.buy(amt, act, action, duration)
    return f"Trade {'Executed' if success else 'Failed'} | ID: {trade_id}"
