import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os
import json
import random
import praw

load_dotenv()
reddit = praw.Reddit(client_id=os.getenv("R_Client_ID"),client_secret=os.getenv("R_Client_Secret"),username=os.getenv("praw_username"),password=os.getenv("praw_password"),user_agent="prawbot")
intents = discord.Intents(members=True)
bot = discord.Client(intents=intents)

#get prefix
def get_prefix(bot,message):
    with open("prefixes.json","r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix)

#prefix create
@bot.event
async def on_guild_join(guild):
    with open("prefixes.json","r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] ="!"
    with open("prefixes.json","w") as f:
        json.dump(prefixes,f)
#prefix dump
@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json","r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("prefixes.json","w") as f:
        json.dump(prefixes,f)

#on ready
@bot.event
async def on_ready():
    print('Logged in as '+bot.user.name)
    print("Bot Present in "+str(len(bot.guilds))+" Servers")
    await bot.change_presence(activity=discord.Game(name="with your mom"))

#welcome
@bot.event
async def on_member_join(member):
    print("hoegea")
    channel = bot.get_channel(825458023745060877)
    embed=discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!") # F-Strings!
    embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
    await channel.send(embed=embed)


#upvote/downvote
@bot.command()
async def vote(ctx):
    attachment = ctx.message.attachments[0]
    if attachment.size > 0:
        await ctx.message.add_reaction("⬆")
        await ctx.message.add_reaction("⬇")

#roast
@bot.command()
async def roast(ctx,user: discord.Member = None):
    await ctx.send(f"{user} teri ma ki chut laude")

#pfp
@bot.command()
async def pfp(ctx,member: discord.Member = None):
    embed = discord.Embed(title =member,color=discord.Color.dark_blue())
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)

#normie
@bot.command()
async def hownormie(ctx,user: discord.Member = None):
    message = await ctx.send("Checking.... ██ 20%")
    await asyncio.sleep(1)
    await message.edit(content="Checking.... ███ 40%")
    await asyncio.sleep(1)
    await message.edit(content="Checking.... █████ 60%")
    await asyncio.sleep(1)
    await message.edit(content="Checking.... ███████ 80%")
    await asyncio.sleep(1)
    await message.edit(content="Checking.... █████████ 100%")
    await asyncio.sleep(1)
    await message.edit(content=f"{user.mention} is {random.randint(0,100)}% likely to be a normie")

#gay
@bot.command()
async def howgay(ctx,user: discord.Member = None):
    if user.id != 469535449694732289:
        message = await ctx.send("Checking.... ██ 20%")
        await asyncio.sleep(1)
        await message.edit(content="Checking.... ███ 40%")
        await asyncio.sleep(1)
        await message.edit(content="Checking.... █████ 60%")
        await asyncio.sleep(1)
        await message.edit(content="Checking.... ███████ 80%")
        await asyncio.sleep(1)
        await message.edit(content="Checking.... █████████ 100%")
        await asyncio.sleep(1)
        await message.edit(content=f"{user.mention} is {random.randint(70,100)}% likely to be a fucking gay")
    else:
        await ctx.send(f"{user} is a fucking chad")

#reddit
@bot.command()
async def r(ctx,sub):
    subreddit = reddit.subreddit(sub)
    allsubs = []
    top = subreddit.top(limit = 50)

    for submissions in top:
        allsubs.append(submissions)
    
    randomsub = random.choice (allsubs)
    name = randomsub.title
    url = randomsub.url

    em = discord.Embed(title = name)
    em.set_image(url = url)

    await ctx.send(embed = em)
    


#whois
@bot.command()
async def whois(ctx,member: discord.Member = None):
    embed = discord.Embed(title =member,color=discord.Color.dark_blue())
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="UserID",value=member.id,inline=True)
    embed.add_field(name="NickName",value=member.nick,inline=True)
    embed.add_field(name="Joined Discord On",value=member.created_at.strftime("%A, %B %d %Y"), inline=False)
    embed.add_field(name="Joined Server On",value=member.joined_at.strftime("%A, %B %d %Y"), inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

#kick
@bot.command(aliasis = ['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason = "Undefined Reason"):
    await member.send("kicked because of "+reason)
    await ctx.send(f'{member} has been kicked due to {reason}')
    await member.kick(reason = reason)

#ban
@bot.command(aliasis = ['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason = "Undefined Reason"):
    await member.send("banned because of "+reason)
    await ctx.send(f'{member} has been banned due to {reason}')
    await member.ban(reason = reason)

#change prefix
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open("prefixes.json","r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json","w") as f:
        json.dump(prefixes,f)
    await ctx.send(f"Prefix Changed To : {prefix}")
#create invite    
@bot.command()
async def invite(ctx,age = 60):
    link = await ctx.channel.create_invite(max_age = age*60,unique = True)
    embed = discord.Embed(title = "Here is your invite link",description = link,color = discord.Colour.blue())
    embed.add_field(name = "Validity",value = f"{age} minutes",inline=True)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)
#running
load_dotenv()
bot.run(os.getenv("Client_ID"))