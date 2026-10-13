"""起動用スクリプト。  python main.py"""
from uno.game import Game
from uno.player import CPUPlayer, HumanPlayer


def main() -> None:
    print("=== UNO ===")
    mode = input("モード: 1=CPUと対戦  2=2人で交代プレイ(同じPC) > ").strip()
    if mode == "2":
        p1 = input("プレイヤー1の名前 > ").strip() or "P1"
        p2 = input("プレイヤー2の名前 > ").strip() or "P2"
        players = [HumanPlayer(p1), HumanPlayer(p2)]
    else:
        name = input("あなたの名前 > ").strip() or "あなた"
        players = [HumanPlayer(name), CPUPlayer("CPU1"), CPUPlayer("CPU2")]
    Game(players).run()


if __name__ == "__main__":
    main()
