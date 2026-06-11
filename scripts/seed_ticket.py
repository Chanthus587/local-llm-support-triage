import requests


payload = {
    "customer_id": "cust-demo-1",
    "subject": "Payment failed but card was charged",
    "body": "The checkout screen says payment failed, but our bank shows a charge. Please help urgently because our account renewal is due today.",
    "channel": "email",
}

response = requests.post("http://localhost:8000/tickets", json=payload, timeout=10)
response.raise_for_status()
print(response.json())
