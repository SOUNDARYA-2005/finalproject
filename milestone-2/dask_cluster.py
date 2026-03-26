from dask.distributed import Client

def start_cluster():
    client = Client()
    print(client)
    return client

if __name__ == "__main__":
    start_cluster()