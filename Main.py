import discord
from discord.ext import commands

# pip install discord.py


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

# Define a "ping" command
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert latency to milliseconds
    await ctx.send(f'Pong! Latency is {latency}ms')

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    # Check if the user invoking the command has the "kick" permission
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked.')
    else:
        await ctx.send("You do not have permission to use this command.")



# Run the bot with your token
bot.run("YOUR_BOT_TOKEN")
# replace YOUR_BOT_TOKEN with you bot s'token
