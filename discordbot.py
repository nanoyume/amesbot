from discord.ext import commands
from os import getenv
import traceback
import math

bot = commands.Bot(command_prefix='/')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command()
async def neko(ctx):
    await ctx.send('にゃーん')
    
@bot.command()
# 与えたダメージ, 残HP
async def 持越(ctx, damage: int, zan: int):
    # 430 , 100
    # (余剰ダメージ÷総ダメージ)×90+20
    overdamage = damage - zan
    time = (float(overdamage) / float(damage)) * 90.0 + 20.0
    time = int(math.ceil(time))
    await ctx.send('与えるダメージ：' + str(damage) + '万')
    await ctx.send('残りのHP：' + str(zan) + '万')
    await ctx.send('持ち越し時間は[ ' + str(time) + ' ]秒よ')

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
