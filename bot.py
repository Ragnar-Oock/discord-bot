import os
import logging
import random
import urllib.request
import urllib.parse
import re

import discord 
from discord.ext import commands

description = (
        f"Hi, I'm Kevin. I teach people how to make the web and how to make "
        f"it look good while they're at it."
        )

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('TOKEN')

client = commands.Bot(command_prefix = ".", description=description)

youtube_url = "https://www.youtube.com/watch?v="
youtube_search = "https://www.youtube.com/kepowob/search?"


# Events is a piece of code happens when the bot detects a 
# specific activity has happened
@client.event
async def on_ready():
    ####
    ## MODIFY FOR IT TO CHANGE PERIODICALLY
    ## Instead of on load
    ####
    GAMES = ['Minecraft', 'Anything but Fortnite', 'Lucid Dream']
    is_playing = random.choice(GAMES)
    await client.change_presence(status=discord.Status.idle,
            activity=discord.Game(is_playing))
    print('Bot is ready')


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')


@client.event
async def on_command_error(ctx, error):
    """ The event will be triggered for all functions
        if using commands.MissingRequiredArgument
    """
    if isinstance(error, commands.CommandNotFound):
        print(f'Invalid command used. To get a lists of commands type `.help`')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    """ Deletes the last message
    """
    await ctx.channel.purge(limit=amount)


@client.listen('on_message')
async def on_message(message):
    ext = '.html'
    reply = (
            f'"It\'s quite possible this asteroid is not entirely stable". '
            f'Upload your file to codepen {message.author.mention}, '
            f'and someone may come around to take a look.'
        )

    if message.author == client.user:
        return

    if message.attachments[0].url.endswith('html'):
        print(message.attachments[0].url.endswith('html'))
        return await message.channel.send(reply)


@client.command(aliases=['dontask', 'dontasktoask', 'dont-ask-to-ask', 'justask'])
async def dont_ask_to_ask(ctx):
    """ Don't ask to ask, just ask.
    Send a message enquiring users in a channel to ask a question directly
    """

    message = f"Be a good netizen and don't ask to ask. " \
              f"It wastes the other person's time by having to ask " \
              f"you what is the question and waiting for a reply. " \
              f"Rather ask: How do I do [problem] with Java and [other relevant info]? " \

    embed = discord.Embed(title="Don't ask to ask, just ask",
                          url="https://dontasktoask.com")
    embed.set_thumbnail(url="https://dontasktoask.com/favicon.png")
    await ctx.send(content=message, embed=embed)


@client.command(aliases=['yt', 'YouTube'])
async def youtube(ctx, title, amount=1):
    """ Searches for kevins videos on a given topic.
    """
    if amount >= 4:
        amount = 3
    params = urllib.parse.urlencode({'query': title})
    search = f'{youtube_search}{params}'
    html = urllib.request.urlopen(search)
    content = html.read().decode()
    video_ids = re.findall(r"watch\?v=(\S{11})", content)
    for video in video_ids[:amount]:
        await ctx.send(f'{youtube_url}{video}')


@client.command()
async def ping(ctx):
    """ You think Javascript is fast? pffttt...
    """
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


@client.command(aliases=['box_sizing'])
async def box_model(ctx):
    """ There is only one, sane, choice.
    """
    await ctx.send(file=discord.File('assets/borderbox.png'))


@client.command(aliases=['can'])
async def cssanatomy(ctx):
    """ Explains the different parts of a css rule
    """
    await ctx.send(file=discord.File('assets/anatomy.png'))


@client.command(aliases=['crl'])
async def conquering_layouts(ctx):
    """ Your path to finally conuering responsive layouts
       
    """
    embed = discord.Embed(title=f"Conquering Responsive Layouts", 
            description="Start creating responsive layouts with confidence!",
            url="https://courses.kevinpowell.co/conquering-responsive-layouts")
    embed.set_thumbnail(url="https://cssdemystified.com/assets/kevinpowell@0,25x.jpg")
    await ctx.send(embed=embed)


@client.command(aliases=['dem'])
async def cssdemystified(ctx):
    """ A course by Kevin that helps you unravel CSS. Not me,
        the other Kevin.
    """
    embed = discord.Embed(title=f"CSS demystified",
            description="Start writing css with confidence",
            url="https://cssdemystified.com/")
    embed.set_thumbnail(url="https://cssdemystified.com/assets/kevinpowell@0,25x.jpg")
    await ctx.send(embed=embed)


#@commands.check(is_it_user) # will run if the custom check returns true
@client.command(aliases=['toss'])
async def coinflip(ctx, *, question):
    """ Whenever you are stuck, toss a coin. Heads and tails have
        been replaced for yes and no respectively.
    """
    responses = ['yes', 'no']
    if not 'sure' in question.lower():
        return await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}\n{ctx.author.mention}')
    return await ctx.send(f'The captain says you are a friend. I will not kill you. {ctx.author.mention}')


# Specifying errors directly to each command
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Please specify an amount of messages to delete')


if __name__ == "__main__":
    try:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.load_extension(f'cogs.{filename[:-3]}')
    except Exception as ex:
        print(f'{ex}')
    client.run(TOKEN)
