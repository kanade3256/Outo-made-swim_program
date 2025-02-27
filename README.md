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
cd Outo-made-swim_program

# 2. 最新の変更を取得して main を最新にする
git checkout main  # または git switch main
git pull origin main  # 最新の変更を取得（fetch + merge）

# 3. 作業ブランチを作成
BRANCH_NAME="feature-branch"
git switch -c $BRANCH_NAME  # checkout -b よりも switch -c のほうが推奨

# 4. コードを編集し、変更をコミット
git add .
git commit -m "Implement feature X"

# 5. 作業ブランチをリモートにプッシュ（upstream 設定）
git push -u origin $BRANCH_NAME

```

## 使用フロー

1. **ExcelからCSVへの変換・結合**  
   `scripts/excel_to_merged_csv.py` を実行すると、指定フォルダ内のExcelファイルから必要なシートを取得し、CSVファイルとして出力した後、複数のCSVを結合して `merged_output.csv` を生成します。

2. **正規化・タイムフォーマット変換**  
   `scripts/data_convert.py` を実行して、結合後のCSVファイルを読み込み、全角スペース・カタカナの半角化などのテキスト正規化やタイム表記の変換を行い、変換後のCSVファイルを出力します。

3. **最終的なプログラム作成・ソート処理**  
   `src/main.py` を実行し、正規化済みのCSVを読み込んで選手情報をオブジェクト化し、種目ごとのタイムをソートします。大会の競技プログラム作成やランキング作成などが行われる想定です。
