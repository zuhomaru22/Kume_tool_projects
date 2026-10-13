from collections import Counter

from uno.card import Color, Value, build_deck, Card
from uno.game import Game
from uno.player import CPUPlayer


def test_deck_has_108_cards():
    deck = build_deck()
    assert len(deck) == 108
    assert Counter(deck)[Card(Color.RED, Value.ZERO)] == 1
    assert Counter(deck)[Card(Color.WILD, Value.WILD4)] == 4


def test_deal():
    g = Game([CPUPlayer("a"), CPUPlayer("b")], verbose=False)
    assert all(len(p.hand) == 7 for p in g.players)
    assert len(g.deck) == 108 - 14 - 1


def test_can_play():
    g = Game([CPUPlayer("a"), CPUPlayer("b")], verbose=False)
    g.discard.append(Card(Color.RED, Value.FIVE))
    g.current_color = Color.RED
    assert g.can_play(Card(Color.RED, Value.NINE))
    assert g.can_play(Card(Color.BLUE, Value.FIVE))
    assert g.can_play(Card(Color.WILD, Value.WILD))
    assert not g.can_play(Card(Color.BLUE, Value.NINE))


def test_cpu_games_always_finish():
    for n in (2, 3, 4):
        for _ in range(50):
            g = Game([CPUPlayer(str(i)) for i in range(n)], verbose=False)
            for _ in range(5000):
                if g.winner:
                    break
                g.play_turn()
            assert g.winner is not None
