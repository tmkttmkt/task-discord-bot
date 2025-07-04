# Discord Text Generator Bot

MeCab を使用した日本語文章生成機能付き Discord ボット（py-cord 使用）

## 特徴

- **py-cord** による最新 Discord API 対応
- **スラッシュコマンド** + 従来のプレフィックスコマンド両対応
- MeCab による日本語形態素解析
- マルコフ連鎖による文章生成
- 美しい Embed メッセージ
- Docker 完全対応
- 一つのコンテナで統合実行

## 必要なもの

- Docker & Docker Compose
- Discord Bot Token

## セットアップ

### 1. リポジトリをクローン

```bash
git clone <repository-url>
cd newdisc
```

### 2. 環境変数設定

```bash
cp .env.example .env
```

`.env`ファイルを編集して Discord Bot Token を設定:

```
DISCORD_TOKEN=your_discord_bot_token_here
```

### 3. データファイル配置

`data/output2.json`に学習データを配置してください。

### 4. 起動

#### Windows:

```cmd
start.bat
```

#### Linux/Mac:

#### Linux/Mac:

```bash
chmod +x start.sh
./start.sh
```

#### 手動起動:

```bash
docker-compose up -d
```

## 使用方法

### Discord コマンド

#### スラッシュコマンド（推奨）

- `/generate` - 🤖 AI テキスト生成
- `/ping` - 🏓 Bot 応答時間確認
- `/info` - 📋 Bot 情報表示

#### 従来のプレフィックスコマンド

- `!generate` または `!g` - テキスト生成
- `!ping` - Bot 応答時間確認

### Docker 管理コマンド

```bash
# ログ確認
docker-compose logs -f

# 停止
docker-compose stop

# 再起動
docker-compose restart

# 完全削除
docker-compose down
```

## 構成

- **Discord Bot**: `discord_bot.py` (py-cord + スラッシュコマンド)
- **Text Generator Service**: `text_generator_service.py`
- **Data Processing**: `data/main.py`, `data/date.py`
- **Docker**: 統合 Dockerfile + docker-compose.yml

## 技術スタック

- Python 3.11
- **py-cord** (最新 Discord API 対応)
- **スラッシュコマンド** + 従来のプレフィックスコマンド
- MeCab + mecab-python3
- Docker & Docker Compose
- マルコフ連鎖文章生成
- 美しい Embed メッセージ

## トラブルシューティング

### よくある問題

1. **Bot が応答しない**

   - DISCORD_TOKEN が正しく設定されているか確認
   - Bot がサーバーに招待されているか確認
   - アプリケーションで Slash Commands の権限が有効になっているか確認

2. **スラッシュコマンドが表示されない**

   - Bot を再招待（applications.commands スコープ付き）
   - 数分待ってから Discord クライアントを再起動

3. **文章生成ができない**

   - `data/output2.json`ファイルが存在するか確認
   - ファイルの形式が正しいか確認

4. **MeCab エラー**
   - Docker イメージを再ビルド: `docker-compose build --no-cache`

### ログ確認

```bash
docker-compose logs discord-text-bot
```
