import discord
import os
from dotenv import load_dotenv
import CustomFunctions
from discord.ext import commands
from discord import app_commands

load_dotenv()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command('help')
#region Bot Prefix Commands
@bot.command()
async def ping(ctx):
    await ctx.send(f"Online at {ctx.guild}")

@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def global_sync_creation_misc(ctx):
    if(ctx.author.id == CustomFunctions.user_darkie['user_id']):
        fmt = await bot.tree.sync()
        await ctx.send(f"Đã đồng bộ hết {len(fmt)} slash commands của Creation Misc vào toàn bộ server hiện hành!")
    else:
        await ctx.send(f"Có phải là Darkie đâu mà dùng lệnh này?")        
        
@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
@app_commands.checks.has_role(1256989385744846989)
async def sync(ctx):
    if(ctx.author.id == CustomFunctions.user_darkie['user_id']):
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)
        await ctx.send(f"Đồng bộ {len(fmt)} commands vào {ctx.guild}")
    else:
        await ctx.send(f"Có phải là Darkie đâu mà dùng lệnh này?")
        

bot_token = os.getenv("BOT_TOKEN_MISC")


client = discord.Client(intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

bot.run(bot_token)