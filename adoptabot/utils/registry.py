import json
import os
from pprint import pprint
from discord.ext import commands
from adoptabot.utils.utils import message_by_creator

class Registry():
    def __init__(self):
        self.REG_PATH = 'res/registry.json'
        if not os.path.exists(self.REG_PATH):
            f = open(self.REG_PATH, mode='w')
            f.write('{ }')
            f.close()
        
        f = open(self.REG_PATH)
        self.registry = json.load(f)
        f.close()
    
    def close(self):
        f = open(self.REG_PATH, mode='w')
        json.dump(self.registry, f)
        f.close()

class RegistryVisible(commands.Cog):
    def __init__(self, bot, registry):
        self.bot = bot
        self.registry = registry
    
    @commands.command(
        name='registry.print',
        description='Prints out the registry',
        aliases=['reg.p'],
        hidden=True
    )
    async def print_registry(self, ctx):
        if not message_by_creator(ctx):
            return
        
        pprint(self.registry.registry)
