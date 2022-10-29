import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, TextInput, Modal
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
embed0.set_author(name='📒 Help command 📒', icon_url="https://cdn.discordapp.com/avatars/688672323032580140/3c71102710889f74c72fc69e3477261d.webp?size=2048")
embed0.add_field(name='<:__:1035209966191120444><:__:1035210037892747336> Icons credit', value='<:__:1035211550123888753> [icons](https://discord.gg/icons-859387663093727263)')
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
    channel = candy.get_channel(con['stage'])
    if channel != None:
      candy.loop.create_task(audio_start(channel))

async def trickortreat(user):
  try:
    if db.getByQuery({'guild': user.guild.id})[0]['setup'] != False:
        select = user
        if select.bot == False:
          selected = candy.get_user(select.id)
          by = random.choice(['vampire', 'ghost', 'bat', 'zombie', 'monster', 'dog', 'your friend', 'cat', 'funny clown', 'your neighbors', 'puppies', 'cow', 'horse'])
          embed = discord.Embed(title='**<a:__:1033702719090872391> Trick or Treat**', description='choose with below buttons <a:__:1033760202010415155>', color=0x00005)
          embed.set_thumbnail(url="https://media.discordapp.net/attachments/1029697849350443061/1033775680376295524/BlackYellowEgret-max-1mb.gif")
          embed.set_image(url="https://media.discordapp.net/attachments/1029697849350443061/1033786732669321318/maxresdefault_3.jpg")
          embed.set_footer(text=f'from {by}')
          await selected.send(content='<:__:1033704628988153927> knock knock!!', embed=embed)
  except Exception:
    pass


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
  db.add({'guild': guild.id, 'setup': False, 'stage': None, 'users':{}})

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
        embed = discord.Embed(title='', description='The main motive of this bot is to make your server special and halloween special', color=0xE67E22)
        embed.set_author(name='Starter Guide', icon_url='https://cdn.discordapp.com/emojis/1035444728776380447.png')
        embed.add_field(name='<:__:1035478606266241086> How To Setup', value='use !hsetup or /setup to setup, for more info check !hhelp or /help')
        embed.add_field(name='<:__:1035478606266241086> How to play', value="The creatures will knock on your dm door's but its required to own a house creatures will not knock on your door until they don't get any house with your name")
        embed.add_field(name='<:__:1035478606266241086> Earn Coins', value="You have to keep the chat active and chating with your friend for each 2 messages you will get 1 coin to buy a house you don't need any amount of coins you will get a starter house for free to buy for more info check /shop")
        await ctx.send(embed=embed)
      except Exception:
        pass 
    else:
      await ctx.reply('<a:__:1033760202010415155> server is already setuped and it is not possible to disable because all the creatures have come and they will go <t:1667154600:R>')
  except Exception:
    db.add({'guild': ctx.guild.id, 'setup': True, 'stage': None, 'users':{}})
  

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
    db.add({'guild': ctx.guild.id, 'setup': False, 'stage': None, 'users': {}})

@candy.command()
async def ping(ctx):
    await ctx.send(round(candy.latency * 1000))

@candy.command()
async def help(ctx):
    await Paginator.Simple(PreviousButton=Button(emoji='<:__:1035096189957320744>'), NextButton=Button(emoji='<:__:1035095602003980340>'), PageCounterStyle=discord.ButtonStyle.blurple, InitialPage=0).start(ctx, pages=embeds)

no = 15
messages = []
@candy.event
async def on_message(message):
  messages.append(message.author)
  if len(messages) >= no:
    author = random.choice(messages)
    await trickortreat(author)
    messages.clear()
  await candy.process_commands(message)

class hitBtn(Button):
  async def callback(self, interaction: discord.Interaction):
    self.view.opponent_health -= random.randint(5, 15)
    self.view.hitbox[0] += 1
    if self.view.hitbox[0] == 5:
      self.view.hitbox[1] += 1
    hit = self.view.hitbox
    if 2 < hit[0] < 5:
      hit[1] = "🟧"
    elif 2 > hit[0] < 5:
      hit[1] = "🟩"
    elif 2 < hit[0] > 5:
      hit[1] = "🟥"
    embed1 = discord.Embed(title='')
    embed1.add_field(name="Congratulations",value=f"👑 {interaction.user.name} You won {self.view.opponent_candies} treats from 🎃 {self.view.ghost}")
    embed2 = discord.Embed(title='')
    embed2.add_field(name="Better luck next time!",value=f"Sorry {interaction.user.name} {self.view.ghost} 🎃 has won the match 20% treats from your treat bag will gived to {self.view.ghost}")
    embed3 = discord.Embed(title='')
    embed3.add_field(name="Players",value=f"{interaction.user.name} - ❤️ {self.view.health}% | In bag {self.view.candies}\n{self.view.ghost} - ❤️ {self.view.opponent_health}% | In bag {self.view.opponent_candies}")
    embed3.add_field(name="Tiers",value=f"{self.view.tiers[5]} {self.view.tiers[4]} {self.view.tiers[3]} {self.view.tiers[2]} {self.view.tiers[1]} {self.view.tiers[0]}")
    fview = fightView(self.view.message,self.view.ghost,self.view.opponent_candies,self.view.candies)
    hitbttn = hitBtn(label="Hit!", style=discord.ButtonStyle.red)
    fview.add_item(hitbttn)
    still = 1
    while still > 0:
      if self.view.opponent_health < 0:
        await self.message.edit(embed=embed1)
        still = 0
      elif self.view.health < 0:
        await self.message.edit(embed=embed2)
        still = 0
      elif self.view.health > 0:
        await self.message.edit(embed=embed3, view=view)
    
