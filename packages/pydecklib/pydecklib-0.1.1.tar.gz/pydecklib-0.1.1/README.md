# pydecklib

A deck of cards

## Installation

```bash
$ pip install pydecklib
```

## Usage

`pydecklib` can be used to use a deck of cards in a game context.

```python
from pydecklib.deck import Deck

deck = Deck()
deck.shuffle()
card = deck.draw()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pydecklib` was created by amaurylekens. It is licensed under the terms of the MIT license.

## Credits

`pydecklib` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
