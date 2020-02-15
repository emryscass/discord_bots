import discord
from discord.ext import commands
import random
import requests
import json
import urllib.parse, urllib.request, re
from googletrans import Translator

client = commands.Bot(command_prefix='emry ')

# show connection has been made
@client.event
async def on_ready():
    print('I\'ve made a connection and ready for some action!')

# Greet member on joining server
@client.event
async def on_member_join(member):
    print(f'A new member has joined -> {member}')
    await member.send(f'Welcome to our learning server {member}! Type "bot info" for more information.')



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


# Clear the screen
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)



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

# search youtube
@client.command()
async def youtube(ctx, *, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })

    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string
    )

    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])


# Translate any language to English
@client.command()
async def translate(ctx, *, phrase):
    translator = Translator()
    translated = translator.translate(phrase)
    await ctx.send(f'{translated.text}')

client.run('DISCORD_TOKEN')
