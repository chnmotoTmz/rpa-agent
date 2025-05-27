# MCP技術学習ノート

## 概要
Model Context Protocol (MCP) の技術仕様と利用可能機能についての学習記録

## 基本概念
- **MCP**: Model Context Protocolの略称
- **VS Code統合**: VS Code設定のMCPサーバーを使用
- **直接API呼び出し**: subprocessを使わない直接的な制御
- **bb7_プレフィックス**: 全MCP機能の統一命名規則

## 利用可能機能一覧（43機能）

### 📁 ファイル・ディレクトリ操作（10機能）
```
bb7_read_file               - ファイル内容読み取り
bb7_write_file              - ファイル作成・上書き  
bb7_edit_file               - 行ベース編集
bb7_create_directory        - ディレクトリ作成
bb7_move_file               - ファイル移動・リネーム
bb7_list_directory          - ディレクトリ一覧表示
bb7_directory_tree          - ディレクトリツリー表示
bb7_search_files            - ファイル検索
bb7_get_file_info           - ファイル詳細情報取得
bb7_read_multiple_files     - 複数ファイル同時読み取り
```

### 🌐 GitHub操作（11機能）
```
bb7_create_repository       - リポジトリ作成
bb7_fork_repository         - リポジトリフォーク
bb7_create_branch           - ブランチ作成
bb7_create_pull_request     - プルリクエスト作成
bb7_get_pull_request        - プルリクエスト取得
bb7_merge_pull_request      - プルリクエストマージ
bb7_list_issues             - Issues一覧
bb7_create_issue            - Issue作成
bb7_update_issue            - Issue更新
bb7_push_files              - 複数ファイルプッシュ
bb7_get_file_contents       - GitHubファイル取得
```

### 💬 LINE操作（6機能）
```
bb7_push_text_message       - テキストメッセージ送信
bb7_push_flex_message       - Flexメッセージ送信
bb7_broadcast_text_message  - テキスト一斉送信
bb7_broadcast_flex_message  - Flex一斉送信
bb7_get_profile             - ユーザープロフィール取得
bb7_get_message_quota       - メッセージ配信数確認
```

### 🌐 ブラウザ操作（8機能）- RPA核心機能
```
bb7_browser_navigate        - ページ遷移
bb7_browser_screenshot      - スクリーンショット
bb7_browser_click           - 要素クリック
bb7_browser_type            - テキスト入力
bb7_browser_hover           - 要素ホバー
bb7_browser_snapshot        - アクセシビリティスナップショット
bb7_browser_wait            - 待機処理
bb7_browser_press_key       - キー入力
```

### 🔍 検索機能（4機能）
```
bb7_search_repositories     - GitHub リポジトリ検索
bb7_search_code             - GitHub コード検索
bb7_search_issues           - GitHub Issues検索
bb7_search_users            - GitHub ユーザー検索
```

### 📋 Redmine操作（4機能）
```
bb7_redmine_request         - Redmine API リクエスト
bb7_redmine_upload          - ファイルアップロード
bb7_redmine_download        - ファイルダウンロード
bb7_redmine_paths_list      - API パス一覧
bb7_redmine_paths_info      - API 詳細情報
```

## RPA-Agent実装での活用パターン

### 基本的なワークフロー
1. **画面操作**: `bb7_browser_*` 系機能
2. **ファイル処理**: `bb7_*_file` 系機能  
3. **結果保存**: `bb7_push_files` でGitHub保存
4. **通知**: `bb7_push_text_message` でLINE通知

### エラーハンドリング
- subprocessを使わないため、エラー時は直接クラッシュ
- 問題箇所の特定が容易
- VS Code環境での直接デバッグが可能

## 技術的利点
1. **安定性**: subprocess実行なしによる安定動作
2. **可視性**: VS Code統合によるデバッグ容易性
3. **直接性**: API直接呼び出しによる高速処理
4. **統合性**: 開発・実行・デバッグの一元化

## 学習日
2025年5月28日
