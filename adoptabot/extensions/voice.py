from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, registry):
        self.registry = registry


    @commands.command(
        name='voice.list',
        description='Prints the voice lists',
        aliases=['v.l']
    )
    async def list_voice_channel(self, ctx):
        print(ctx.message.guild.voice_channels)
    # Register event mods or mod_roles
    # Register event channels (interactive embed with reaction)
    # register event groups (role)
    # register event size per channel
    # register event pairings ()
    