import glob

processed_files = set()

def ingest_logs():
    files = glob.glob("data/*.jsonl")

    new_files = [f for f in files if f not in processed_files]

    for file in new_files:
        processed_files.add(file)

    return new_files