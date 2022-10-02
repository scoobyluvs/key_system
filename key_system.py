import discord, sqlite3 , rstr
from discord.ext import commands


# change yo shi here
token = 'your_token_here'
mods = ['mods here', 'other_mod_here']
prefix = '.'

# dont change unless yk what ur doing
intents = discord.Intents.all()
activity = activity = discord.Game(name="made by scooby#0001")
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None, activity=activity,status=discord.Status.idle)


DB=sqlite3.connect("Bot_DB.db")
query=DB.cursor()
query.execute("""CREATE TABLE IF NOT EXISTS KEYS (
        UNQ_ID PRIMARY KEY,
        USER_ID NUMBER,
        VAILD NUMBER,
        CLAIMED_KEY VARCHAR2
);""")


def check_Mod(ctx):
    if ctx.author.id in modList:
        IsMod = True
    else:
        IsMod = False
    return IsMod


# gen yo key

@bot.command()
async def genkey(ctx):
    IsMod = check_Mod(ctx)
    if IsMod == False:
        embed=discord.Embed(title="Demon V2", description="You have no perms to use this command.", color=0xd70f0f)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/818895366740115466/1006291408375795773/gif44.gif")
        embed.set_footer(text="#8k.HITTAS | scooby#0001")
        await ctx.send(embed=embed)
    else:
        new_key=rstr.xeger(r'[a-zA-Z\d]{25}')
        query.execute("""INSERT INTO KEYS (USER_ID, CLAIMED_KEY) VALUES (?, ?)""",(ctx.author.id, new_key,))
        DB.commit()
        embed=discord.Embed(title="Key generated!", description=f"Your new key is **{new_key}**", color=0xf8f7f7)
        await ctx.send(embed=embed)


# key redeem

@bot.command()
async def redeem(ctx, key):
    if isinstance(key, commands.MissingRequiredArgument):
        await ctx.send('Inccorrect arguments entered | **.redeem <key>**')
    query.execute("""SELECT CLAIMED_KEY FROM KEYS WHERE CLAIMED_KEY=?""",(key,))
    list_keys = [row[0] for row in query.fetchall()]
    if key in list_keys:
        embed=discord.Embed(title="Demon V2", description=f"Claimed the key !", color=0xf8f7f7)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/818895366740115466/1006291408375795773/gif44.gif")
        embed.set_footer(text="#8k.HITTAS | scooby#0001")
        await ctx.send(embed=embed)
        query.execute("""DELETE FROM KEYS WHERE CLAIMED_KEY=?""",(key,))
        query.execute("""INSERT INTO KEYS (VAILD) VALUES (?)""",(ctx.author.id,))
        DB.commit()
    else:
        embed=discord.Embed(title="Demon V2", description="Invaild Key / The key doesn't exist.", color=0xf8f7f7)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/818895366740115466/1006291408375795773/gif44.gif")
        embed.set_footer(text="#8k.HITTAS | scooby#0001")
        await ctx.send(embed=embed)



# how to check if user has a key 

@bot.command()
async def test(ctx):
    query.execute("""SELECT VAILD FROM KEYS WHERE VAILD=?""",(ctx.author.id,))
    result = [row[0] for row in query.fetchall()]
    if ctx.author.id in result:
        pass
    else:
        embed=discord.Embed(title="Demon v2 | buy @ scooby#0001", description="You have no key to Demon V2" + '\n' +  "Buy @ scooby#0001", color=0xf8f7f7)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/818895366740115466/1006291408375795773/gif44.gif")
        embed.set_footer(text="Demon V2 | scooby#001")
        await ctx.send(embed=embed)
        return


bot.run(token)