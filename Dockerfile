FROM python:3.11-slim

# 必要なシステムパッケージとMeCab本体をインストール
RUN apt-get update && apt-get install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# MeCabの辞書パスを正しく設定
RUN echo "=== MeCab Setup Start ===" && \
    DICDIR="/var/lib/mecab/dic/ipadic-utf8" && \
    echo "Using dictionary at: $DICDIR" && \
    if [ ! -d "$DICDIR" ]; then \
        echo "ERROR: Dictionary directory not found at $DICDIR" && \
        echo "Available dictionary directories:" && \
        find /usr /var -name "*dic*" -type d 2>/dev/null | grep -E "(ipadic|mecab)" && \
        exit 1; \
    fi && \
    mkdir -p /usr/local/etc && \
    echo "dicdir = $DICDIR" > /usr/local/etc/mecabrc && \
    echo "userdic = " >> /usr/local/etc/mecabrc && \
    echo "=== Created mecabrc ===" && \
    cat /usr/local/etc/mecabrc && \
    echo "=== Testing MeCab CLI ===" && \
    echo "こんにちは" | mecab && \
    echo "=== MeCab Setup Complete ==="

# MeCabの環境変数を設定
ENV MECABRC=/usr/local/etc/mecabrc

# Pythonの依存関係をインストール
COPY requirements-discord-bot.txt requirements-text-generator.txt ./
RUN pip install --no-cache-dir mecab-python3
RUN pip install --no-cache-dir -r requirements-discord-bot.txt
RUN pip install --no-cache-dir -r requirements-text-generator.txt

# アプリケーションコードをコピー
WORKDIR /app/src
COPY . .

# データディレクトリを作成
RUN mkdir -p /app/data

# MeCab Python テスト
RUN echo "=== Testing Python MeCab ===" && \
    python3 -c "import MeCab; print('MeCab import successful'); t=MeCab.Tagger(); print('MeCab Tagger created successfully'); print('Test result:', t.parse('テスト').strip())"

# デフォルトコマンド
CMD ["python", "discord_bot.py"]
