import asyncio
import sys

import discord
from discord.ext import commands

from timer import TimerList

try: 
    from setting import TOKEN, PREFIX, ADMIN, BOT_CHANNEL_IDs
except ModuleNotFoundError:
    print("setting file is not found")
    sys.exit(0)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


_is_mute_vc_message = False


@bot.event
async def on_ready():
    print(f"{bot.user} is ready")


def _get_bot_channel(member):
    if BOT_CHANNEL_IDs is None:
        raise Exception("BOT_CHANNEL_IDs is not setted.")
        
    ids = [channel.id for channel in member.guild.channels]
    bot_channel_id = set(BOT_CHANNEL_IDs) & set(ids)
    if len(bot_channel_id) == 0:
        raise Exception("The bot does not have own channel")
    channel = bot.get_channel(bot_channel_id.pop())
    return channel


@bot.event
async def on_voice_state_update(member, before, after):
    """
    誰かが来たら、{}さんが来ました！ 
    消えたら、{}さん、またね！
    と返す
    """
    if _is_mute_vc_message:
        return
    channel = _get_bot_channel(member)
    
    if before.channel is None and after.channel is not None:
        await channel.send(f"{member.display_name}さんが参加しました！")
    else:
        await channel.send(f"{member.display_name}さん、またね！")


@bot.command()
async def say(ctx, *args):
    # 言葉をそのまま返す
    if args == "":
        return
    arg = " ".join(args)
    await ctx.send(arg)


@bot.command()
async def timer(ctx, *args):
    # 時間を計る
    user = ctx.author.name
    if TimerList.is_new(user):
        TimerList.append(user)
        await ctx.send("タイマースタート!")
    else:
        timer = TimerList.pop(user)
        result_time = timer.stop()
        await ctx.send(f"時間は{result_time}でした！")


@bot.command()
async def halt(ctx, *args):
    if ctx.author.id == ADMIN:
        await bot.close()
        sys.exit(0)
    else:
        await ctx.send(f"{bot.user}は知らんぷりしている...")


@bot.command()
async def nube(ctx):
    await ctx.send("ぬべぢょん")
    await ctx.author.create_dm()
    await ctx.author.dm_channel.send("ぬべぬべ")


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(bot.load_extension("test"))
    asyncio.run(bot.load_extension("wolf"))
    bot.run(TOKEN)
