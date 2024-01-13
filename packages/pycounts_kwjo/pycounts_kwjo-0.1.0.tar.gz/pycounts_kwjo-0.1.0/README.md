# pycounts_kwjo

Calculate word counts in a text file

## Installation

```bash
$ pip install pycounts_kwjo
```

## Usage

`pycounts_kwjo` can be used to count words in a text file and plot the results as follows:

```bash
from pycounts_kwjo.pycounts_kwjo import count_words
from pycounts_kwjo.plotting import plot_words
import matplotlib.pyplot as plt

file_path = "test.txt"  # path to your file
counts = count_words(file_path)
fig = plot_words(counts, n=10)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pycounts_kwjo` was created by Kittipong Wongwipasamitkun. It is licensed under the terms of the MIT license.

## Credits

`pycounts_kwjo` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
