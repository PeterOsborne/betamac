import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import math


def is_one(number):
    return number == 1


def main():
    n = 900
    samples = get_samples(0, n, [])
    ones_length = len(list(filter(is_one, samples)))
    print(f"Our estimation of pi is: {ones_length/len(samples) * 4}")


def get_samples(i, n, samples):
    if i < n:
        x = random.random()
        y = random.random()
        length = math.sqrt(x**2 + y**2)
        if length <= 1:
            samples.append(1)
        else:
            samples.append(0)
        samples = get_samples(i + 1, n, samples)
    return samples

if __name__ == "__main__":
    main()
