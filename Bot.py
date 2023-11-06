import discord
from discord.ext import commands, tasks
import sqlite3

cursor = sqlite3.Cursor()
cursor.execute(
    ''
)

bot = commands.Bot('!')


@bot.event
async def on_ready():
    print(f'Logado como {bot.user}')


@bot.command(name='add')
async def add(ctx):
    await ctx.mention(ctx.message.user)


@bot.command(name='show')
async def show(ctx):
    pass


@bot.command(name='delete')
async def delete(ctx):
    pass


bot.run('OTQzNTU1OTAwNjk2ODUwNTMy.Yg0w6Q.d76eyClTa0vAxDIp71hao42mdgE')
