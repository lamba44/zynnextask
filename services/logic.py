import json
import re

with open("data/orders.json") as f:
    orders = json.load(f)

with open("data/policies.json") as f:
    policies = json.load(f)


def find_order(order_id):
    for o in orders:
        if o["order_id"] == order_id:
            return o
    return None


def handle_query(text):
    text = text.lower()

    order_match = re.search(r"ord\d+", text.upper())
    order_id = order_match.group(0) if order_match else None

    if "order" in text and order_id:
        order = find_order(order_id)
        if not order:
            return "Order not found"

        if order["status"] == "delivered":
            return f"Order {order_id} was delivered on {order['delivery_date']}"
        if order["status"] == "in_transit":
            return f"Order {order_id} is in transit and will arrive by {order['expected_delivery']}"

    if "return" in text:
        r = policies["returns"]
        return f"Returns allowed within {r['window_days']} days. Conditions: {', '.join(r['conditions'])}"

    if "refund" in text:
        r = policies["refunds"]
        return f"Refunds are processed via {r['method']} in {r['processing_time_days']} days"

    return "Sorry, I did not understand your query"
