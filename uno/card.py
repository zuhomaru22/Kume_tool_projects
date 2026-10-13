"""カードの定義とデッキ生成。"""
from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum


class Color(Enum):
    RED = "赤"
    YELLOW = "黄"
    GREEN = "緑"
    BLUE = "青"
    WILD = "ワイルド"


class Value(Enum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    SKIP = "スキップ"
    REVERSE = "リバース"
    DRAW2 = "ドロー2"
    WILD = "ワイルド"
    WILD4 = "ワイルドドロー4"


NUMBER_VALUES = [v for v in Value if v.value.isdigit()]
ACTION_VALUES = [Value.SKIP, Value.REVERSE, Value.DRAW2]
PLAYABLE_COLORS = [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE]

ANSI = {
    Color.RED: "\033[91m",
    Color.YELLOW: "\033[93m",
    Color.GREEN: "\033[92m",
    Color.BLUE: "\033[94m",
    Color.WILD: "\033[95m",
}
RESET = "\033[0m"


@dataclass(frozen=True)
class Card:
    color: Color
    value: Value

    @property
    def is_wild(self) -> bool:
        return self.color is Color.WILD

    def __str__(self) -> str:
        if self.is_wild:
            return self.value.value
        return f"{self.color.value}の{self.value.value}"

    def colored(self) -> str:
        return f"{ANSI[self.color]}{self}{RESET}"


def build_deck() -> list[Card]:
    """標準的な108枚のデッキを作る(シャッフルはしない)。"""
    deck: list[Card] = []
    for color in PLAYABLE_COLORS:
        deck.append(Card(color, Value.ZERO))  # 0は各色1枚
        for v in NUMBER_VALUES[1:]:  # 1-9は各色2枚
            deck += [Card(color, v)] * 2
        for v in ACTION_VALUES:  # 記号カードは各色2枚
            deck += [Card(color, v)] * 2
    deck += [Card(Color.WILD, Value.WILD)] * 4
    deck += [Card(Color.WILD, Value.WILD4)] * 4
    return deck


def shuffled_deck() -> list[Card]:
    deck = build_deck()
    random.shuffle(deck)
    return deck
