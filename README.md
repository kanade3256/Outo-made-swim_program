# 競技プログラム作成自動化システム

このプロジェクトは、小規模な大会で競技プログラムの作成を自動化するシステムを作成するプロジェクトである。  
手動での競技プログラム作成に多くの時間がかかるという問題を解決し、効率的な運用を支援する。

---

## プロジェクトの目的

- **競技プログラムの作成時間を短縮**  
  手作業で行われていた競技プログラム作成を自動化し、作成にかかる負担を軽減することが目的。

---

## 機能

1. **競技プログラムの自動生成**  
   自動でプログラムを生成し、効率化を実現する。
2. **ユーザーがカスタマイズ可能な設定**  
   ユーザーのニーズに合わせた柔軟な設定が可能である。
3. **出力形式の選択**  
   CSVで出力予定
4. **過去のデータを活用したプログラム最適化**  
   過去の実績データを基に、より良いプログラム作成をサポートする。

---

## 作業ルール
- 機能実装の時は必ずブランチを分けて実装する
- 修正の時は、’modify/修正内容’
- 新機能の場合は、’feature/新機能名’
- 新たに関数を作成した場合、その関数の機能について説明をコメントにて書く

```sh
#example
def test():
   """
   'this is test' と出力する関数
   """
   print("this is test")
   return 0
```

---
## gitの使い方

```sh
# 1. リポジトリをクローン（初回のみ）
git clone https://github.com/kanade3256/Outo-made-swim_program.git

# 2. 最新の変更を取得して main を最新にする
git fetch origin

# 3. 作業ブランチを作成（作業内容に応じてブランチ名を変更してください）
#BRANCH_NAME="feature-branch"とする
git checkout -b $BRANCH_NAME
git switch $BRANCH_NAME
# または
git switch -c $BRANCH_NAME

# 4. コードを編集し、変更をコミット（適宜編集）
git add .
git commit -m "Implement feature X"

# 5. 作業ブランチをリモートにプッシュ
git push origin $BRANCH_NAME
```

