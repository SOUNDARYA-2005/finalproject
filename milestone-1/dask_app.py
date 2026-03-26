from dask import delayed
import dask

@delayed
def square(x):
    return x * x

@delayed
def sum_values(a, b):
    return a + b

if __name__ == "__main__":
    a = square(10)
    b = square(20)
    total = sum_values(a, b)

    print("Dask Result:", total.compute())
