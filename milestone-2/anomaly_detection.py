def detect_anomalies(logs):
    anomalies = []

    error_count = 0
    internal_ips = set()
    long_message_count = 0

    for log in logs:
        if log.get("level") == "ERROR":
            error_count += 1

        if log.get("message_length", 0) > 100:
            long_message_count += 1

        if log.get("ip", "").startswith("192.168"):
            internal_ips.add(log.get("ip"))

    # Add summarized anomalies
    if error_count > 5:
        anomalies.append(f"High error rate detected: {error_count} errors")

    if long_message_count > 0:
        anomalies.append(f"Long messages detected: {long_message_count}")

    if internal_ips:
        anomalies.append(f"Internal IP activity from {len(internal_ips)} unique IPs")

    return anomalies