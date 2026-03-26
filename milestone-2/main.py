import time
from realtime_ingestion import ingest_logs
from dask_pipeline import run_dask

def run_pipeline():
    print("🚀 Real-Time Log Monitoring Started...\n")

    while True:
        files = ingest_logs()

        if not files:
            print("⏳ No new files...")
        else:
            for file in files:
                print(f"📂 Processing file: {file}")
                run_dask(file)

        time.sleep(5)

if __name__ == "__main__":
    run_pipeline()