from discord.ext import commands
from os import getenv
from discord_slash import SlashCommand, SlashContext
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

# 持ち越し時間の計算
# 引数：与えるダメージ, 今の残HP
@bot.command()
async def 持越(ctx, damage: int, zan: int):
    outstr = '与えるダメージ：' + str(damage) + '万\n'
    outstr += '残りのHP：' + str(zan) + '万\n'

    if damage < zan:
        await ctx.send(outstr + '倒せてないわ')
        return

    # (余剰ダメージ÷総ダメージ)×90+20
    overdamage = damage - zan
    time = (float(overdamage) / float(damage)) * 90.0 + 20.0
    time = int(math.ceil(time))

    if 90 < time:
        time = 90

    await ctx.send(outstr + '持ち越し時間は[ ' + str(time) + ' ]秒よ')

# TL秒数改変
@bot.command()
async def TL(ctx, time: int, tlstr: str):
    orgtime = []
    counter = 1
    for num in range(90):
        Minutes = math.floor(counter / 60)
        Seconds = counter % 60
        if Seconds < 10:
            orgtime.append(str(Minutes) + ':0' + str(Seconds))
        else:
            orgtime.append(str(Minutes) + ':' + str(Seconds))
        counter += 1

    convertime = []
    counter = 89
    for num in range(90):
        Minutes = math.floor((time - counter) / 60)
        Seconds = (time - counter) % 60
        if Minutes < 0:
            convertime.append('0:00')
        elif Seconds < 10:
            convertime.append(str(Minutes) + ':0' + str(Seconds))
        else:
            convertime.append(str(Minutes) + ':' + str(Seconds))
        counter -= 1

    sp = tlstr.split('\n')

    outstr = '持ち越し時間でTLを書き換えたわ'
    outstr += '```c++\n'
    for val in sp:
        for num in range(90):
            val = val.replace(orgtime[num], convertime[num])

        if val.startswith('0:00'):
            break

        outstr += val
        outstr += '\n'

    outstr += '```'
    await ctx.send(outstr)

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
