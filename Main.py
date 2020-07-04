import discord
from discord.utils import get
import hypixel
from discord.guild import Guild
from discord import Member
import time
from discord.ext import commands
import json
import requests

print(discord.__version__)

with open('BotToken.txt', "r") as f:
    TOKEN = f.read()

with open('apikey.txt', "r") as f:
    APIKEY = f.read()

client = commands.Bot(command_prefix='/')

hypixel.setKeys([APIKEY])

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return

    if message.content.startswith('Hi'):
        msg = 'Hello there {0.author.mention}'.format(message)
        await channel.send(msg)
    await client.process_commands(message)

@client.command(pass_context=True)
async def link(ctx, username=None):
    message = ctx.message
    username = username
    user = ctx.message.author
    discord_tag = None
    # TODO: use UUID instead
    MojangAPI = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    
    try:
        # TODO: #2 use UUID instead
        player = hypixel.Player(username)
        player_info = player.getPlayerInfo()
    except:
        await ctx.send(f"{message.author.mention}")
        await ctx.send("Invalid username (or there's a problem in the hypixel api)")
        return
    try:
        discord_tag = player_info["socialMedia"]["links"]["DISCORD"]
    except:
        pass

    if discord_tag == str(message.author):
        linkSuccess = discord.Embed(color=0x00FF00)
        linkSuccess.set_author(name="Success!")
        linkSuccess.add_field(name=":white_check_mark: Successfuly Linked Account", value="Your roles should update now")
        # TODO: #1 Add an system to automaticly add roles
        if get(ctx.guild.roles, name="Verified"):
            pass
        else:
            pass
        verified_role = get(user.guild.roles, name='Verified')
        await Member.add_roles(user, verified_role)
        with open("links.json") as f:
            temp = json.load(f)

        # TODO: use UUID instead
        playerlinkdata = {username:discord_tag}
        temp.update(playerlinkdata)

        with open("links.json", "w") as f:
            json.dump(temp, f, indent=4)

        await ctx.send(f"{message.author.mention}")
        await ctx.send(embed=linkSuccess)

    else:
        linkFail = discord.Embed(color=0xFF0000)
        linkFail.set_author(name="Please check your ingame social media")
        linkFail.add_field(name=":x: Link your discord account along with your tag in hypixel to verify", value="My profile -> Social media -> Discord -> Example:YOURUSERNAME#0000")
        await ctx.send(f"{message.author.mention}")
        await ctx.send(embed=linkFail)

client.run(TOKEN)
