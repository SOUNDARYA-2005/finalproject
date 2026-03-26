import json

def ingest_logs(file_path):
    logs = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip():  # skip empty lines
                logs.append(json.loads(line))
    return logs