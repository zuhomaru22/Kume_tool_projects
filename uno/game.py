"""ゲームの進行ルール。"""
from __future__ import annotations

import random

from .card import Card, Color, Value, shuffled_deck
from .player import Player

INITIAL_HAND = 7


class Game:
    def __init__(self, players: list[Player], verbose: bool = True):
        if not 2 <= len(players) <= 10:
            raise ValueError("プレイヤーは2〜10人です。")
        self.players = players
        self.verbose = verbose
        self.deck: list[Card] = shuffled_deck()
        self.discard: list[Card] = []
        self.index = 0
        self.direction = 1
        self.winner: Player | None = None
        self._setup()

    # ---------- 準備 ----------
    def _setup(self) -> None:
        for p in self.players:
            p.hand = [self.deck.pop() for _ in range(INITIAL_HAND)]
        # 最初の場札は数字カードにする(ややこしい特殊処理を避けるため)
        while True:
            card = self.deck.pop()
            if card.value.value.isdigit():
                break
            self.deck.insert(0, card)
        self.discard.append(card)
        self.current_color: Color = card.color
        self.index = random.randrange(len(self.players))

    # ---------- 状態 ----------
    @property
    def top_card(self) -> Card:
        return self.discard[-1]

    @property
    def current_player(self) -> Player:
        return self.players[self.index]

    def can_play(self, card: Card) -> bool:
        if card.is_wild:
            return True
        return card.color is self.current_color or card.value is self.top_card.value

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    # ---------- 山札 ----------
    def draw_cards(self, n: int) -> list[Card]:
        drawn: list[Card] = []
        for _ in range(n):
            if not self.deck:
                self._reshuffle()
            if not self.deck:
                break  # 引けるカードが無い
            drawn.append(self.deck.pop())
        return drawn

    def _reshuffle(self) -> None:
        top = self.discard.pop()
        self.deck = self.discard
        random.shuffle(self.deck)
        self.discard = [top]

    # ---------- 進行 ----------
    def _advance(self, steps: int = 1) -> None:
        self.index = (self.index + self.direction * steps) % len(self.players)

    def _next_player(self) -> Player:
        return self.players[(self.index + self.direction) % len(self.players)]

    def play_turn(self) -> None:
        """現在のプレイヤーの1ターンを進める。"""
        player = self.current_player
        card = player.choose_card(self)

        if card is None:
            drawn = self.draw_cards(1)
            if not drawn:
                self._log(f"{player.name} は引けるカードがなく、パス")
                self._advance()
                return
            new = drawn[0]
            player.hand.append(new)
            self._log(f"{player.name} は山札から1枚引いた")
            if self.can_play(new) and player.wants_to_play_drawn(new, self):
                card = new
            else:
                self._advance()
                return

        self._play_card(player, card)

    def _play_card(self, player: Player, card: Card) -> None:
        player.hand.remove(card)
        self.discard.append(card)
        self.current_color = card.color
        if card.is_wild:
            self.current_color = player.choose_color(self)
        self._log(f"{player.name} が {card.colored()} を出した"
                  + (f" → 色は{self.current_color.value}" if card.is_wild else ""))

        if len(player.hand) == 1:
            self._log(f"★ {player.name}: UNO!")
        if not player.hand:
            self.winner = player
            return

        self._apply_effect(card)

    def _apply_effect(self, card: Card) -> None:
        v = card.value
        if v is Value.SKIP:
            self._log(f"  {self._next_player().name} はスキップ")
            self._advance(2)
        elif v is Value.REVERSE:
            self.direction *= -1
            # 2人のときはスキップと同じ扱い
            self._advance(2 if len(self.players) == 2 else 1)
        elif v in (Value.DRAW2, Value.WILD4):
            n = 2 if v is Value.DRAW2 else 4
            victim = self._next_player()
            victim.hand += self.draw_cards(n)
            self._log(f"  {victim.name} は{n}枚引いてスキップ")
            self._advance(2)
        else:
            self._advance()

    def run(self) -> Player:
        while self.winner is None:
            self.play_turn()
        self._log(f"\n🎉 {self.winner.name} の勝ち!")
        return self.winner
