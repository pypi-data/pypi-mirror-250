# Installation
The following instructions are for installing the SGIA package on a Linux/Windows/MacOS system. The following vector indexing algorithm is implemented in Python 3.6.8. The package is available on PyPI and can be installed using pip. The package is also available on GitHub.

## Requirements
    numpy
    scipy

## Installation
    pip install sgia

## Source
    https://pypi.org/project/sgia/

# Usage
```python
from sgia import SGIA

# Create a SGIA object
sgia = SGIA()
sgia.insert([1.0, 2.0], "Data A")
sgia.insert([3.0, 4.0], "Data B")
sgia.insert([5.0, 6.0], "Data C")

# Display the index
sgia.display()

# Search for nearest neighbors to a query vector
query = [2.0, 3.0]
k_neighbors = sgia.search(query, k=3)

print("Nearest neighbors to query:", k_neighbors)

```