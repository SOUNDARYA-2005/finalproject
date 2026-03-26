from dask_pipeline import run_dask
from ray_pipeline import run_ray

print("Running Dask Pipeline...")
run_dask("data/sample_logs.json")

print("\nRunning Ray Pipeline...")
run_ray("data/sample_logs.json")