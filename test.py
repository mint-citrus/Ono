import asyncio

import discord
from discord.ext import commands


async def dm(self, ctx, *args):
    author = ctx.author
    await author.create_dm()
    await author.dm_channel.send("This message is a Test.")


async def res(self, ctx, *args):
    sent_message = await ctx.send("Waiting for response...")
    try:
        res = await self.bot.wait_for(
            "message",
            check=lambda x: x.channel.id == ctx.channel.id
                            and ctx.author.id == x.author.id
                            and x.content.lower() == "yes"
                            or x.content.lower() == "no",
            timeout=10.0) # 秒数
    except TimeoutError:
        await sent_message.edit(content=f"{ctx.author} reply nothing...")

    if res.content.lower() == "yes":
        await sent_message.edit(content=f"{ctx.author} said yes!")
    else:
        await sent_message.edit(content=f"{ctx.author} said no!")


async def stop(self, ctx, *args):
    await ctx.send("10秒待ちます")
    await asyncio.sleep(10)
    await ctx.send("10秒くらいたったよ")


async def emoji(self, ctx, *args):
    # emojiのstrを返す
    await ctx.send("Add reaction at this message")
    reaction, _ = await self.bot.wait_for("reaction_add")
    await ctx.send(str(reaction.emoji))


async def embed(self, ctx, *args):
    # embed messageの送り方を調べる
    embed = discord.Embed(title="Sample Embed", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)


async def react(self, ctx, *args):
    # reactionを使っていろいろ確かめる
    await ctx.send("Enter the message id")
    msg = await self.bot.wait_for("message", check=lambda m: m.content.isnumeric())
    tgt = await ctx.fetch_message(int(msg.content))
    await ctx.send(f"{tgt.reactions}")


async def fetch(self, ctx: commands.Context, *args):
    msg = await ctx.send("Please type 'ok' ")
    await self.bot.wait_for("message", check=lambda m: m.content == "ok")
    result = await msg.fetch()
    await ctx.send(result)

_test_functions = [dm, res, stop, emoji, embed, react, fetch]

class Test(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def test(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Command name is needed")
            return 
        try:
            command = args[0]
            await [func for func in _test_functions if func.__name__ == command][0](self, ctx, *args)
        except IndexError:
            await ctx.send(f"that \"{args[0]}\" command is not prepared.\n here is not something funny :\\")


async def setup(bot):
    await bot.add_cog(Test(bot))