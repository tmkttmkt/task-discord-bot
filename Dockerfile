FROM python:3.11-slim

# 必要なシステムパッケージとMeCab本体をインストール
RUN apt-get update && apt-get install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    git \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "=== MeCab installation completed ==="

# MeCabの辞書パスを正しく設定
RUN echo "=== MeCab Setup Start ===" && \
    echo "Available dictionary directories:" && \
    find /usr /var -name "*dic*" -type d 2>/dev/null | grep -E "(ipadic|mecab)" || true && \
    find /usr -name "*ipadic*" -type d 2>/dev/null || true && \
    DICDIR=$(find /usr /var -name "ipadic-utf8" -type d 2>/dev/null | head -1) && \
    if [ -z "$DICDIR" ]; then \
        DICDIR="/var/lib/mecab/dic/ipadic-utf8"; \
        if [ ! -d "$DICDIR" ]; then \
            DICDIR="/usr/share/mecab/dic/ipadic-utf8"; \
        fi; \
        if [ ! -d "$DICDIR" ]; then \
            DICDIR="/usr/lib/x86_64-linux-gnu/mecab/dic/ipadic-utf8"; \
        fi; \
    fi && \
    echo "Using dictionary at: $DICDIR" && \
    if [ ! -d "$DICDIR" ]; then \
        echo "ERROR: Dictionary directory not found at $DICDIR" && \
        ls -la /usr/share/mecab/ || true && \
        ls -la /var/lib/mecab/ || true && \
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
    python3 -c "import MeCab; print('MeCab import successful'); t=MeCab.Tagger(); print('MeCab Tagger created successfully'); print('Test result:', t.parse('テスト').strip())" || \
    (echo "MeCab Python test failed, trying alternative setup..." && \
     python3 -c "import MeCab; t=MeCab.Tagger('-d /usr/share/mecab/dic/ipadic-utf8'); print('Alternative MeCab setup successful'); print('Test result:', t.parse('テスト').strip())")

# デフォルトコマンド
CMD ["python", "discord_bot.py"]
