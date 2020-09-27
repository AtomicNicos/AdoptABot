# bot.py
import os
import asyncio
from pprint import pprint

import discord

from dotenv import load_dotenv
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def load_file():
    file = open('order.yaml', 'r')
    data = load(file, Loader=Loader)
    file.close()
    return (data['guild_id'], {[*a.keys()][0]: [*a.values()][0] for a in data['ordering']})

# ID OF THE "Adopt A Skill 2020" DISCORD SERVER
# ORDER OF PASSAGE (ENTERPRISE_CHANNEL_ID : List[USER_MEMBER_ID])
GUILD_ID, ORDERING = load_file()

# NUMBER OF INTERVIEW ROUNDS
ROUNDS = 14

# TIME OF EACH ROUND
TIME = 5 * 60

# WAITING PERIOD BETWEEN ROUNDS
WAIT = 1 * 60

# WHETHER @everyone should be called
SHOULD_ALERT = True;

# ALERT TIME
ALERT = 1

# WAIT VOICE CHANNEL NAME
WAIT_CHANNEL_NAME = "Salle d'attente"

# GENERAL ANNOUNCEMENTS TEXT CHANNEL NAME
ANNOUNCEMENTS_CHANNEL_NAME = "annonces"

# BOTSPAM CHANNEL NAME
BOTSPAM_CHANNEL_NAME = "botspam"

# Client
client = discord.Client()

global guild, enterprise_channels, voice_channels, wait_channel_name, announce_channel_name, botspam_channel_name, announce_channel, wait_channel, participants, running

guild = None
enterprise_channels, voice_channels = [], []
wait_channel_name, announce_channel_name, botspam_channel_name = WAIT_CHANNEL_NAME, ANNOUNCEMENTS_CHANNEL_NAME, BOTSPAM_CHANNEL_NAME
announce_channel, wait_channel = None, None
participants = []
running = False

async def prune(message = 0):
    argv = message.content.split(' ')
    n = 20
    if len(argv) > 1:
        try: 
            n = int(argv[1])
        except:
            n = 20
    counter = 0
    async for x in message.channel.history(limit= n):
        if counter < n:
            await x.delete()
            counter += 1 

async def startRounds(message = 0):
    global running
    if not running:
        argv = message.content.split(' ')
        start = 0
        if len(argv) > 1:
            try: 
                start = int(argv[1])
            except:
                start = 0
        running = True
        if not (-1 < start < ROUNDS):
            await message.channel.send(f'Value is not a valid round (0 <= {start} < {ROUNDS}, starting at 0)')
        else:
            await message.channel.send(f'Starting at round {start}')
            await loop(start, message)
        running = False
    else:
        await message.channel.send('Loop has already started')


"""
Loops through interviews, at start value = 0
"""
async def loop(start = 0, message = None):
    global guild, announce_channel, wait_channel, participants
    for r in range(start, ROUNDS):
        print(f'\n\nINTERVIEW ROUND {r}')
        await message.channel.send(f'ROUND {r + 1} / {ROUNDS}')

        assignment = list(map(lambda z: (guild.get_channel(z[0]), guild.get_member(z[1])), filter(lambda y: y[1] != -1, map(lambda x: (x[0], x[1][r]), ORDERING.items()))))

        for room, user in assignment:
            try:
                await user.move_to(room)
                print(f'Moved {user} to "{room}"')
            except discord.errors.HTTPException:
                print(f'{user} is not connected to voice.')
                pass
        
        await asyncio.sleep(TIME / 60 - ALERT)
        
        await announce_channel.send(f'{"@everyone " if SHOULD_ALERT else ""}Round {r+1}/{ROUNDS} finishes in {ALERT} seconds !')
        await asyncio.sleep(ALERT)
        
        print('\nBREAK')
        await message.channel.send('INTER-ROUND BREAK')

        if r != ROUNDS - 1:
            await announce_channel.send(f'{"@everyone " if SHOULD_ALERT else ""}Round {r+1} will begin in {WAIT / 20} seconds.')
        
        for user in participants:
            try:
                await user.move_to(wait_channel)
                print(f'Moved {user} back to "{wait_channel}"')
            except discord.errors.HTTPException:
                print(f'{user} is not connected to voice.')
                pass
        await asyncio.sleep(WAIT / 20)



@client.event
async def on_message(message):
    global botspam_channel_name, running
    if message.author == client.user:
        return

    if message.content.startswith('$prune'):
        await prune(message)
    elif message.content.startswith('$') and message.channel.name != botspam_channel_name:
        await message.channel.send('Please use channel <#758653291093032961> for all bot related activities! (<@&758595404983697419>)')
    elif message.content.startswith('$start'):
        await startRounds(message)


@client.event
async def on_ready():
    global guild, enterprise_channels, voice_channels, wait_channel_name, announce_channel_name, announce_channel, wait_channel, participants
    
    print(f'{client.user} has connected to Discord!\n')
    
    guild = client.get_guild(GUILD_ID)
    print(f'{client.user} is active on {guild.name}! ({guild.member_count - 1} members)')
    
    voice_channels = list(guild.voice_channels)

    announce_channel = list(filter(lambda x: announce_channel_name in x.name, guild.text_channels))[0]

    enterprise_channels = list(filter(lambda x: wait_channel_name not in x.name, voice_channels))
    wait_channel = list(filter(lambda x: wait_channel_name in x.name, voice_channels))[0]

    print(f'There are [{len(enterprise_channels)} enterprise] | [1 waiting] voice channels')

    participants = list(map(lambda a: a[0],filter(lambda y: "Participants" in list(map(lambda z: z.name,y[1])),map(lambda x: (x, x.roles), guild.members))))

    print('\nAll of the members')
    pprint(list(map(lambda m: f'{m.id} : {m.name}', guild.members)))

    
client.run(TOKEN)