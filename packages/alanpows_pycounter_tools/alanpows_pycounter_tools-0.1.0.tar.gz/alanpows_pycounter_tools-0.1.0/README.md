# alanpows_pycounter_tools

A package to help you count through your texts and understand how many and what words you have!

## Installation

```bash
$ pip install alanpows_pycounter_tools
```

## Usage

`alanpows_pycounter_tools` can be used to count words in a text file and plot results
as follows:

```python
from alanpows_pycounter_tools.alanpows_pycounter_tools import count_words
from alanpows_pycounter_tools.plotting import plot_words
import matplotlib.pyplot as plt

file_path = "test.txt"  # path to your file
counts = count_words(file_path)
fig = plot_words(counts, n=10)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`alanpows_pycounter_tools` was created by Alan Powichrowski. It is licensed under the terms of the MIT license.

## Credits

`alanpows_pycounter_tools` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
