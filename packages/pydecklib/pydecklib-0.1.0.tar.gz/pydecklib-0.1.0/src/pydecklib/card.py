#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import annotations

from enum import Enum


class Suit(Enum):
    SPADES = 0
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3


class Value(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card:

    """
    Represents a playing card with a suit and a value. Provides methods to
    access card properties and compare cards based on a customizable ranking
    system defined for suits and values. The ranking can be adjusted to
    prioritise suit over value if desired.

    Attributes:
        suit_ranking (dict): A dictionary mapping Suit enums to their ranks.
        value_ranking (dict): A dictionary mapping Value enums to their ranks.
        suit_ordered (bool): Flag to determine if suit is considered in
                             ranking.

    :param suit: The suit of the card.
    :type suit: Suit
    :param value: The value of the card.
    :type value: Value
    """

    suit_ranking = {
        Suit.CLUBS: 0, Suit.SPADES: 1, Suit.HEARTS: 2,
        Suit.DIAMONDS: 3
    }
    value_ranking = {
        Value.TWO: 0, Value.THREE: 1, Value.FOUR: 2, Value.FIVE: 3,
        Value.SIX: 4, Value.SEVEN: 5, Value.EIGHT: 6, Value.NINE: 7,
        Value.TEN: 8, Value.JACK: 9, Value.QUEEN: 10, Value.KING: 11,
        Value.ACE: 12
    }
    suit_ordered = False

    def __init__(self, suit: Suit, value: Value):

        """
        Initializes a new Card instance with the specified suit and value.
        """

        self._suit = suit
        self._value = value

    @property
    def value(self) -> Value:

        """
        Gets the value of the card.

        :return: The value of the card.
        :rtype: Value
        """

        return self._value

    @property
    def suit(self) -> Suit:

        """
        Gets the suit of the card.

        :return: The suit of the card.
        :rtype: Suit
        """

        return self._suit

    def _rank(self):

        """
        Private method to calculate the rank of the card based on its suit and
        value.

        :return: The rank of the card.
        :rtype: int
        """

        if self.suit_ordered:
            rank = self.suit_ranking[self._suit] * len(self.value_ranking) + \
                   self.value_ranking[self._value]
        else:
            rank = self.value_ranking[self._value]

        return rank

    def __lt__(self, to: Card) -> bool:

        return self._rank() < to._rank()

    def __eq__(self, to: Card) -> bool:

        return self._rank() == to._rank()

    def __le__(self, to: Card) -> bool:

        return self._rank() > to._rank()

    def __repr__(self):

        # Base Unicode point for the suits
        base = 0x1F0A0

        # Adjusting the Unicode point based on suit and value
        suit_offset = self._suit.value * 16
        value_offset = self._value.value

        # For values 11 to 13 (Jack, Queen, King), the offset is adjusted as
        # they use 'B', 'D', 'E' in Unicode
        if self._value.value > 10:
            value_offset += 1

        unicode_value = base + suit_offset + value_offset

        return chr(unicode_value)
