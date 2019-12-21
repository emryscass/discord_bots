import discord
from discord.ext import commands
import random
import requests
import json

client = commands.Bot(command_prefix='$')

# show connection has been made
@client.event
async def on_ready():
    print('I\'ve made a connection and ready for some action!')

# member has joined server
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')

# member has left server
@client.event
async def on_member_remove(member):
    print(f'{member} has left the server  :(')

# Check ping of bot
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# Magic 8ball
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes - definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
        'Reply hazy, try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don\'t count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

# Kick a member
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)


# Ban a member
@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

# Unban a member
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# prints a random chuck norris joke
@client.command()
async def norris(ctx):
    url = 'http://api.icndb.com/jokes/'
    data = requests.get(url).json()
    joke = data['value'][random.randint(0, len(data['value']))]['joke']
    if '&quot;' in joke:
        await ctx.send(joke.replace('&quot;', ' '))
    else:
        await ctx.send(joke)


client.run('DISCORD_TOKEN')
