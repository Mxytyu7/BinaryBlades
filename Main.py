import discord
import random
import requests
from discord.ext import commands

# pip install discord.py
# pip install random


# Create an instance of the bot
bot = commands.Bot(command_prefix='!')

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')



# Define some additional responses for new commands
cat_facts = ["Cats have five toes on their front paws but only four on their back paws.", "A group of cats is called a clowder."]
weather_responses = ["Looks like the perfect day to stay indoors and code!", "Cloudy with a chance of virtual rainbows."]
haiku_topics = ["Nature", "Technology", "Pizza"]

# Define new bot commands
def cat_fact_command():
    return random.choice(cat_facts)

def weather_command(location):
    # Replace this with an actual weather API call based on the location
    # For simplicity, I'm just providing a random response
    return random.choice(weather_responses)

def haiku_command(topic):
    if topic not in haiku_topics:
        return "Sorry, I can only generate haikus on specific topics."
    # Replace this with a haiku generation logic based on the topic
    # For simplicity, I'm just providing a placeholder response
    return f"An example haiku about {topic}: \nCherry blossoms fall,\nSilent whispers in the breeze,\nNature's quiet dance."

def emoji_command(emotion):
    # Replace this with a more sophisticated emoji translation logic
    # For simplicity, I'm just providing a basic mapping
    emoji_mapping = {"happy": "😄", "sad": "😢", "confused": "😕"}
    return emoji_mapping.get(emotion, "I don't understand that emotion.")

def riddle_command():
    riddles = ["The more you take, the more you leave behind. What am I?", "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?"]
    return random.choice(riddles)

# Example usage of new commands
print(cat_fact_command())
print(weather_command("New York"))
print(haiku_command("Nature"))
print(emoji_command("happy"))
print(riddle_command())



# Define some responses for each command
compliments = ["You're awesome!", "You're a star!", "Keep shining!"]
jokes = ["Why don't scientists trust atoms? Because they make up everything!", "What do you call fake spaghetti? An impasta!"]
quotes = ["The only way to do great work is to love what you do. - Steve Jobs", "Don't cry because it's over, smile because it happened. - Dr. Seuss"]

# Define the bot commands
def compliment_command():
    return random.choice(compliments)

def joke_command():
    return random.choice(jokes)

def quote_command():
    return random.choice(quotes)

# Example usage
print(compliment_command())
print(joke_command())
print(quote_command())


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def goodbye(ctx):
    await ctx.send('Goodbye!')

@bot.command()
async def avatar(ctx):
    await ctx.send(ctx.author.avatar_url)

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title='Bot Info',
        description=f'Name: {bot.user}\nVersion: 1.0\nCreated by: You',
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked for {reason}.')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned for {reason}.')

@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user} has been unbanned.')
            return

@bot.command()
async def add(ctx, num1: int, num2: int):
    await ctx.send(num1 + num2)

@bot.command()
async def subtract(ctx, num1: int, num2: int):
    await ctx.send(num1 - num2)

@bot.command()
async def multiply(ctx, num1: int, num2: int):
    await ctx.send(num1 * num2)

@bot.command()
async def divide(ctx, num1: int, num2: int):
    await ctx.send(num1 / num2)

@bot.command()
async def greet(ctx):
    await ctx.send('Greetings!')

@bot.command()
async def inspire(ctx):
    quotes = ['Quote 1', 'Quote 2', 'Quote 3']
    await ctx.send(random.choice(quotes))

@bot.command()
async def advice(ctx):
    advices = ['Advice 1', 'Advice 2', 'Advice 3']
    await ctx.send(random.choice(advices))

@bot.command()
async def role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'{member} has been given the {role} role.')

@bot.command()
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'{member} has had the {role} role removed.')

@bot.command()
async def server_info(ctx):
    server = ctx.guild
    roles = [role.name for role in server.roles]
    members = server.member_count
    bots = len([member for member in server.members if member.bot])
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    online = len([member for member in server.members if member.status == discord.Status.online])
    offline = len([member for member in server.members if member.status == discord.Status.offline])
    dnd = len([member for member in server.members if member.status == discord.Status.dnd])
    idle = len([member for member in server.members if member.status == discord.Status.idle])

    embed = discord.Embed(
        title=f'Server Info: {server.name}',
        description=f'Total Roles: {len(roles)}\nTotal Members: {members}\nTotal Bots: {bots}\nText Channels: {text_channels}\nVoice Channels: {voice_channels}\nMembers Online: {online}\nMembers Offline: {offline}\nMembers DND: {dnd}\nMembers Idle: {idle}',
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title='Warning',
        description=f'{member} has been warned for {reason}.',
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def weather(ctx, city: str):
    weather = await get_weather(city)
    embed = discord.Embed(
        title=f'Weather for {city}',
        description=f'{weather}',
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command()
async def server(ctx):
    embed = discord.Embed(
        title='Support Server',
        description='[Click here to join our support server!](your-invite-link-here)',
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def rules(ctx):
    rules = [f'Rule {i}: {rule}' for i, rule in enumerate(bot.rules, start=1)]
    embed = discord.Embed(
        title='Rules',
        description='\n'.join(rules),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command()
async def announce(ctx, *, message: str):
    embed = discord.Embed(
        title='Announcement',
        description=message,
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(
        title=f'User Info: {member}',
        description=f'Name: {member}\nID: {member.id}\nStatus: {member.status}\nHighest Role: {member.top_role}\nCreated at: {member.created_at}\nJoined at: {member.joined_at}',
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command()
async def vote(ctx):
    embed = discord.Embed(
        title='Vote',
        description='[Click here to vote for our bot!](your-vote-link-here)',
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(
        title='Kick',
        description=f'{member} has been kicked for {reason}.',
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(
        title='Ban',
        description=f'{member} has been banned for {reason}.',
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def unban(ctx, *, member: str):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(
                title='Unban',
                description=f'{user} has been unbanned.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    embed = discord.Embed(
        title='Mute',
        description=f'{member} has been muted for {reason}.',
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def unmute(ctx, member: discord.Member, *, reason=None):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole, reason=reason)
    embed = discord.Embed(
        title='Unmute',
        description=f'{member} has been unmuted.',
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

bot.run('your-token-here')
# replace YOUR_BOT_TOKEN with you bot s'token
