from discord.ext import commands
from adoptabot.utils.utils import message_by_creator

class Event(commands.Cog):
    def __init__(self, bot, registry):
        self.bot = bot
        self.registry = registry

    def can_sender_edit_event(self, ctx):
        guild_id = f'{ctx.message.guild.id}'
        print(ctx.message.author.roles)
        print(self.registry.registry[guild_id]['event.moderators.roles'])
        return ctx.message.author.id in [self.registry.registry[guild_id]['event.creator']] + self.registry.registry[guild_id]['event.moderators'] # or message_by_creator(ctx)
    
    @commands.command(
        name='event.new',
        description='Registers a new event in the guild',
        aliases=['e.new']
    )
    async def register_new_event(self, ctx):
        self.registry.registry[f'{ctx.message.guild.id}'] = {
            "event.creator": ctx.message.author.id,
            "event.moderators": [],
            "event.moderators.roles": [],
            "event.roles": [],
            "event.vocal_channels": [],
            "event.wait_channels": [],
            "event.meet_time": -1,
            "event.wait_time": -1,
            "role.targets": {}
        }

        await ctx.message.add_reaction('\U0001F197')

    @commands.command(
        name='event.close',
        aliases=['e.close']
    )
    async def deregister_new_event(self, ctx):
        self.registry.registry.pop(f'{ctx.message.guild.id}', None)
        await ctx.message.add_reaction('\U0001F197')

    @commands.command(
        name='event.moderators',
        aliases=['e.mods']
    )
    async def set_event_moderators(self, ctx):
        if not self.can_sender_edit_event(ctx):
            ctx.send(f'{ctx.message.author} you may not use this command')

        argv = ctx.message.content.split(' ')
        for i in argv[1:]:
            self.registry.registry[f'{ctx.message.guild.id}']['event.moderators'] = list(set(self.registry.registry[f'{ctx.message.guild.id}']['event.moderators'] + list(map(lambda x: x.id, ctx.message.mentions))))

        await ctx.message.add_reaction('\U0001F197')


    @commands.command(
        name='event.moderators_roles',
        aliases=['e.modroles']
    )
    async def set_event_moderator_roles(self, ctx):
        if not self.can_sender_edit_event(ctx):
            ctx.send(f'{ctx.message.author} you may not use this command')

        for member in ctx.message.mentions:
            self.registry.registry[f'{ctx.message.guild.id}']['event.moderators'] += ctx.message.mentions

        await ctx.message.add_reaction('\U0001F197')


    # Register event mods or mod_roles
    # Register event channels (interactive embed with reaction)
    # register event groups (role)
    # register event size per channel
    # register event pairings ()
