import ray
import time
import logging
from ingestion import ingest_logs
from parser import parse_log
from processing import process_logs

# ------------------ Logging Configuration ------------------
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ Initialize Ray ------------------
ray.init()

@ray.remote
def parse_batch(log_batch):
    results = []
    for log in log_batch:
        parsed = parse_log(log)
        if parsed is not None:
            results.append(parsed)
    return results


def run_ray(file_path):
    logging.info("Ray pipeline started")
    start = time.time()

    logs = ingest_logs(file_path)
    logging.info(f"Total logs ingested: {len(logs)}")

    # -------- Batching --------
    batch_size = 500
    batches = [logs[i:i + batch_size] for i in range(0, len(logs), batch_size)]
    logging.info(f"Total batches created: {len(batches)}")

    futures = [parse_batch.remote(batch) for batch in batches]

    parsed_logs = []
    for batch_result in ray.get(futures):
        parsed_logs.extend(batch_result)

    logging.info(f"Total parsed logs: {len(parsed_logs)}")

    # -------- Analytics Layer --------
    error_count = process_logs(parsed_logs)
    logging.info(f"Total ERROR logs: {error_count}")

    end = time.time()
    total_time = end - start

    throughput = len(parsed_logs) / total_time

    logging.info(f"Ray Processing Time: {total_time}")
    logging.info(f"Throughput: {throughput} logs/sec")

    print("Ray Processing Time:", total_time)
    print("Throughput:", throughput, "logs/sec")

    logging.info("Ray pipeline completed successfully")

    return parsed_logs


if __name__ == "__main__":
    run_ray("data/sample_logs.jsonl")