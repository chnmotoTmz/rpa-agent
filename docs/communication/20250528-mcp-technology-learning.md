# [20250528] MCP技術調査: VS Code設定MCPサーバー機能理解

## 1. 目的/概要
*   プロジェクトルール（rule.md）に基づき、VS Code設定のMCPサーバー機能を調査
*   利用可能なMCP（Model Context Protocol）機能の全体把握
*   subprocess禁止ルールに従った直接的なAPI呼び出し手法の確立

## 2. 登場エージェント
*   **人間**: motoc
*   **AI**: GitHub Copilot

## 3. 対話サマリーと結果

### 3.1. GitHub Copilot: プロジェクトルールの確認
*   **人間のプロンプト**:
    ```
    C:\Users\motoc\rpa-agent\.github\rule.md まずどんなｍｃｐが呼べるか理解して
    ```
*   **AIの応答/提案**:
    ```
    rule.mdの内容確認：
    - 常にVS Code設定のMCPサーバーを使用すること
    - subprocess実行禁止
    - 直接的なスクリプト実装でエラー時のクラッシュによる問題明確化
    ```
*   **人間による評価/採用決定**:
    *   ルール理解は適切。MCP機能の調査を実施する方針で進行。

### 3.2. GitHub Copilot: MCP機能の全体調査
*   **人間のプロンプト**:
    ```
    利用可能なMCP機能を整理して説明せよ
    ```
*   **AIの応答/提案**:
    ```
    bb7_プレフィックス付きの豊富なMCP機能を6カテゴリに分類：
    1. ファイル・ディレクトリ操作（10機能）
    2. GitHub操作（11機能）
    3. LINE操作（6機能）
    4. ブラウザ操作（8機能）
    5. 検索機能（4機能）
    6. Redmine操作（4機能）
    ```
*   **人間による評価/採用決定**:
    *   包括的な機能調査結果を採用。RPA-Agentの要件に十分対応可能。

## 4. 技術仕様詳細

### 4.1. ファイル・ディレクトリ操作MCP
| 機能名 | 用途 | 重要度 |
|--------|------|--------|
| `bb7_read_file` | ファイル内容読み取り | ★★★ |
| `bb7_write_file` | ファイル作成・上書き | ★★★ |
| `bb7_edit_file` | 行ベース編集 | ★★★ |
| `bb7_create_directory` | ディレクトリ作成 | ★★ |
| `bb7_move_file` | ファイル移動・リネーム | ★★ |
| `bb7_list_directory` | ディレクトリ一覧 | ★★ |
| `bb7_directory_tree` | ツリー表示 | ★ |
| `bb7_search_files` | ファイル検索 | ★★ |
| `bb7_get_file_info` | ファイル詳細情報 | ★ |
| `bb7_read_multiple_files` | 複数ファイル読み取り | ★★ |

### 4.2. GitHub操作MCP
| 機能名 | 用途 | RPA-Agent適用度 |
|--------|------|----------------|
| `bb7_create_repository` | リポジトリ作成 | 高 |
| `bb7_push_files` | 複数ファイルプッシュ | 高 |
| `bb7_create_pull_request` | PR作成 | 高 |
| `bb7_create_issue` | Issue作成 | 中 |
| `bb7_fork_repository` | フォーク | 中 |
| `bb7_merge_pull_request` | PRマージ | 中 |
| `bb7_get_file_contents` | ファイル取得 | 高 |

### 4.3. ブラウザ操作MCP（RPA核心機能）
| 機能名 | 用途 | RPA重要度 |
|--------|------|----------|
| `bb7_browser_navigate` | ページ遷移 | ★★★ |
| `bb7_browser_screenshot` | スクリーンショット | ★★★ |
| `bb7_browser_click` | 要素クリック | ★★★ |
| `bb7_browser_type` | テキスト入力 | ★★★ |
| `bb7_browser_snapshot` | アクセシビリティ取得 | ★★★ |
| `bb7_browser_hover` | ホバー操作 | ★★ |
| `bb7_browser_wait` | 待機処理 | ★★ |
| `bb7_browser_press_key` | キー入力 | ★★ |

### 4.4. LINE操作MCP（通知機能）
| 機能名 | 用途 | 活用シーン |
|--------|------|----------|
| `bb7_push_text_message` | 個別テキスト送信 | 処理完了通知 |
| `bb7_push_flex_message` | 個別Flex送信 | リッチ通知 |
| `bb7_broadcast_text_message` | 一斉テキスト送信 | 緊急通知 |
| `bb7_get_profile` | プロフィール取得 | ユーザー識別 |

## 5. 決定事項とアクションアイテム
*   **決定事項**:
    1. subprocess禁止ルールに従い、全操作をMCP機能で実装
    2. ブラウザ操作MCPをRPA-Agentの核心機能として活用
    3. GitHub操作MCPで自動コミット・プッシュ機能を実装
    4. LINE操作MCPで処理結果通知機能を構築
*   **アクションアイテム**:
    1. ブラウザ操作MCP を使った画面操作スクリプトの設計
    2. GitHub自動プッシュ機能の実装
    3. LINE通知システムの構築
    4. ファイル操作MCPを使った設定管理システムの設計

## 6. 技術的制約と対応方針
*   **制約**: subprocess実行禁止
*   **対応**: 全てMCP APIで直接実行
*   **利点**: 
    - エラー時の問題明確化
    - より直接的な制御
    - VS Code環境との密接な統合

## 7. 補足/考察
*   MCP機能の豊富さにより、従来のsubprocessベースのRPAよりも安定性と可視性が向上
*   VS Code統合により、開発・デバッグ・実行が一元化される
*   bb7_プレフィックスの一貫性により、機能の発見と利用が容易
*   ブラウザ操作MCPの存在により、Webベースのタスク自動化が直接実装可能
