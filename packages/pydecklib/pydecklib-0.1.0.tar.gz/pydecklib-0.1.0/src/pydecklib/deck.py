#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

import random
from typing import Optional, Generator, List, Iterator, Tuple

from src.pydecklib.card import Card, Suit, Value


class Deck:

    """
    Represents a deck of playing cards. Allows initialisation with a standard
    deck, shuffling, drawing cards, and adding cards to the deck. The deck can
    be customized with a specific number of cards, shuffled with a seed, or
    overridden with a custom set of cards.

    :param initialise: Flag to initialise the deck with standard cards.
    :type initialise: bool
    :param shuffle: Flag to shuffle the deck upon initialisation.
    :type shuffle: bool
    :param n: Number of cards to initialise in the deck, None for full deck.
    :type n: Optional[int]
    :param override: Custom set of cards to initialise the deck with.
    :type override: Optional[Tuple[Card]]
    :param seed: Seed for shuffling operations.
    :type seed: Optional[int]

    :Example:
        >>> deck = Deck(shuffle=True)  # Create and shuffle a deck
        >>> top_card = next(deck.draw())  # Draw the top card
        >>> top_card
        Card(Suit.HEARTS, Value.ACE)

        >>> deck.add_card(Card(Suit.CLUBS, Value.TWO))  # Add a card to the deck
        >>> deck.cards_count
        51

        >>> empty_deck = Deck(initialise=False)  # Create an empty deck
        >>> empty_deck.empty
        True
    """

    def __init__(
        self, initialise: bool = True, shuffle: bool = False,
        n: Optional[int] = None, override: Optional[Tuple[Card], ...] = None,
        seed: Optional[int] = None
    ):

        self._deck: list = list()

        if initialise:
            self.initialise(shuffle, n, seed)

        if override is not None:
            self._deck = list(override)

    @property
    def empty(self) -> bool:

        """
        Checks if the deck is empty.

        :return: True if the deck is empty, False otherwise.
        :rtype: bool

        :Example:
            >>> deck = Deck()
            >>> deck.empty
            False
        """

        return len(self._deck) == 0

    @property
    def cards_count(self) -> int:

        """
        Counts the number of cards remaining in the deck.

        :return: The number of cards in the deck.
        :rtype: int

        :Example:
            >>> deck = Deck()
            >>> deck.cards_count
            52
        """

        return len(self._deck)

    def initialise(
        self, shuffle: bool = False, n: Optional[int] = None,
        seed: Optional[int] = None
    ) -> None:

        """
        Initialises or reinitialises the deck. The deck can be shuffled, and a
        specific number of cards can be selected.

        :param shuffle: Whether to shuffle the deck.
        :param n: Number of cards to keep in the deck.
        :param seed: Seed for the shuffling operation.

        :Example:
            >>> deck = Deck(initialise=False)
            >>> deck.initialise(shuffle=True, n=20)
            >>> deck.cards_count
            20
        """

        self.clear()

        for suit in Suit:
            for value in Value:
                self._deck.append(Card(suit, value))

        if shuffle:
            self.shuffle(seed)

        if n:
            self._deck = self._deck[:n]

    def clear(self) -> None:

        """
        Empties the deck of all cards.

        :Example:
            >>> deck = Deck()
            >>> deck.clear()
            >>> deck.empty
            True
        """

        self._deck = list()

    def shuffle(self, seed: Optional[int] = None) -> None:

        """
        Shuffles the cards in the deck.

        :param seed: Seed for the random shuffle.

        :Example:
            >>> deck = Deck()
            >>> deck.shuffle(seed=42)  # Shuffles the deck with a specific seed
            >>> top_card = next(deck.draw())
            >>> top_card
            Card(Suit.DIAMONDS, Value.SIX)
        """

        if seed:
            random.seed(seed)

        random.shuffle(self._deck)

    def draw(self, n: int = 1) -> Generator[Card, None, None]:

        """
        Draws the top 'n' cards from the deck.

        :param n: Number of cards to draw.
        :return: A generator yielding the drawn cards.

        :Example:
            >>> deck = Deck()
            >>> cards_drawn = [card for card in deck.draw(3)]
            >>> len(cards_drawn)
            3
        """

        for i in range(n):

            if self.empty:
                break

            yield self._deck.pop(0)

    def draw_bottom(self, n: int = 1) -> Generator[Card, None, None]:

        """
        Draws the bottom 'n' cards from the deck.

        :param n: Number of cards to draw from the bottom.
        :return: A generator yielding the drawn cards.

        :Example:
            >>> deck = Deck()
            >>> bottom_cards = [card for card in deck.draw_bottom(2)]
            >>> len(bottom_cards)
            2
        """

        for i in range(n):

            if self.empty:
                break

            yield self._deck.pop(-1)

    def draw_random(
        self, n: int = 1, seed: Optional[int] = None
    ) -> Generator[Card, None, None]:

        """
        Draws 'n' random cards from the deck.

        :param n: Number of cards to draw randomly.
        :param seed: Seed for the random drawing.
        :return: A generator yielding the drawn cards.

        :Example:
            >>> deck = Deck()
            >>> random_cards = [card for card in deck.draw_random(2, seed=42)]
            >>> len(random_cards)
            2
        """

        if seed:
            random.seed(seed)

        for i in range(n):

            if self.empty:
                break

            index = random.randint(0, len(self._deck)-1)
            yield self._deck.pop(index)

    def add_card(
        self, card: Card, position: Optional[int] = None,
        seed: Optional[int] = None
    ) -> None:

        """
        Adds a single card to the deck at a specified or random position.
        By default, a random position is used.

        :param card: The card to add to the deck.
        :param position: Position to insert the card (None for random).
        :param seed: Seed for determining random position.

        :Example:
            >>> deck = Deck(initialise=False)
            >>> deck.add_card(Card(Suit.HEARTS, Value.THREE), position=0)
            >>> deck.cards_count
            1
        """

        if seed:
            random.seed(seed)

        if position:
            self._deck.insert(position, card)

        else:
            self._deck.insert(random.randint(0, len(self._deck)), card)

    def add_cards(
        self, cards: List[Card], seed: Optional[int] = None
    ) -> None:

        """
        Adds multiple cards to the deck at random positions.

        :param cards: A list of cards to add to the deck.
        :param seed: Seed for determining random positions.

        :Example:
            >>> deck = Deck(initialise=False)
            >>> deck.add_cards([
            ...     Card(Suit.DIAMONDS, Value.NINE),
            ...     Card(Suit.SPADES, Value.ACE)
            ... ])
            >>> deck.cards_count
            2
        """

        for card in cards:
            self.add_card(card, seed=seed)

    def __iter__(self) -> Iterator[Card]:

        return iter(self._deck)

    def __eq__(self, other: Deck) -> bool:

        return self._deck == other._deck
