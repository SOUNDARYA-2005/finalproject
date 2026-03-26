from dask.distributed import Client
import time
import logging
import pandas as pd
import os

from ingestion import ingest_logs
from parser import parse_log
from processing import process_logs
from anomaly_detection import detect_anomalies
from alerting import send_alerts


# ---------------- Logging ----------------
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------- Batch Parsing ----------------
def parse_batch(log_batch):
    """Parse a batch of logs."""
    results = []
    for log in log_batch:
        parsed = parse_log(log)
        if parsed:
            results.append(parsed)
    return results


# ---------------- Main Pipeline ----------------
def run_dask(file_path):

    with Client() as client:

        print("Dask cluster started:", client)
        print("Dask Dashboard Link:", client.dashboard_link)

        logging.info("Dask pipeline started")
        start_time = time.time()

        # -------- Ingestion --------
        logs = ingest_logs(file_path)
        print("Total logs ingested:", len(logs))
        logging.info(f"Logs ingested: {len(logs)}")

        if not logs:
            print("⚠️ No logs found")
            return []

        # -------- Create Batches --------
        batch_size = 500
        batches = [logs[i:i + batch_size] for i in range(0, len(logs), batch_size)]

        logging.info(f"Batches created: {len(batches)}")

        # -------- Distributed Parsing --------
        futures = client.map(parse_batch, batches)
        results = client.gather(futures)

        parsed_logs = []

        for batch in results:
            parsed_logs.extend(batch)

        print("Sample processed logs:", parsed_logs[:3])

        logging.info(f"Parsed logs: {len(parsed_logs)}")

        if not parsed_logs:
            print("⚠️ No parsed logs available")
            return []

        # -------- Analytics --------
        process_logs(parsed_logs)

        # -------- Anomaly Detection --------
        anomalies = detect_anomalies(parsed_logs)

        print("Anomalies detected:", len(anomalies))
        logging.info(f"Anomalies detected: {len(anomalies)}")

        # -------- Alerting --------
        if anomalies:
            send_alerts(anomalies)
            print("🚨 Alerts sent!")
        else:
            print("✅ No anomalies")

        # -------- Save CSV for Dashboard --------
        os.makedirs("processed_logs", exist_ok=True)

        df = pd.DataFrame(parsed_logs)

        # Add anomaly column
        df["anomaly"] = 0

        # -------- Mark anomalies in dataframe --------
        if anomalies:

            for anomaly in anomalies:

                index = next(
                    (i for i, log in enumerate(parsed_logs) if log == anomaly),
                    None
                )

                if index is not None and index < len(df):
                    df.loc[index, "anomaly"] = 1

        # Save CSV
        df.to_csv("processed_logs/output.csv", index=False)

        print("✅ CSV saved for dashboard")

        # -------- Save anomalies separately --------
        if anomalies:

            os.makedirs("docs/outputs", exist_ok=True)

            with open("docs/outputs/anomalies.txt", "w") as f:

                for anomaly in anomalies:
                    f.write(str(anomaly) + "\n")

        # -------- Performance Metrics --------
        end_time = time.time()

        total_time = end_time - start_time

        throughput = len(parsed_logs) / total_time if total_time > 0 else 0

        print("\n⏱ Processing Time:", round(total_time, 2), "seconds")
        print("🚀 Throughput:", round(throughput, 2), "logs/sec")

        logging.info(f"Processing Time: {total_time}")
        logging.info(f"Throughput: {throughput}")
        logging.info("Pipeline completed")

        return parsed_logs


# ---------------- Run Pipeline ----------------
if __name__ == "__main__":
    run_dask("data/sample_logs_new.jsonl")