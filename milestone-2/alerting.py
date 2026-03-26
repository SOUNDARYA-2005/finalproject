import logging

def send_alerts(anomalies):
    if not anomalies:
        print("No anomalies detected.")
        logging.info("No anomalies detected.")
        return

    print("\n🚨 ALERT: Anomalies Detected! 🚨")

    for anomaly in anomalies:
        print(anomaly)
        logging.warning(f"Anomaly detected: {anomaly}")