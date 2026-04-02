import json
import re

with open("data/orders.json") as f:
    orders = json.load(f)

with open("data/policies.json") as f:
    policies = json.load(f)


def normalize_text(text):
    text = text.lower()
    text = text.replace("ordered", "order")
    return text


def extract_order_id(text):
    text = text.upper()
    match = re.search(r"ORD\s*\d+", text)
    if match:
        return match.group(0).replace(" ", "")
    return None


def find_order(order_id):
    for o in orders:
        if o["order_id"] == order_id:
            return o
    return None


def handle_query(text):
    text = normalize_text(text)
    order_id = extract_order_id(text)

    if "order" in text and order_id:
        order = find_order(order_id)
        if not order:
            return f"Order {order_id} not found"

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
