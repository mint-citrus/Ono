from urllib import request
import json
from pprint import pprint

import discord
from discord.ext import commands

class Result:
    def __init__(self, json) -> None:
        rules = json["result"]
        for rule in rules:
            ...


res = request.urlopen("https://spla3.yuu26.com/api/schedule")
content = res.read()

js = json.loads(content)
r = Result(js)

class Splatoon3Info(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def splatoon(self, ctx: commands.Context):
        content = "現在のサーモンランNWの情報はこちら！"
        async with ctx.typing():
            await ctx.send(content=content)
            