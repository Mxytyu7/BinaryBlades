import discord
import random
from discord.ext import commands

# pip install discord.py
# pip install random


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

# Define a "rank" command
@bot.command()
async def rank(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    roles = member.roles[1:]  # Exclude the @everyone role

    if roles:
        role_names = ", ".join([role.name for role in roles])
    else:
        role_names = "No roles"

    await ctx.send(f'{member.mention}\'s roles: {role_names}')

# Define a "roles" command
@bot.command()
async def roles(ctx):
    # Create an embed to display the roles
    embed = discord.Embed(
        title='Server Roles',
        description='\n'.join([role.mention for role in ctx.guild.roles]),
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed)

# Define an "unrank" command
@bot.command()
async def unrank(ctx, member: discord.Member, *, role_name):
    # Check if the user invoking the command has the "manage_roles" permission
    if ctx.author.guild_permissions.manage_roles:
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role is not None and role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f'{member.mention} has been unranked from {role_name}.')
        else:
            await ctx.send(f'{member.mention} does not have the role {role_name}.')

    else:
        await ctx.send("You do not have permission to use this command.")

# Define a "create_role" command
@bot.command()
async def create_role(ctx, role_name, color: discord.Color = None):
    # Check if the user invoking the command has the "manage_roles" permission
    if ctx.author.guild_permissions.manage_roles:
        guild = ctx.guild

        if discord.utils.get(guild.roles, name=role_name) is None:
            # Create the role with the specified name and color
            new_role = await guild.create_role(name=role_name, color=color)

            await ctx.send(f'Role "{new_role.name}" created.')
        else:
            await ctx.send('A role with that name already exists.')
    else:
        await ctx.send("You do not have permission to use this command.")

# Define a "clear" command
@bot.command()
async def clear(ctx, amount: int):
    # Check if the user invoking the command has the "manage_messages" permission
    if ctx.author.guild_permissions.manage_messages:
        if 1 <= amount <= 100:  # Limit the number of messages to delete
            await ctx.channel.purge(limit=amount + 1)  # +1 to account for the command message
            await ctx.send(f'{amount} messages have been cleared.', delete_after=5)
        else:
            await ctx.send('Please specify a number of messages to delete between 1 and 100.')
    else:
        await ctx.send("You do not have permission to use this command.")

# Define a "how_sus" command
@bot.command()
async def how_sus(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    sus_level = random.randint(0, 100)
    sus_message = f"{member.mention} is {sus_level}% sus."

    await ctx.send(sus_message)

# Define a "coinflip" command
@bot.command()
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on **{result}**!")

# Define a "ban_list" command
@bot.command()
async def ban_list(ctx):
    # Check if the user invoking the command has the "ban_members" permission
    if ctx.author.guild_permissions.ban_members:
        bans = await ctx.guild.bans()
        if bans:
            banned_users = [f"{entry.user.name}#{entry.user.discriminator}" for entry in bans]
            ban_list = "\n".join(banned_users)
            await ctx.send(f"List of banned users:\n{ban_list}")
        else:
            await ctx.send("There are no banned users in this server.")
    else:
        await ctx.send("You do not have permission to use this command.")


# Run the bot with your token
bot.run("YOUR_BOT_TOKEN")
# replace YOUR_BOT_TOKEN with you bot s'token
