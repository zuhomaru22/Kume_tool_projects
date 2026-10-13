# UNO (Python)

ターミナルで遊べるUnoです。標準ライブラリのみで動きます(テストだけ pytest)。

## 遊び方
```bash
python main.py
```

## テスト
```bash
pip install -r requirements.txt
pytest
```

## ファイル構成
| ファイル | 役割 |
|---|---|
| `uno/card.py` | カード・デッキ |
| `uno/player.py` | 人間 / CPU のプレイヤー |
| `uno/game.py` | ルール・ターン進行 |
| `main.py` | 起動・モード選択 |
| `tests/` | テスト |

## ルール(簡易)
- 手札7枚、先に手札を無くした人の勝ち
- 出せないときは山札から1枚引く(出せるなら出してもOK)
- ドロー2 / ワイルドドロー4 の重ね出しは無し
- ワイルドドロー4はいつでも出せる

## 共同開発の流れ
1. `main` に直接pushせず、`feature/xxx` ブランチを切る
2. 小さくコミット → push → Pull Request
3. 相方がレビューしてマージ

## 今後のアイデア
- [ ] UNO宣言を忘れたら2枚引くペナルティ
- [ ] ドロー2の重ね出し
- [ ] CPUを賢くする
- [ ] ネット対戦 / GUI(pygame, tkinter)
