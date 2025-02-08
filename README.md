# 競技プログラム作成自動化システム

このプロジェクトは、小規模な大会で競技プログラムの作成を自動化するシステムです。  
手動でのプログラム作成に多くの時間がかかるという問題を解決し、効率的な運用を支援します。

## 📌 プロジェクトの目的

- **競技プログラムの作成時間を短縮**  
  手作業で行われていた競技プログラム作成を自動化し、負担を軽減する。

## 🛠 機能

1. 競技プログラムの自動生成
2. ユーザーがカスタマイズ可能な設定
3. 出力形式の選択（PDF / CSV など）
4. 過去のデータを活用したプログラム最適化

## 🚀 インストール方法

# Git Fetch を活用した共同開発フロー

このプロジェクトでは、`git fetch` を用いてリモートの変更を取得しながら、円滑な共同開発を進めます。  
以下のコマンドを **一括実行するだけ** で、最新のコードを取得し、新しいブランチを作成し、作業完了後にプッシュする流れを自動化できます。

## **1回コピーするだけでOK！**
```sh
# 1. リポジトリをクローン（初回のみ）
git clone https://github.com/organization/project.git && cd project

# 2. 最新の変更を取得して main を最新にする
git fetch origin && git checkout main && git pull origin main

# 3. 作業ブランチを作成（作業内容に応じてブランチ名を変更してください）
BRANCH_NAME="feature-branch"
git checkout -b $BRANCH_NAME

# 4. コードを編集し、変更をコミット（適宜編集）
git add . && git commit -m "Implement feature X"

# 5. リモートの変更を取得して rebase（衝突がある場合は手動で解決）
git fetch origin && git rebase origin/main

# 6. 作業ブランチをリモートにプッシュ
git push origin $BRANCH_NAME

# 7. GitHub で Pull Request（PR）を作成する
echo "Pull Request を作成してください: https://github.com/organization/project/pulls"

# 8. PR 承認後、マージしたらブランチを削除
git branch -d $BRANCH_NAME && git push origin --delete $BRANCH_NAME