class fightView(View):
  def __init__(self, message, ghost, opponent_candies, candies):
    self.opponent_health = 100
    self.health = 100
    self.tiers = ["🟩","🟩","🟩","🟩","🟩","🟩"]
    self.hitbox = [0,0]
    self.message = message
    self.ghost = ghost
    self.opponent_candies = opponent_candies
    self.candies = candies
    super().__init__()

@candy.command()
async def fight(ctx):
  candies = db.getByQuery({'guild': ctx.guild.id})[0]['users'][0][f"{ctx.author.id}"]['treats']
  health = 100
  opponent_health = 100
  opponent_candies = random.randint(10, 50)
  ghost = random.choice(['spirit', 'ghost', 'zombie', 'headless man', 'angry jack o lantern', 'monster', 'vampire', 'angry bat', 'skeleton'])
  embed = discord.Embed(title='', description=f'Fight starting in')
  embed.set_author(name=candy.user.name, icon_url='https://cdn.discordapp.com/avatars/1033705675370537010/9ae462928f0b7fbdcf0e4f1287e35267.webp?size=2048')
  counter = 3
  timerbtn = Button(label=counter, style=discord.ButtonStyle.grey, disabled=True)
  view = View()
  view.add_item(timerbtn)
  msg = await ctx.send(embed=embed, view=view)
  for i in range(3):
    counter = counter - 1
    view.remove_item(timerbtn)
    timerbtn = Button(label=str(counter), style=discord.ButtonStyle.grey, disabled=True)
    view.add_item(timerbtn)
    embed2 = embed
    await msg.edit(embed=embed2, view=view)
    await asyncio.sleep(1)
  embed2 = discord.Embed(title='')
  embed2.add_field(name="Players",value=f"{ctx.author.name} - ❤️ {health}% | In bag {candies}\n{ghost} - ❤️ {opponent_health}% | In bag {opponent_candies}")
  embed2.add_field(name="Tiers",value="🟩🟩🟩🟩🟩🟩")
  hitbttn = hitBtn(label="Hit!", style=discord.ButtonStyle.red)
  btns = [hitbttn]
  random.shuffle(btns)
  fview = fightView(msg,ghost,opponent_candies,candies)
  for btn in btns:
    fview.add_item(btn)
  await msg.edit(embed=embed2, view=fview)

class ReferralInput(Modal, title="Reffering system"):
  def init(self):
    self.message = None

  referer_id = TextInput(label="Refferal", style=discord.TextStyle.short, default="Discord User Id")
  
  async def on_submit(self, interaction: discord.Interaction):
    view = View()
    refferUser = await candy.fetch_user(int(self.referer_id.value))
    yesBtn = Button(label="Yes!", style=discord.ButtonStyle.green)
    editBtn = Button(label="edit", style=discord.ButtonStyle.red)
    view.add_item(yesBtn)
    view.add_item(editBtn)
    await interaction.response.send_message(content=f"Are you sure to refer with {refferUser.name}?", view=view, ephemeral=True)
    async def yesBtn_callback(interaction: discord.Interaction):
      view.remove_item(yesBtn)
      view.remove_item(editBtn)
      referrerBtn = Button(label=f"You are Reffering with {refferUser.name}", style=discord.ButtonStyle.blurple, disabled=True, emoji=candy.get_emoji(1035846332709085235))
      confirmBtn = Button(label="Confirm", style=discord.ButtonStyle.green)
      view.add_item(referrerBtn)
      view.add_item(confirmBtn)
      embed2=discord.Embed(title="", description="use below button to referred and fill refferer DiscordID then click on confirm button", color=0xE67E22)
      embed2.set_author(name=f"{candy.user.name} registration", icon_url=interaction.user.display_avatar)
      await self.message.edit(embed=embed2, view=view)
    async def editBtn_callback(interaction: discord.Interaction):
      await interaction.response.send_modal(ReferralInput())
    yesBtn.callback = yesBtn_callback
    editBtn.callback = editBtn_callback

@candy.command()
async def register(ctx):
  try:
    db.getByQuery({"guild":ctx.guild.id})[0]["users"][0][f"{ctx.author.id}"]
    await ctx.send("You are already registered")
  except Exception:
    referrerBtn = Button(label="Refer", style=discord.ButtonStyle.blurple, emoji=candy.get_emoji(1035846332709085235))
    view = View()
    embed=discord.Embed(title="", description="use below button to refer and fill referer DiscordID then click on confirm button", color=0xE67E22)
    embed.set_author(name=f"{candy.user.name} registration", icon_url=ctx.author.avatar)
    view.add_item(referrerBtn)
    msg = await ctx.send(content="Note - _your referer user must have already registered else you can't refer with that user_", embed=embed, view=view)
    async def referrerBtn_callback(interaction):
      modal = ReferralInput()
      modal.message = msg
      await interaction.response.send_modal(modal)
    referrerBtn.callback = referrerBtn_callback

async def main():
    async with candy:
        await candy.load_extension('jishaku')
        await candy.start('MTAzMzcwNTY3NTM3MDUzNzAxMA.Gpwh5K.9adc7WN_Xlwj0fNrTFC560TDiAbkZCSLcu8O9Q')
        
if __name__ == '__main__':
  asyncio.run(main())
