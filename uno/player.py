"""プレイヤー(人間 / CPU)。新しい種類のプレイヤーはここに追加する。"""
from __future__ import annotations

import random
from collections import Counter
from typing import TYPE_CHECKING

from .card import PLAYABLE_COLORS, Card, Color

if TYPE_CHECKING:
    from .game import Game


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] = []

    # --- サブクラスで実装する ---
    def choose_card(self, game: "Game") -> Card | None:
        """出すカードを返す。出せない/出さないなら None(山札から引く)。"""
        raise NotImplementedError

    def choose_color(self, game: "Game") -> Color:
        """ワイルドを出したときの色を選ぶ。"""
        raise NotImplementedError

    def wants_to_play_drawn(self, card: Card, game: "Game") -> bool:
        """引いたカードが出せるとき、出すかどうか。"""
        return True

    def playable_cards(self, game: "Game") -> list[Card]:
        return [c for c in self.hand if game.can_play(c)]

    def most_common_color(self) -> Color:
        counts = Counter(c.color for c in self.hand if not c.is_wild)
        if not counts:
            return random.choice(PLAYABLE_COLORS)
        return counts.most_common(1)[0][0]


class CPUPlayer(Player):
    def choose_card(self, game: "Game") -> Card | None:
        playable = self.playable_cards(game)
        if not playable:
            return None
        # ワイルドは最後の手段にする
        non_wild = [c for c in playable if not c.is_wild]
        return random.choice(non_wild or playable)

    def choose_color(self, game: "Game") -> Color:
        return self.most_common_color()


class HumanPlayer(Player):
    def choose_card(self, game: "Game") -> Card | None:
        print(f"\n=== {self.name} の番 ===")
        print(f"場: {game.top_card.colored()}  (現在の色: {game.current_color.value})")
        print("手札:")
        for i, card in enumerate(self.hand, 1):
            mark = "*" if game.can_play(card) else " "
            print(f"  {mark}{i:2d}: {card.colored()}")
        print("  (* = 出せるカード / 0 = 山札から引く)")
        while True:
            raw = input("番号を入力 > ").strip()
            if not raw.isdigit():
                print("数字を入力してください。")
                continue
            n = int(raw)
            if n == 0:
                return None
            if 1 <= n <= len(self.hand):
                card = self.hand[n - 1]
                if game.can_play(card):
                    return card
                print("そのカードは出せません。")
            else:
                print("範囲外です。")

    def choose_color(self, game: "Game") -> Color:
        print("色を選んでください: " + " / ".join(f"{i}={c.value}" for i, c in enumerate(PLAYABLE_COLORS, 1)))
        while True:
            raw = input("色の番号 > ").strip()
            if raw.isdigit() and 1 <= int(raw) <= 4:
                return PLAYABLE_COLORS[int(raw) - 1]
            print("1〜4を入力してください。")

    def wants_to_play_drawn(self, card: Card, game: "Game") -> bool:
        print(f"引いたカード: {card.colored()} (出せます)")
        return input("出しますか? [y/N] > ").strip().lower() == "y"
