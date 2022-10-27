import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
import random
import asyncio
from pysondb import db
import wavelink
import jishaku
import Paginator

candy = commands.Bot(command_prefix="!h", intents=discord.Intents().all(), strip_after_prefix=True)
candy.remove_command('help')
db = db.getDb("guilddb.json")
embed0 = discord.Embed(title='')
embed0.add_field(name='<prefix>setup', value='setup the bot for you automatically')
embed0.add_field(name='<prefix>start', value="start a stage and automatically start playing relaxing halloween audio's")
embed0.add_field(name='<prefix>ping', value="show latency of bot")
embed0.set_author(name='**📒 Help command 📒**', icon_url="https://cdn.discordapp.com/avatars/688672323032580140/3c71102710889f74c72fc69e3477261d.webp?size=2048")
embed1 = discord.Embed(title='', description='```\n- <prefix> = !h or / \n```')
embed1.set_author(name="Setup", icon_url='https://cdn.discordapp.com/avatars/1033705675370537010/9ae462928f0b7fbdcf0e4f1287e35267.webp?size=2048')
embed1.add_field(name='Info', value='setup the bot for you automatically')
embed1.add_field(name='Aliases', value="No Aliases")
embed1.add_field(name="Usage", value="<prefix>setup")
embed2 = discord.Embed(title='', description='```\n- <prefix> = !h or / \n```')
embed2.set_author(name="Start", icon_url='https://cdn.discordapp.com/avatars/1033705675370537010/9ae462928f0b7fbdcf0e4f1287e35267.webp?size=2048')
embed2.add_field(name='Info', value="start a stage and automatically start playing relaxing halloween audio's")
embed2.add_field(name="Aliases", value="No Aliases")
embed2.add_field(name="Usage", value="<prefix>start")
embeds = [embed0, embed1, embed2]

@candy.event
async def on_ready():
  candy.loop.create_task(connect_nodes())
  print('spookotuber ready')
  json = db.getAll()
  for con in json:
    guild = con['guild']
    setup = con['setup']
    if setup == True:
      trickortreat.start(guild)
  for con2 in json:
    channel = candy.get_channel(con['stage'])
    if channel != None:
      candy.loop.create_task(audio_start(channel))

@tasks.loop(seconds=300)
async def trickortreat(guild):
  guild = candy.get_guild(guild)
  users = []
  async for member in guild.fetch_members(limit=None):
    users.append(member)
  selc = 0
  while selc < 1:
    select = random.choice(users)
    if select.bot == True:
      users.clear()
      selected = candy.get_user(select.id)
      by = random.choice(['vampire', 'ghost', 'bat', 'zombie', 'monster', 'dog', 'your friend', 'cat', 'funny clown', 'your neighbors', 'puppies', 'cow', 'horse'])
      embed = discord.Embed(title='**<a:__:1033702719090872391> Trick or Treat**', description='choose with below buttons <a:__:1033760202010415155>', color=0x00005)
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/1029697849350443061/1033775680376295524/BlackYellowEgret-max-1mb.gif")
      embed.set_image(url="https://media.discordapp.net/attachments/1029697849350443061/1033786732669321318/maxresdefault_3.jpg")
      embed.set_footer(text=f'from {by}')
      await selected.send(content='<:__:1033704628988153927> knock knock!!', embed=embed)
      selc = 1


async def connect_nodes():
  await candy.wait_until_ready()
  await wavelink.NodePool.create_node(bot=candy, host='lavalink.botsuniversity.ml', port=443, password='mathiscool', https=True)

async def audio_start(channel):
  audio = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, 'https://youtu.be/82klOP4jTRg')
  member = channel.guild.get_member(candy.user.id)
  try:
    stage = await channel.create_instance(topic='happy halloween 🎃', reason=None)
    vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
    await member.edit(suppress = False)
    plar = await vc.play(audio[0])
    await vc.seek(540000)
  except Exception:
    vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
    await member.edit(suppress = False)
    plar = await vc.play(audio[0])
    await vc.seek(540000)

@candy.event
async def on_guild_join(guild):
  db.add({'guild': guild.id, 'setup': False, 'stage': None})

@candy.event
async def on_guild_remove(guild):
  id = db.getByQuery({'guild': guild.id})[0]['id']
  db.deleteById(id)

@candy.command()
async def setup(ctx):
  try:
    check = db.getByQuery({'guild': ctx.guild.id})[0]['setup']
    if check != True:
      try:
        id = db.getByQuery({'guild': ctx.guild.id})[0]['id']
        db.updateById(id, {'setup': True})
        await ctx.reply('hello spooky wooky i sent your server invite to all cute and spooky creatures they will coming in a while 🎃')
        trickortreat.start(ctx.guild.id)
      except Exception:
        pass 
    else:
      await ctx.reply('<a:__:1033760202010415155> server is already setuped and it is not possible to disable because all the creatures have come and they will go <t:1667154600:R>')
  except Exception:
    db.add({'guild': ctx.guild.id, 'setup': True, 'stage': None})
  

@candy.command()
async def start(ctx):
  try:
    if db.getByQuery({'guild':ctx.guild.id})[0]['setup'] != False:
      channel = await ctx.guild.create_stage_channel(name='halloween lofi', topic='all the creatures are tired and they want to listen relaxing music')
      db.updateByQuery({'guild': ctx.guild.id}, {'stage': channel.id})
      candy.loop.create_task(audio_start(channel))
      await ctx.send(await channel.create_invite())
      embed = discord.Embed(title='🎃 Note from Fuser(Owner)', description='\nHello Dear discord\nIf you are thinking to take against this bot because of music system so please read this first the bot is not taking audios from youtube its predownloaded audios in my folder and bot playing the audios from it\n~ Happy halloween Discord', color=0xE67E22)
      embed.set_footer(text='if you are an normal user then you dont need to read this')
      await ctx.send(embed=embed)
    else:
      await ctx.send("you can't start a stage until you don't setup the bot using `!hsetup` command")
  except Exception:
    db.add({'guild': ctx.guild.id, 'setup': False, 'stage': None})

@candy.command()
async def ping(ctx):
    await ctx.send(round(candy.latency * 1000))

@candy.command()
async def help(ctx):
    await Paginator.Simple().start(ctx, pages=embeds)

async def main():
    async with candy:
        await candy.load_extension('jishaku')
        await candy.start('MTAzMzcwNTY3NTM3MDUzNzAxMA.Gpwh5K.9adc7WN_Xlwj0fNrTFC560TDiAbkZCSLcu8O9Q')
        
if __name__ == '__main__':
  asyncio.run(main())
