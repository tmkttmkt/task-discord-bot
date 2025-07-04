#!/bin/bash

# Docker Compose スクリプト for Discord Text Generator Bot (py-cord)

echo "=== Discord Text Generator Bot (py-cord) Docker Setup ==="

# .envファイルの確認
if [ ! -f .env ]; then
    echo "警告: .envファイルが見つかりません"
    echo ".env.exampleを参考に.envファイルを作成してください"
    echo ""
    echo "必要な環境変数:"
    echo "  DISCORD_TOKEN=your_discord_bot_token_here"
    echo ""
    read -p "続行しますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# データファイルの確認
if [ ! -f ./data/output2.json ]; then
    echo "警告: ./data/output2.jsonが見つかりません"
    echo "テキスト生成機能が正常に動作しない可能性があります"
fi

echo "Dockerイメージをビルドしています..."
docker-compose build

echo "コンテナを起動しています..."
docker-compose up -d

echo ""
echo "=== セットアップ完了 ==="
echo "Discord Bot (py-cord) が起動しました"
echo ""
echo "コマンド:"
echo "  docker-compose logs -f     # ログを表示"
echo "  docker-compose stop        # 停止"
echo "  docker-compose restart     # 再起動"
echo "  docker-compose down        # 停止して削除"
echo ""
echo "Discord Botコマンド:"
echo "  スラッシュコマンド（推奨）:"
echo "    /generate  # 🤖 AIテキスト生成"
echo "    /ping      # 🏓 応答時間確認" 
echo "    /info      # 📋 Bot情報表示"
echo ""
echo "  従来のプレフィックスコマンド:"
echo "    !generate  # テキスト生成"
echo "    !ping      # 応答時間確認"
