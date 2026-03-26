import ray

ray.init()

@ray.remote
def square(x):
    return x * x

if __name__ == "__main__":
    future1 = square.remote(10)
    future2 = square.remote(20)

    result1 = ray.get(future1)
    result2 = ray.get(future2)

    print("Ray Results:", result1, result2)

    ray.shutdown()
