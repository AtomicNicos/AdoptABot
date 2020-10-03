# bot.py
import os
import asyncio
from pprint import pprint

import discord
from discord.utils import get

from dotenv import load_dotenv
from yaml import load, dump
from codecs import open as copen
import json
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def load_file():
    file = open('res/order.yaml', 'r')
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

global guild, enterprise_channels, voice_channels, wait_channel_name, announce_channel_name, botspam_channel_name, announce_channel, wait_channel, participants, running, members

guild = None
enterprise_channels, voice_channels = [], []
wait_channel_name, announce_channel_name, botspam_channel_name = WAIT_CHANNEL_NAME, ANNOUNCEMENTS_CHANNEL_NAME, BOTSPAM_CHANNEL_NAME
announce_channel, wait_channel = None, None
participants, members = [], []
running = False

"""

"""
async def prune(message = 0):
    if message.author.name != "AtomicNicos":
        await message.channel.send('You are not allowed to use this command! (<@&758595404983697419>)')
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

"""

"""
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

"""
async def recall(message = 0):
    global participants, wait_channel, running
    for user in participants:
        try:
            await user.move_to(wait_channel)
            print(f'Moved {user} back to "{wait_channel}"')
        except discord.errors.HTTPException:
            print(f'{user} is not connected to voice.')
            pass
    running = False

async def reload(message = 0):
    if message != 0:
        if message.author.name != "AtomicNicos":
            await message.channel.send('You are not allowed to use this command! (<@&758595404983697419>)')
            return

    global guild, enterprise_channels, voice_channels, wait_channel_name, announce_channel_name, announce_channel, wait_channel, participants, members

    voice_channels = list(guild.voice_channels)

    announce_channel = list(filter(lambda x: announce_channel_name in x.name, guild.text_channels))[0]

    enterprise_channels = list(filter(lambda x: wait_channel_name not in x.name, voice_channels))
    wait_channel = list(filter(lambda x: wait_channel_name in x.name, voice_channels))[0]

    print(f'There are [{len(enterprise_channels)} enterprise] | [1 waiting] voice channels')

    members = list(guild.members)
    participants = list(map(lambda a: a[0],filter(lambda y: "Participants" in list(map(lambda z: z.name,y[1])),map(lambda x: (x, x.roles), members))))
    enterprises = list(map(lambda a: a[0],filter(lambda y: "Entreprise" in list(map(lambda z: z.name,y[1])),map(lambda x: (x, x.roles), members))))

    print('\nAll of the members')
    f = copen('res/membs.json', mode='w', encoding='utf-8')
    a = {f'{m.id}': m.nick if m.nick is not None else m.name for m in participants}
    json.dump(a, f, indent=4, sort_keys=True)
    f.close()

    print(len(members))
    print(len(participants))
    print(len(enterprises))

"""

"""
async def assign_roles(message = 0):
    if message.author.name != "AtomicNicos":
        await message.channel.send('You are not allowed to use this command! (<@&758595404983697419>)')
        return

    global members, guild
    role = get(guild.roles, id=758591394922627092)
    print(role)

    for p in members:
        if p.name.startswith('ETU'):
            if role not in p.roles:
                print(f'{p.nick} | {p.name} gets role {role}')
                await p.add_roles(role)
        
        elif p.nick != None:
            if p.nick.startswith('ETU'):
                if role not in p.roles:
                    print(f'{p.nick} | {p.name} gets role {role}')
                    await p.add_roles(role)



"""
Loops through interviews, at start value = 0
"""
async def loop(start = 0, message = None):
    global guild, announce_channel, wait_channel, participants
    for r in range(start, ROUNDS):
        print(f'\n\nINTERVIEW ROUND {r}')
        await message.channel.send(f'ROUND {r + 1}/{ROUNDS}')

        assignment = list(map(lambda z: (guild.get_channel(z[0]), guild.get_member(z[1])), filter(lambda y: y[1] != -1, map(lambda x: (x[0], x[1][r]), ORDERING.items()))))

        for room, user in assignment:
            try:
                await user.move_to(room)
                print(f'Moved {user} to "{room}"')
            except discord.errors.HTTPException:
                print(f'{user} is not connected to voice.')
                pass
        
        await asyncio.sleep(TIME - ALERT)
        
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
        await asyncio.sleep(WAIT)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$prune'):
        await prune(message)
    elif message.content.startswith('$roles'):
        await assign_roles(message)
    elif message.content.startswith('$') and message.channel.name != botspam_channel_name:
        await message.channel.send('Please use channel <#758653291093032961> for all bot related activities! (<@&758595404983697419>)')
    elif message.content.startswith('$recall'):
        await recall(message)
    elif message.content.startswith('$start'):
        await startRounds(message)
    elif message.content.startswith('$reload'):
        await reload(message)

@client.event
async def on_ready():
    global guild, enterprise_channels, voice_channels, wait_channel_name, announce_channel_name, announce_channel, wait_channel, participants
    
    print(f'{client.user} has connected to Discord!\n')
    
    guild = client.get_guild(GUILD_ID)
    print(f'{client.user} is active on {guild.name}! ({guild.member_count - 1} members)')
    
    await reload()

    
client.run(TOKEN)
