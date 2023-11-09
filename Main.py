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

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    # Check if the user invoking the command has the "ban" permission
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned.')
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command()
async def unban(ctx, *, member):
    # Check if the user invoking the command has the "ban" permission
    if ctx.author.guild_permissions.ban_members:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

        await ctx.send('User not found in the ban list.')
    else:
        await ctx.send("You do not have permission to use this command.")

# Define a "mute" command
@bot.command()
async def mute(ctx, member: discord.Member):
    # Check if the user invoking the command has the "manage_roles" permission
    if ctx.author.guild_permissions.manage_roles:
        # Check if a "Muted" role exists, and create it if not
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role is None:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

        # Add the "Muted" role to the member
        await member.add_roles(muted_role)
        await ctx.send(f'{member.mention} has been muted.')

    else:
        await ctx.send("You do not have permission to use this command.")

# Define an "unmute" command
@bot.command()
async def unmute(ctx, member: discord.Member):
    # Check if the user invoking the command has the "manage_roles" permission
    if ctx.author.guild_permissions.manage_roles:
        # Find the "Muted" role
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role is not None and muted_role in member.roles:
            # Remove the "Muted" role from the member
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} has been unmuted.')
        else:
            await ctx.send(f'{member.mention} is not muted.')

    else:
        await ctx.send("You do not have permission to use this command.")


# Run the bot with your token
bot.run("YOUR_BOT_TOKEN")
# replace YOUR_BOT_TOKEN with you bot s'token
