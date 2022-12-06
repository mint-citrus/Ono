from discord import Reaction, Emoji


def emphasize_print(*args):
    print("########################")
    print(args)
    print("########################")

async def extract_without_user(reactions: list[Reaction], 
                       emoji: Emoji, 
                       user: str):
    reaction = list(filter(lambda x: str(x.emoji) == emoji, reactions))
    return list(filter(lambda x: x.name != user,
                       [user async for user in reaction.users()]))