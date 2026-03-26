import pandas as pd

output_file = "processed_logs/output.csv"


def process_logs(parsed_logs):

    logs = []

    for log in parsed_logs:

        level = log["level"]

        # Simple anomaly rule
        anomaly = 1 if level == "ERROR" and log["service"] == "payment-service" else 0

        logs.append({
            "@timestamp": log["@timestamp"],
            "level": level,
            "service": log["service"],
            "message": log["message"],
            "anomaly": anomaly
        })

    df = pd.DataFrame(logs)

    error_count = df[df["level"] == "ERROR"].shape[0]

    print("Total ERROR logs:", error_count)

    df.to_csv(output_file, index=False)

    print("Processed logs saved to:", output_file)