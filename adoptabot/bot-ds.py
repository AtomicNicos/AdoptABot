# bot.py
import os
import asyncio
from pprint import pprint

import discord

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# WAIT VOICE CHANNEL NAME
WAIT_CHANNEL_NAME = "General"

# Client
client = discord.Client()

global guild, voice_channels, wait_channel_name, participants, wait_channel

guild = None
participants = []
voice_channels = []
wait_channel_name = WAIT_CHANNEL_NAME
wait_channel = None


async def prune(message = 0):
    if message.author.name != "Emmanuel":
        await message.channel.send('You are not allowed to use this command!')
        return

    argv = message.content.split(' ')
    n = 21
    if len(argv) > 1:
        try: 
            n = int(argv[1]) + 1
        except:
            n = 21
    counter = 0
    async for x in message.channel.history(limit= n):
        if counter < n:
            await x.delete()
            counter += 1 


async def recall(message = 0):
    global participants, wait_channel
    for user in participants:
        try:
            await user.move_to(wait_channel)
            print(f'Moved {user} back to "{wait_channel}"')
        except discord.errors.HTTPException as e:
            print(e)
            print(f'{user} is not connected to voice.')
            pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$prune'):
        await prune(message)
    elif message.content.startswith('$recall'):
        await recall(message)


@client.event
async def on_ready():
    global guild, voice_channels, wait_channel_name, wait_channel, participants
    
    print(f'{client.user} has connected to Discord!\n')
    for g in client.guilds:
        if g.name == 'Design Science':
            guild = g

    ###
    #guild = client.get_guild(GUILD_ID)
    print(f'{client.user} is active on {guild.name}! ({guild.member_count - 1} members)')
    
    voice_channels = list(guild.voice_channels)

    wait_channel = list(filter(lambda x: wait_channel_name in x.name, voice_channels))[0]

    participants = list(filter(lambda x: x.bot == False, guild.members))

    pprint(list(map(lambda m: f'{m.id} : {m.name}', participants)))

client.run(TOKEN)
