from elasticsearch import Elasticsearch
import pandas as pd

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "roHqG6c2O6tQdIXAc1_b"),
    verify_certs=False
)

# Read CSV
df = pd.read_csv("processed_logs/output.csv")

# Send logs
for _, row in df.iterrows():
    es.index(index="logs", document=row.to_dict())

print("Logs successfully sent to Elasticsearch!")