import json
import random
import time
from datetime import datetime

levels = ["INFO", "WARN", "ERROR"]

services = [
    "auth-service",
    "payment-service",
    "order-service"
]

messages = {
    "INFO": [
        "User login successful",
        "Request processed",
        "Service running normally"
    ],
    "WARN": [
        "Slow response detected",
        "High memory usage"
    ],
    "ERROR": [
        "Database connection failed",
        "Payment processing error",
        "Service unavailable"
    ]
}

file_path = "data/sample_logs.json"

print("Generating logs... Press CTRL+C to stop")

with open(file_path, "w") as f:

    for i in range(5000):

        level = random.choice(levels)

        log = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "service": random.choice(services),
            "message": random.choice(messages[level]),
            "ip": f"192.168.1.{random.randint(1,254)}"
        }

        f.write(json.dumps(log) + "\n")

        time.sleep(0.01)

print("5000 JSON-line logs generated.")