import discord
import os
import sys
from pathlib import Path
import asyncio
from dotenv import load_dotenv

# data モジュールをインポート
sys.path.append('/app/src')
from data.main import Tetsu, Fumu

# .envファイルを読み込み
load_dotenv()

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

class TextGenerator:
    def __init__(self):
        self.tetsu = None
        self.is_initialized = False
        self.init_error = None
    
    async def initialize(self):
        """テキスト生成器を初期化（Bot起動後に呼び出し）"""
        if self.is_initialized:
            return
            
        try:
            print("テキスト生成器の初期化を開始...")
            self.f = Fumu(num=1)
            
            # 複数のパスを試行してデータファイルを探す
            possible_paths = [
                Path('/app/data/output2.json'),  # Docker環境
                Path('./data/output2.json'),     # 相対パス
                Path('./output2.json'),          # ルートディレクトリ
                Path('/app/src/data/output2.json'),  # src内のdata
                Path('/app/src/output2.json'),   # src内
            ]
            
            data_path = None
            for path in possible_paths:
                if path.exists():
                    data_path = path
                    print(f"データファイルが見つかりました: {data_path}")
                    break
            
            if data_path is None:
                # デバッグ情報を出力
                print("利用可能なパス:")
                import os
                current_dir = os.getcwd()
                print(f"現在のディレクトリ: {current_dir}")
                
                for root, dirs, files in os.walk('.'):
                    for file in files:
                        if 'output2.json' in file:
                            print(f"見つかったファイル: {os.path.join(root, file)}")
                
                self.init_error = f"データファイルが見つかりません。確認したパス: {[str(p) for p in possible_paths]}"
                print(self.init_error)
                return
            
            self.f.read_json(data_path)
            self.tetsu = Tetsu(self.f.date)
            self.is_initialized = True
            print("テキスト生成器が正常に初期化されました")
            
        except Exception as e:
            self.init_error = f"テキスト生成器の初期化に失敗しました: {e}"
            print(self.init_error)
    
    def generate_text(self):
        if not self.is_initialized:
            if self.init_error:
                return f"❌ 初期化エラー: {self.init_error}"
            else:
                return "⏳ テキスト生成器を初期化中です。しばらくお待ちください。"
        
        if self.tetsu is None:
            return "❌ テキスト生成器が利用できません。データファイルを確認してください。"
        
        try:
            return self.tetsu.create_text()
        except Exception as e:
            return f"❌ テキスト生成中にエラーが発生しました: {e}"

# テキスト生成器のインスタンス
text_generator = TextGenerator()

@bot.event
async def on_ready():
    print(f'{bot.user} がログインしました！')
    print(f'Bot ID: {bot.user.id}')
    
    # テキスト生成器を初期化
    await text_generator.initialize()
    
    print("スラッシュコマンドを同期中...")
    # スラッシュコマンドの同期（デプロイ時に重要）
    try:
        synced = await bot.sync_commands()
        print(f"スラッシュコマンドが同期されました: {len(synced)}個")
    except Exception as e:
        print(f"スラッシュコマンドの同期に失敗しました: {e}")
    print("Bot準備完了！")

@bot.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == bot.user:
        return
    if message.content.strip() == "課題嫌い!!!":
        await message.channel.send("わかるマーン!!!")
        return
    # Botがメンションされた場合
    if bot.user.mentioned_in(message):
        await message.reply("課題嫌い", mention_author=False)
        await message.channel.send("それはそうと課題滅ぶべし")
        return

@bot.slash_command(name="generate", description="AIによるテキストを生成します")
async def generate_text(ctx):
    """テキストを生成するスラッシュコマンド"""
    try:
        # まず応答してからテキスト生成を行う
        await ctx.respond("🤖 テキストを生成中です...", ephemeral=True)
        
        generated_text = text_generator.generate_text()
        embed = discord.Embed(
            title="🤖 生成されたテキスト",
            description=f"```\n{generated_text}\n```",
            color=0x00ff00
        )
        await ctx.followup.send(embed=embed)
        await ctx.followup.send("それはそうと課題滅ぶべし")
    except Exception as e:
        try:
            await ctx.followup.send(f"❌ エラーが発生しました: {e}")
        except:
            # フォローアップが失敗した場合は新しいメッセージを送信
            await ctx.send(f"❌ エラーが発生しました: {e}")

@bot.slash_command(name="ping", description="Botの応答時間を確認します")
async def ping(ctx):
    """Botの応答時間を確認するスラッシュコマンド"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"応答時間: **{latency}ms**",
        color=0x0099ff
    )
    await ctx.respond(embed=embed)

@bot.slash_command(name="info", description="Botの情報を表示します")
async def info(ctx):
    """Botの情報を表示するスラッシュコマンド"""
    embed = discord.Embed(
        title="🤖 Discord Text Generator Bot",
        description="MeCabを使用した日本語文章生成ボット",
        color=0x00ff00
    )
    embed.add_field(
        name="📋 利用可能なコマンド",
        value="`/generate` - テキスト生成\n`/ping` - 応答時間確認\n`/info` - Bot情報表示",
        inline=False
    )
    embed.add_field(
        name="⚙️ 技術スタック",
        value="• MeCab (日本語形態素解析)\n• py-cord\n• Python 3.11\n• Docker",
        inline=True
    )
    embed.add_field(
        name="🔧 機能",
        value="• マルコフ連鎖文章生成\n• スラッシュコマンド対応\n• エラーハンドリング",
        inline=True
    )
    await ctx.respond(embed=embed)

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("DISCORD_TOKENが設定されていません。環境変数を確認してください。")
        sys.exit(1)
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"Botの起動に失敗しました: {e}")
        sys.exit(1)