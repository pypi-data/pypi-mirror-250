```
# JTools: A Python Library for Data Manipulation

JTools is a Python library designed to simplify common data manipulation tasks. The library currently consists of two modules: `Sorter` and `Adder`. These modules provide easy-to-use functions for sorting and adding numeric data, respectively.

## Installation

To install JTools, simply use pip:

```bash
pip install jtools
```

## Modules

### Sorter

The `Sorter` module offers functionalities for sorting arrays. It's built on top of NumPy, ensuring efficient sorting for large datasets.

#### Usage:

```python
from jtools import Sorter

# Initialize the Sorter
s = Sorter()

# Sort an array
things = [5, 1, 4, 2, 3]
sorted_things = s.sort_things(things)
print(sorted_things)
```

### Adder

The `Adder` module provides a simple way to add two arrays. Like `Sorter`, it relies on NumPy for fast computations.

#### Usage:

```python
from jtools import Adder

# Initialize the Adder
a = Adder()

# Add two arrays
things1 = [5, 1, 4, 2, 3]
things2 = [1, 2, 3, 4, 5]
summed_things = a.add_things(things1, things2)
print(summed_things)
```

## Contributing

Contributions to JTools are welcome! Please feel free to submit pull requests or open issues to discuss proposed changes or report bugs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```
