import asyncio
import random
from enum import Enum
import logging

import discord
from discord.ext import commands

import theme


class WordwolfError(Exception):
    pass


class Status(Enum):
    Setting      = 1
    MeetingStart = 2
    MeetingEnd   = 3
    Aggregating  = 4
    Finnished    = 5

    def __new__(cls, value: int):
        status = object.__new__(cls)
        status._value_ = value
        return status
        
    def __int__(self) -> int:
        return self.value

class Room:
    def __init__(self) -> None:
        self._status = Status.Setting
        self._players = []
        self._wolves = []
        self._villagers = []
        self.ballot_box = {}
        self._wolf_theme = None
        self._villager_theme = None
    
    @property
    def players(self):
        return self._players

    @property
    def wolf_theme(self):
        return self._wolf_theme
    
    @property
    def villager_theme(self):
        return self._villager_theme

    @property
    def wolves(self):
        return self._wolves
    
    @property
    def villagers(self):
        return self._villagers

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        if self._status == Status.Setting:
            return "ゲームを開始します"
        elif self._status == Status.MeetingStart:
            return "会議中です"
        elif self._status == Status.MeetingEnd:
            return "会議が終了しました"
        elif self._status == Status.Aggregating:
            return "集計中です"
        else: # Finnished
            return "ゲームは終了しました"

    def register(self, members):
        self._players = members
        logging.debug(f"players who will participant the game are : {self.players}")
            
    def unregister(self, name):
        if name in self.players:
            self._players -= [name]

    def _divide(self):
        wolf = random.choice(self._players)
        players = []
        for p in self._players:
            if p != wolf:
                players.append(p)
        self._wolves = [wolf]
        self._villagers = players
        logging.debug(f"wolf : {[wolf]}, players : {players}")
        return wolf, players

    def start(self):
        self._divide()
        themes = theme.select()
        random.shuffle(themes)
        self._villager_theme = themes[0]
        self._wolf_theme = themes[1]
        logging.debug("game room has started")

    def end(self):
        logging.debug("game has ended")

    def get_vote(self, to_player, from_plyaer):
        self.ballot_box[from_plyaer] = to_player

    def aggregate(self, votes):
        self._votes = votes
        for whom, from_who in votes.items():
            self.get_vote(whom, from_who)

    def _get_same_votes(self, number, votes):
        # ex: votes == [(A, 3), (B, 1), (C, 0)]
        return list(filter(lambda x: x[1] == number, votes))

    def disclose(self):
        # 最も得票した順番に返す
        votes = self._votes
        if votes == {}:
            raise WordwolfError("votes is empty")
        sorted_vote = sorted(votes.items(), key = lambda x : x[1], reverse=True)
        most_number = sorted_vote[0][1]
        return self._get_same_votes(most_number, sorted_vote)
        

def create_room():
    return Room()

def register_players(room, players):
    for player in players:
        room.register(player)


class Wolf(commands.Cog):
    emoji = {"wolf" : "🐺", "ok": "🆗", "check" : "✅"}
    meeting_time = 180

    def __init__(self, bot) -> None:
        self.bot = bot
    
    def _has_checked(self, message):
        reaction_emoji = list(map(str, message.reactions))
        ret = Wolf.emoji["check"] in reaction_emoji
        return ret

    async def _send_theme_for_players(self, players, themes):
        for player in players:
            dm = await player.create_dm()
            await dm.send(f"あなたの今回のお題は{themes}です")

    async def _send_theme(self, room: Room):
        await self._send_theme_for_players(room.wolves, room.wolf_theme)
        await self._send_theme_for_players(room.villagers, room.villager_theme)

    @commands.command()
    async def wordwolf(self, ctx, *_args):
        room = create_room()

        # TODO: embed messageにする
        start_msg = await ctx.send("ゲームを開始します\n参加する人は🐺を、準備ができたら🆗をリアクションしてください")

        try:
            ok_reaction, _ = await self.bot.wait_for(
                "reaction_add", 
                timeout=180,
                check=lambda reaction, _: str(reaction.emoji) == Wolf.emoji["ok"])
        except asyncio.TimeoutError:
            pass
        wolf_reaction = list(filter(lambda x: str(x) == Wolf.emoji["wolf"], ok_reaction.message.reactions))[0]
        players = [user async for user in wolf_reaction.users()]
        if len(players) < 3:
            await ctx.send("時間内に人数が集まりませんでした...")

        async with ctx.typing():
            room.register(players)
            room.start()
            await self._send_theme(room)

        meet = "話し合いをしてください！\n" + \
            "終了するときはこのメッセージに✅をリアクションしてください"
        time_msg = f"残り時間は{self.meeting_time}です"
        meet_msg = await ctx.send(content=meet+time_msg)

        while self.meeting_time >= 0:
            updated_meet_msg = await ctx.fetch_message(meet_msg.id)
            if self._has_checked(updated_meet_msg):
                room.end()
                break
            await asyncio.sleep(1)
            self.meeting_time -= 1
            logging.debug(f"meeting time is {self.meeting_time}")
            await meet_msg.edit(content = meet + \
                f"残り時間は{self.meeting_time}です")

        poll_message = "次の中から人狼だと思う人の番号を書いてください！"
        for i, player in enumerate(room.players):
            poll_message += f"\n{i} : {player}"
        for player in room.players:
            await player.dm_channel.send(poll_message)
        await ctx.send("DMにて投票してください")

        messages = []
        while len(messages) != len(room.players):
            messages.clear()
            for player in room.players:
                async for message in player.dm_channel.history(limit=1):
                    messages += [message]
            messages = list(filter(lambda m: m.content.isdecimal(), messages))

        votes = {}
        for m in messages:
            n = int(m.content)
            voted_player = room.players[n]
            if voted_player in votes.keys():
                votes[voted_player] += 1
            else:
                votes[voted_player] = 1
        room.aggregate(votes)
        results = room.disclose() # ex) result == [(A, 3), (B, 2),,,]

        content = ""
        for result in results:
            player = result[0]
            name = player.display_name
            content += f"{name}さん\n"
        await ctx.send("投票結果は\n" + content + "でした!")

        elected_member = results[0][0]
        elected_member_name = elected_member.display_name
        if elected_member in room.wolves:
            await ctx.send(f"{elected_member_name}さんは人狼でした\n村人側の勝ちです!")
        else:
            await ctx.send(f"{elected_member_name}さんは村人でした\n人狼側の勝ちです!")
        
        await ctx.send(
            f"人狼のお題 : {room.wolf_theme}" + \
            f"村人のお題 : {room.villager_theme}" + \
            f"人狼役　   : {room.wolves}"
                )

async def setup(bot):
    await bot.add_cog(Wolf(bot))