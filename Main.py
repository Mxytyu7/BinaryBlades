import discord
from discord.ext import commands

# Create an instance of the bot
bot = commands.Bot(command_prefix='!')

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Define a simple command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello, World!')

# Run the bot with your token
bot.run("YOUR_BOT_TOKEN")
# replace YOUR_BOT_TOKEN with you bot s'token
