import discord
from discord.ext import commands
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
        try:
            self.f = Fumu(num=1)
            data_path = Path('/app/data/output2.json')
            if data_path.exists():
                self.f.read_json(data_path)
                self.tetsu = Tetsu(self.f.date)
                print("テキスト生成器が正常に初期化されました")
            else:
                print(f"データファイルが見つかりません: {data_path}")
                self.tetsu = None
        except Exception as e:
            print(f"テキスト生成器の初期化に失敗しました: {e}")
            self.tetsu = None
    
    def generate_text(self):
        if self.tetsu is None:
            return "テキスト生成器が利用できません。データファイルを確認してください。"
        
        try:
            return self.tetsu.create_text()
        except Exception as e:
            return f"テキスト生成中にエラーが発生しました: {e}"

# テキスト生成器のインスタンス
text_generator = TextGenerator()

@bot.event
async def on_ready():
    print(f'{bot.user} がログインしました！')
    print(f'Bot ID: {bot.user.id}')

@bot.slash_command(name="generate", description="AIによるテキストを生成します")
async def generate_text(ctx):
    """テキストを生成するスラッシュコマンド"""
    await ctx.defer()
    try:
        generated_text = text_generator.generate_text()
        embed = discord.Embed(
            title="🤖 生成されたテキスト",
            description=f"```\n{generated_text}\n```",
            color=0x00ff00
        )
        await ctx.followup.send(embed=embed)
    except Exception as e:
        await ctx.followup.send(f"❌ エラーが発生しました: {e}")

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

# 従来のプレフィックスコマンドも併用したい場合は以下を追加
@bot.command(name='gen', aliases=['g', 'text'])
async def generate_text_prefix(ctx):
    """テキストを生成するプレフィックスコマンド"""
    try:
        generated_text = text_generator.generate_text()
        embed = discord.Embed(
            title="🤖 生成されたテキスト",
            description=f"```\n{generated_text}\n```",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ エラーが発生しました: {e}")

@bot.command(name='p')
async def ping_prefix(ctx):
    """Botの応答時間を確認するプレフィックスコマンド"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"応答時間: **{latency}ms**",
        color=0x0099ff
    )
    await ctx.send(embed=embed)

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