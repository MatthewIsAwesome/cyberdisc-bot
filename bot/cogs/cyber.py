from typing import Iterable

from aiohttp import ClientSession
from discord import Embed, Message
from discord.ext.commands import Bot, Context, command

from bot.constants import CYBERDISC_ICON_URL, PWNED_ICON_URL


class Cyber:
    """
    Cyber Discovery/Security related commands.
    """

    def __init__(self, bot: Bot):
        self.bot = Bot

    def all_words_in_text(self, text: str, words: Iterable[str]):
        return all(word in text for word in words)

    def any_words_in_text(self, text: str, words: Iterable[str]):
        return any(word in text for word in words)

    def contains_words(self, text: str, all_words: Iterable[str], *any_words: Iterable[Iterable[str]]):
        all_words_check = self.all_words_in_text(text, all_words)
        any_words_check = all(self.any_words_in_text(text, words) for words in any_words)
        return all_words_check and any_words_check
    
    @command(aliases=["l", "lc"])
    async def level(self, ctx: Context, level_num: int, challenge_num: int):
        with open('headquarters.txt','r') as f:
            game_docs = [level.split(":::\n") for level in f.read().split(";;;;;;\n")]
        
        if level_num not in range(len(game_docs)):
            await ctx.send("Invalid level number!")

        elif challenge_num not in range(len(game_docs[level_num])):
            await ctx.send("Invalid challenge number!")
            
        else:
            challenge_raw = game_docs[level_num][challenge_num].splitlines()
            challenge_title = challenge_raw.pop(0)
            challenge_tip = challenge_raw.pop(-1)
            challenge_text = "\n".join(challenge_raw)
            embed = Embed(
                title=(f"Level {level_num} Challenge {challenge_num} - {challenge_title}"),
                description=challenge_text,
                colour=0x4262f4
            )
            embed.set_author(
                name="Cyber Discovery",
                icon_url=CYBERDISC_ICON_URL
            )
            embed.set_footer(text=challenge_tip)

            await ctx.send(embed=embed)

    @command()
    async def haveibeenpwned(self, ctx: Context, account: str):
        url = "https://haveibeenpwned.com/api/v2/breachedaccount/"

        async with ClientSession() as session:
            async with session.get(url + account) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    data = {}

        if data:
            await ctx.send(
                f"{ctx.author.mention}  |  Info from `https://haveibeenpwned.com/`. Showing up to **5** breaches (Total: "+str(len(data))+")"
            )
            for i in data[:5]:
                output = "```"
                output += f"Title: {i['Title']}\n"
                output += f"Name: {i['Name']}\n"
                output += f"Breach date: {i['BreachDate']}\n"
                output += f"PwnCount: {i['PwnCount']}\n"

                desc = i["Description"]
                desc = desc.replace("<a href=\"","").replace("\" target=\"_blank\" rel=\"noopener\">"," ").replace("</a>","")
                desc = desc.replace("&quot;", "\"")
                output += f"Description: {desc}\n"

                output += "Lost data: " + "/".join(i['DataClasses']) + "\n"
                output += f"Currently active: {i['IsActive']}\n"
                output += "```"
                await ctx.send(output)

        else:
            await ctx.send(f"{ctx.author.mention}  |  This account has never been breached!")
        
    @command()        
    async def hasitbeenpwned(self, ctx: Context, password: str):
        url = "https://api.pwnedpasswords.com/pwnedpassword/"

        async with ClientSession() as session:
            async with session.get(url + password) as response:
                if response.status == 200:
                    data = await response.text()
                else:
                    data = ""

        embed = Embed(
            name="have i been pwned?",
            description=f"{ctx.author.mention} | This password has ",
            colour=0x5DBCD2
        )
        embed.set_author(
            name="have i been pwned?",
            icon_url=PWNED_ICON_URL
        )

        if data:
            embed.description += f"been uncovered {data} times."
        else:
            embed.description += f"has never been uncovered."
        
        await ctx.send(embed=embed)

    async def on_message(self, message: Message):
        text = (message.content).lower()
        if self.contains_words(text, ["when", "game"], ["does", "will"], ["end", "finish", "close"]):
            await message.channel.send(f"{message.author.mention}  |  Cyberstart Game ends on the 29th May.")
        elif self.contains_words(text, ["when", "essentials"], ["?", "does", "will"], ["end", "finish", "close"]):
            await message.channel.send(f"{message.author.mention}  |  Cyberstart Essentials ends on the 18th June.")
        elif self.contains_words(text, ['how','elite','get','to']):
            await message.channel.send(f"{message.author.mention}  |  **Quote from the @CyberDiscUK Twitter: **Selection for CyberStart Elite will be based on a combination of Game and Essentials results.")

def setup(bot):
    bot.add_cog(Cyber(bot))
