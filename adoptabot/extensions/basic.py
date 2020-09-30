from discord.ext import commands
from datetime import datetime as d

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='ping',
        description='Gives an estimate of the delay between the client and the bot',
        aliases=[]
    )
    async def ping_command(self, ctx):
        start = d.timestamp(d.now())
        msg = await ctx.send(content='Pinging')
        await msg.edit(content=f'Pong!\nOne message round-trip took {( d.timestamp( d.now() ) - start ) * 1000 }ms.')
        return
    
    @commands.command(
        name='prune',
        description='Removes a select number of messages from the channel',
        aliases=['p'],
        usage='<number>'
    )
    async def prune_command(self, ctx):
        # TODO Remove in prod
        if ctx.message.author.name != "AtomicNicos":
            await ctx.message.channel.send('You are not allowed to use this command! (<@&758595404983697419>)')
            return
        
        n = 21
        argv = ctx.message.content.split(' ')
        if len(argv) > 1:
            try: 
                n = int(argv[1]) + 1
            except:
                ctx.send('A number must be specified.')

        counter = 0
        async for x in ctx.message.channel.history(limit= n):
            if counter < n:
                await x.delete()
                counter += 1

def setup(bot):
    bot.add_cog(Basic(bot))
