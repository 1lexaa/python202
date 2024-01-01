from functools import reduce


# <--====== Functions for calculating averages sector. ======-->
_arithmetic_function = lambda data: sum(data) / len(data)
_geometric_function = lambda data: reduce(lambda x, y: x * y, data) ** (1 / len(data))
_harmonic_function = lambda data: len(data) / sum(1 / x for x in data)

# <--======  Function for applying a strategy with the selected mean distribution method sector. ======-->
def ApplyStrategy(data, mean_strategy):
    return mean_strategy(data)

# <--====== Custom code. sector. ======-->
_data_set = [2, 4, 6, 8, 10]

print(f"Arithmetic average: {ApplyStrategy(_data_set, _arithmetic_function)}")
print(f"Geometric average: {ApplyStrategy(_data_set, _geometric_function)}")
print(f"Harmonic average: {ApplyStrategy(_data_set, _harmonic_function)}")