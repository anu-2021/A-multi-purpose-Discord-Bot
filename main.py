import discord 
from discord.ext import commands
import os
import json
import random
import asyncio
import requests
import datetime
import time



client = commands.Bot(command_prefix = ".", intents = discord.Intents.all(), activity = discord.Activity(type=discord.ActivityType.listening, name= " .help"))

@client.command()
async def joke(ctx):
  response = requests.get("https://icanhazdadjoke.com", headers = {"Accept": "text/plain"})
  embed = discord.Embed(title = "Joke", description = response.text, color = discord.Colour.blue())
  await ctx.send(embed = embed)


@client.command()
async def invite(ctx):
  embed = discord.Embed(title = "Thanks for considering!", description = f"[Click Here](link) to invite me to your server! \n Currently, I'm in {len(client.guilds)} servers!", color = discord.Color.green())
  embed.set_footer(text = "Invite me", icon_url = client.user.avatar_url)
  await ctx.send(embed = embed)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
  client.load_extension(f"cogs.{extension}")
  await ctx.send(f"Loaded ``{extension}`` successfully")

@client.command()
async def server(ctx):
  all_roles = ""
  for role in ctx.guild.roles:
    all_roles += f"{role.mention} "

  guild = ctx.guild
  embed = discord.Embed(title = ctx.guild.name, decription = f"Information on {ctx.guild}", color = client.ecolor)
  embed.add_field(name = "Members", value = guild.member_count, inline = False)
  embed.add_field(name = "Channels", value = f"All channels: {len(guild.channels)} \n Text Chanels: {len(guild.text_channels)} \n Voice Channels: {len(guild.voice_channels)}", inline = False)
  embed.add_field(name = "ID", value = guild.id, inline = False)
  embed.add_field(name = "Owner", value = guild.owner, inline = False)
  embed.add_field(name = f"Roles ({len(guild.roles)})", value = all_roles, inline = False)
  embed.set_thumbnail(url = ctx.guild.icon_url)
  await ctx.send(embed = embed)

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
  client.unload_extension(f"cogs.{extension}")
  await ctx.send(f"Unloaded ``{extension}`` successfully")

@client.command()
@commands.is_owner()
async def loadall(ctx):
  for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
      client.load_extension(f"cogs.{filename[:-3]}")
      await ctx.send(f"Loaded ``{filename[:-3]}`` successfully")

@client.event
async def on_ready():
  for filename in os.listdir("./cogs"):
    if filename.endswith('.py') and not filename.startswith('Automod'):
      client.load_extension(f"cogs.{filename[:-3]}")
      print(f"Loaded ``{filename[:-3]}`` successfully")
  client.load_extension('jishaku')
  print("Ready")
  

@client.command()
async def ping(ctx):
  start = time.perf_counter()
  a = await ctx.send("Pinging...")
  end = time.perf_counter()
  dur = (end-start) * 1000
  embed = discord.Embed(title = "Pong!", description = f"**Response Time** \n ```{dur:.2f}ms``` \n **Websocket Latency** \n ```{round(((client.latency) * 1000), 2)}ms```", color = 0xb3b3ff)
  await a.edit(embed = embed)
  

@client.command(aliases = ["bug"])
async def suggest(ctx, *, suggestion):
  you = client.get_user(your_id)

  await you.send(f"New Suggestion by {ctx.author} \n {suggestion}")
  await ctx.send("Thank you for your suggestion / bug report! It helps a lot!")


snipe_message_content = None
snipe_message_author = None
snipe_message_id = None
snipe_message = None

@client.event
async def on_message_delete(message):
  global snipe_message_content
  global snipe_message_author
  global snipe_message_id
  global snipe_message

  snipe_message_content = message.content
  snipe_message_author = message.author
  snipe_message_id = message.id
  snipe_message = message
  await asyncio.sleep(60)

  if message.id == snipe_message_id:
      snipe_message_author = None
      snipe_message_content = None
      snipe_message_id = None
      snipe_message = None

@client.command()
async def snipe(ctx):
    if snipe_message_content==None:
        await ctx.send("There's nothing to snipe!")
    else:
        embed = discord.Embed(title = f"{snipe_message_author.name}#{snipe_message_author.discriminator}", description = f"{snipe_message_content}", color = 0xb3b3ff)
        created_time = snipe_message.created_at
        str_time = created_time.strftime('%m/%d/%Y, %H:%M:%S')
        embed.set_footer(text =f"Deleted at {str_time}")
        await ctx.send(embed=embed)
        return

client.run(os.getenv("TOKEN"))