# tool.py - ミニ便利ツール
print("=== ミニ便利ツール ===")
print("1: あいさつ")
print("9: 終了")

choice = input("メニュー番号を入力してください: ")

if choice == "1":
    print("こんにちは！Gitチーム開発演習中です。")
elif choice == "9":
    print("終了します。")
else:
    print("未対応のメニューです。")