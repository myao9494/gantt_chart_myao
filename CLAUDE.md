# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

DHTMLX Ganttライブラリを使用したWebベースのガントチャートアプリケーションです。タスク、マイルストーン、進捗管理を含むプロジェクト管理機能を提供します。Node.js/Expressバックエンドと、データ永続化のためのMySQLデータベースを使用しています。

## 開発コマンド

### サーバー操作
- **サーバー起動**: `npm start` または `node server.js` (ポート1337で実行)
- **サーバー停止**: `lsof -i :1337`でPIDを確認し、`kill -9 <PID>`で停止

### データベース設定
- データベース名: `gantt_howto_node`
- テーブル: `gantt_tasks` と `gantt_links`
- 接続: localhost MySQL、ユーザー'root'でパスワード空
- サンプルスキーマは`gantt_howto_node_2023-08-27.sql`に格納

## アーキテクチャ

### バックエンド (server.js)
- **フレームワーク**: Express.js + promise-mysql によるデータベース操作
- **主要エンドポイント**:
  - `GET /data` - 日付フォーマット処理付きでタスクとリンクを取得
  - `POST/PUT/DELETE /data/task/:id` - タスクのCRUD操作
  - `POST/PUT/DELETE /data/link/:id` - タスクリンクのCRUD操作
- **日付処理**: Asia/Tokyoタイムゾーン用にmoment-timezoneを使用
- **セッション管理**: セキュアHTTPS用クッキーセッション設定

### フロントエンド (public/index.html)
- **ライブラリ**: DHTMLX Gantt v9.x + プラグイン（undo/redo、キーボードナビゲーション、マーカー、マルチセレクト）
- **カスタム機能**:
  - タイプ別フィルタ (task/pro/MS)、所有者、完了状況、日付範囲
  - タスク名とプロジェクト名の検索機能
  - 埋め込みカレンダーデータによるカスタムタスクスケジューリング
  - 印刷用クリーンモード
  - ネイティブブラウザーズーム対応のズームコントロール
  - タスク複製機能

### データモデル
タスクは以下の豊富なプロパティを持ちます:
- 標準フィールド: text, start_date, duration, progress, parent
- カスタムフィールド: kind_task, ToDo, task_schedule, folder, url_address, mail, memo, hyperlink, color, textColor, owner_id, edit_date

### 主要機能
- **タスクタイプ**: 3種類のビジュアルスタイリング（task=青、pro=橙、MS=紫円）
- **所有者管理**: 4つの所有者タイプ（自分、待、サイン取、他）とフィルタリング
- **スケジュール統合**: カレンダーイベント埋め込み用のカスタムtask_scheduleフィールド
- **階層タスク**: 親子関係とビジュアル階層表示
- **Undo/Redo**: Ctrl+Z/Ctrl+Shift+Zショートカットによる完全なundo/redo対応

## ファイル構造

### コアファイル
- `server.js` - メインサーバーアプリケーション
- `public/index.html` - メインフロントエンドアプリケーション
- `public/event.js` - カレンダーハイライト用イベント定義
- `public/holidays.js` - 週末ハイライト用祝日定義
- `public/schedule.js` - 追加スケジューリング機能

### アセット
- `public/css/` - カスタムDHTMLXテーマ修正を含むスタイリング
- `public/js/` - DHTMLX Ganttライブラリファイル
- `public/skins/` - カスタムbroadway_modテーマ付きDHTMLXテーマファイル

## 開発ガイドライン

### タスク管理
- タスクはsortorderフィールドで自動ソート
- 新しいタスクは最高のsortorderを取得し、親の最上位に移動
- タスク更新時に編集日時を自動追跡
- progress=1のタスクは翌日にend_dateが自動設定

### 日付処理
- データベースにはYYYY-MM-DD形式で日付を保存
- フロントエンドはAsia/Tokyo変換にmoment-timezoneを使用
- タスク期間はstart_date + durationから自動計算

### スタイリング規約
- タスクタイプには専用CSSクラス: .task、.pro、.ms
- 週末/祝日セルは.weekendクラスでスタイリング
- カスタムスケジュールイベントはスケジュールテキストから動的CSS生成

### データベース操作
- コネクションプーリングでpromise-mysqlを使用
- 全CRUD操作は標準化されたレスポンス形式を返す
- データ一貫性のためのトランザクション安全な操作

## テスト・デバッグ

### ブラウザー開発
- ブラウザー開発ツールでコンソールログを確認
- タスク操作は詳細情報とともにログ記録
- ネットワークタブで/dataエンドポイントへのAPI呼び出しを表示

### データベース検証
- MySQL にローカル接続してデータ永続化を確認
- データ整合性のためgantt_tasksとgantt_linksテーブルをチェック
- タスク階層はparentフィールドの関係で維持